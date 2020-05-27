from api_binder import *
from mock import make_mock
import pickle


# todo: Implement function to get streak independant average imbalance
#  and standard deviation for average amount of win/lose streak players per game


USEMOCK = False
REFERENCE_PLAYER = "OneTabz"


class MM:
    def __init__(self):
        self.streaks = ['win', 'lose', 'neutral']
        self.data_count = 0
        self.total_imbalance = 0
        self.nwinstreaks = []
        self.nlosestreaks = []


    def main(self, match):
        matchid = match['gameId']
        # getting player's teams and current streak status before game
        match_players = [[], []]
        players_streaks = [[], []]
        for part in range(10):
            curaccid = match['participantIdentities'][part]['player']['accountId']
            team = int(match['participants'][part]['stats']['win'])
            match_players[team].append(curaccid)
            print(f"Getting player {part + 1} current streak")
            players_streaks[team].append(self.get_streak(curaccid, matchid))
        nonecount = players_streaks[0].count(3) + players_streaks[1].count(3)
        if nonecount > 2:
            print("Too many missing data")
            return None
        print("Current game streaks: ", end="")
        print(players_streaks)
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
        if USEMOCK:
            matches = mock.players_games[accountid]
        else:
            matches = get_matches(accountid, 3)
        if matches is not None:
            if matches[0]['gameId'] == match_id:
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
                return 3
        else:
            return 3


    def get_imbalance(self):
        return self.total_imbalance // self.data_count


    def get_stats(self):
        print("\nAverage imbalance is " + str(self.get_imbalance()))
        print("Games in db: " + str(self.data_count))
        print(self.nwinstreaks)
        print(self.nlosestreaks)


def create_db_file():
    save = MM()
    with open('db.dat', 'wb') as file:
        pickle.dump(save, file)


def run(playername, iterations=1):
    try:
        with open('db.dat', 'rb') as file:
            db = pickle.load(file)
    except IOError:
        print("db file missing, creating it")
        create_db_file()
        with open('db.dat', 'rb') as file:
            db = pickle.load(file)

    print("Getting API data")

    if USEMOCK:
        match = mock.main_game
    else:
        match = get_recent_match(playername)

    if match != -1:
        matchid = match['gameId']
        print("Getting match " + str(matchid))
        db.main(match)
        for it in range(iterations):
            res = None
            while res is None:
                queueid = 0
                while queueid != 420:  # blaze it rito
                    matchid -= 1
                    match = get_match(matchid)
                    if match != -1:
                        queueid = match["queueId"]

                print("Getting match " + str(match['gameId']))
                res = db.main(match)
        db.get_stats()

        with open('db.dat', 'wb') as file:
            pickle.dump(db, file)


if USEMOCK:
    try:
        with open('mock.dat', 'rb') as f:
            mock = pickle.load(f)
    except IOError:
        print("no mock file, creating it")
        make_mock(REFERENCE_PLAYER)
        with open('mock.dat', 'rb') as f:
            mock = pickle.load(f)

run(REFERENCE_PLAYER, 50)
