from pantheon import pantheon
import asyncio
import json
import pickle


server = "euw1"
api_key = "RGAPI-591df5d2-9d77-4d90-a325-4f6958105052"


def requestsLog(url, status, headers):
    print(url)
    print(status)
    print(headers)


panth = pantheon.Pantheon(server, api_key, errorHandling=True, requestsLoggingFunction=requestsLog, debug=True)


class MM:
    def __init__(self):
        self.streaks = ['win', 'neutral', 'lose']
        self.teammates = [0 for _ in range(9)]
        self.opponents = [0 for _ in range(9)]
        self.streak_count = [0 for _ in range(3)]

    def p(self, streak):
        return float(self.streak_count[streak]) / sum(self.streak_count)

    def p_play_with(self, streak0, streak1):
        s = sum(self.teammates[streak0:streak0 + 3])
        if s:
            return float(self.teammates[streak0 * 3 + streak1]) / s
        return 0

    def p_play_against(self, streak0, streak1):  # changed
        s = sum(self.opponents[streak0:streak0 + 3])
        if s:
            return float(self.opponents[streak0 * 3 + streak1]) / s
        return 0

    def main(self):
        with open('challenger_names.txt', 'rb') as file:
            players = pickle.load(file)
        for current_player in players:
            matches = load_matches(current_player, 3)
            game_id = matches[0]['gameId']
            sorted_players = [[], []]  # 0 for losers 1 for winners
            for part in range(10):
                current_name = matches[0]['participantIdentities'][part]['player']['summonerName']
                if current_name == current_player:
                    p_team = int(matches[0]['participants'][part]['stats']['win'])
                    print('Owner in team ' + str(p_team))
                    oc1 = get_outcome(current_player, matches[1])
                    oc2 = get_outcome(current_player, matches[2])
                    print(oc1, oc2)
                    if oc1 and oc2:
                        current_streak = 0
                    elif oc1 or oc2:
                        current_streak = 1
                    else:
                        current_streak = 2
                else:
                    sorted_players[int(matches[0]['participants'][part]['stats']['win'])].append(current_name)
            print(sorted_players)
            for tm in sorted_players[p_team]:
                tm_streak = getStreak(tm, game_id)
                if tm_streak != -1:
                    self.streak_count[tm_streak] += 1
                    self.teammates[current_streak * 3 + tm_streak] += 1
            for op in sorted_players[1 - p_team]:
                op_streak = getStreak(op, game_id)
                if op_streak != -1:
                    self.streak_count[op_streak] += 1
                    self.opponents[current_streak * 3 + op_streak] += 1

        for i, s in enumerate(self.streaks):
            print("Expected " + s + " streak probability: " + str(100 * self.p(i)) + "%")
        print('\n')
        for i, s0 in enumerate(self.streaks):
            for j, s1 in enumerate(self.streaks):
                print(s0 + " streak plays with " + s1 + " streak " + str(100 * self.p_play_with(i, j)) + "%")
                print(s0 + " streak plays against " + s1 + " streak " + str(100 * self.p_play_against(i, j)) + "%\n")


async def getSummonerId(mname):
    try:
        data = await panth.getSummonerByName(mname)
        return data['id'], data['accountId']
    except Exception as e:
        print(e)


async def getRecentMatchlist(maccountId, n):
    try:
        data = await panth.getMatchlist(maccountId, params={"endIndex": n})
        return data
    except Exception as e:
        print(e)


async def getRecentMatches(maccountId, n):
    try:
        matchlist = await getRecentMatchlist(maccountId, n)
        tasks = [panth.getMatch(match['gameId']) for match in matchlist['matches']]
        return await asyncio.gather(*tasks)
    except Exception as e:
        print(e)


async def getChallengerNames():
    try:
        data = await panth.getChallengerLeague()
        return data
    except Exception as e:
        print(e)


def get_names(limit=-1):
    print('Getting challenger names')
    chall_names = []
    loop = asyncio.get_event_loop()
    data = loop.run_until_complete(getChallengerNames())
    for i, chall in enumerate(data['entries']):
        if i == limit:
            break
        chall_names.append(chall['summonerName'])
    with open('challenger_names.txt', 'wb') as file:
        pickle.dump(chall_names, file)


def original_load_matches(name, n):
    try:
        loop = asyncio.get_event_loop()
        (summonerId, accountId) = loop.run_until_complete(getSummonerId(name))
        return loop.run_until_complete(getRecentMatches(accountId, n))
    except Exception as e:
        print(e)


def load_matches(name, n):
    return mocked_matches[mocked_names[name]][:n]  # changed


def getStreak(name, match_id):
    nload = 10
    matches = load_matches(name, nload)
    print("Reference is " + str(match_id))
    for g in range(nload - 2):
        print("Current match_id is " + str(matches[g]['gameId']))
        if matches[g]['gameId'] == match_id:
            oc1 = get_outcome(name, matches[g + 1])
            oc2 = get_outcome(name, matches[g + 2])
            if oc1 and oc2:
                return 0
            elif oc1 or oc2:
                print("Returning 1 for " + name)
                return 1
            else:
                return 2
    print("Returning -1 for " + name)
    return -1


def get_outcome(name, game):
    for part in range(10):
        if game['participantIdentities'][part]['player']['summonerName'] == name:
            return game['participants'][part]['stats']['win']


def create_db_file():
    save = MM()
    with open('db.dat', 'wb') as file:
        pickle.dump(save, file)


def run():
    with open('db.dat', 'rb') as file:
        db = pickle.load(file)
    db.main()
    with open('db.dat', 'wb') as file:
        pickle.dump(db, file)


# preload and make test run


def make_mock():
    mocked_m = []
    cor = {}
    with open('challenger_names.txt', 'rb') as file:
        player = pickle.load(file)[0]
    m = original_load_matches(player, 1)[0]
    for part in range(10):
        cor[m['participantIdentities'][part]['player']['summonerName']] = part
        mocked_m.append(original_load_matches(m['participantIdentities'][part]['player']['summonerName'], 10))
    with open('mock.dat', 'wb') as file:
        pickle.dump(mocked_m, file)
    with open('dict.dat', 'wb') as file:
        pickle.dump(cor, file)


with open('mock.dat', 'rb') as f:
    mocked_matches = pickle.load(f)
with open('dict.dat', 'rb') as f:
    mocked_names = pickle.load(f)
#
run()
