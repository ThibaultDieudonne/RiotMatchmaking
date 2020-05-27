from api_binder import *
from mock import make_mock
import pickle


# todo: Implement function to get streak independant average imbalance
#  and standard deviation for average amount of win/lose streak players per game


ITERATIONS = 10
INITIAL_GAME_ID = 4625931783
USEMOCK = False  # Don't touch


class MM:
    def __init__(self):
        self.streaks = ['win', 'lose', 'neutral']
        self.data_count = 0
        self.total_imbalance = 0
        self.nwinstreaks = []
        self.nlosestreaks = []
        self.current_game_id = INITIAL_GAME_ID


    def main(self, match):
        matchid = match['gameId']
        # getting player's teams and current streak status before game
        match_players = [[], []]
        players_streaks = [[], []]
        print(f"Getting players' current streaks")
        for part in range(10):
            curaccid = match['participantIdentities'][part]['player']['accountId']
            team = int(match['participants'][part]['stats']['win'])
            match_players[team].append(curaccid)
            players_streaks[team].append(self.get_streak(curaccid, matchid))
        nonecount = players_streaks[0].count(3) + players_streaks[1].count(3)
        if nonecount > 2:
            return None
        # constructing streaks data
        local_streak_count = [0, 0]
        team_streak_count = [0, 0, 0, 0]
        local_imbalance = 0
        for strk in range(2):
            local_streak_count[strk] += players_streaks[0].count(strk) + players_streaks[1].count(strk)
        for tm in range(2):
            for strk in range(2):
                team_streak_count[tm * 2 + strk] = 2 * players_streaks[tm].count(strk)
        # computing game imbalance
        for dat in range(4):
            local_imbalance += abs(team_streak_count[dat] - local_streak_count[dat % 2])
        # removing bias
        bias = 2 * (local_streak_count[0] % 2 + local_streak_count[1] % 2)
        local_imbalance -= bias
        # updating data
        self.total_imbalance += local_imbalance
        self.data_count += 1
        self.nwinstreaks.append(players_streaks[0].count(0) + players_streaks[1].count(0))
        self.nlosestreaks.append(players_streaks[0].count(1) + players_streaks[1].count(1))

        return 1


    @staticmethod
    def get_streak(accountid, match_id):
        global replace_index
        if USEMOCK:
            matches = mock.players_games[accountid]
        else:
            matches = get_matches(accountid, 3)
        if matches is not None:
            curmatchid = matches[0]['gameId']
            if curmatchid == match_id and len(matches) > 2:
                oc1 = get_outcome(accountid, matches[1])
                oc2 = get_outcome(accountid, matches[2])
                if oc1 and oc2:
                    result = 0  # win streak
                elif oc1 or oc2:
                    result = 2  # neutral
                else:
                    result = 1  # lose streak
                return result
            else:
                if curmatchid > replace_index:
                    replace_index = curmatchid
                return 3
        else:
            return 3


    def get_imbalance(self):
        return self.total_imbalance // self.data_count


    def get_stats(self):
        print("\nAverage imbalance is " + str(self.get_imbalance()))
        print("Games in db: " + str(self.data_count))
        print("Last game id: " + str(self.current_game_id))


def create_db_file():
    save = MM()
    with open('db.dat', 'wb') as file:
        pickle.dump(save, file)


def run(matchid, iterations=1):
    global replace_index

    try:
        with open('db.dat', 'rb') as file:
            db = pickle.load(file)
    except IOError:
        print("db file missing, creating it")
        create_db_file()
        with open('db.dat', 'rb') as file:
            db = pickle.load(file)
    if INITIAL_GAME_ID > db.current_game_id:
        db.current_game_id = INITIAL_GAME_ID

    print("Getting API data")
    if USEMOCK:
        match = mock.main_game
        db.main(match)
    else:
        for it in range(iterations):
            res = None
            while res is None:
                queueid = 0
                while queueid != 420:  # blaze it rito
                    if matchid < replace_index:
                        matchid = replace_index
                    else:
                        matchid += 1
                    match = get_match(matchid)
                    if match != -1:
                        queueid = match["queueId"]

                print("Getting match " + str(match['gameId']))
                res = db.main(match)
            print(f"Done: {it + 1}/{iterations}")
            db.current_game_id = matchid
    db.get_stats()

    with open('db.dat', 'wb') as file:
        pickle.dump(db, file)


if USEMOCK:
    try:
        with open('mock.dat', 'rb') as f:
            mock = pickle.load(f)
    except IOError:
        print("no mock file, creating it")
        make_mock(INITIAL_GAME_ID)
        with open('mock.dat', 'rb') as f:
            mock = pickle.load(f)

replace_index = 0
run(INITIAL_GAME_ID, ITERATIONS)
