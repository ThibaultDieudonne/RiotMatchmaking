from api_binder import *
from mock import Mock, make_mock
import pickle


# todo: Implement function to get streak independant average imbalance
USEMOCK = True
REFERENCE_PLAYER = "Pixel Pangolin"


class MM:
    def __init__(self):
        self.streaks = ['win', 'lose', 'neutral']
        self.data_count = 0
        self.total_imbalance = 0
        self.streak_count = [0 for _ in range(3)]


    def main(self, match):
        matchid = match['gameId']
        # getting player's teams and current streak status before game
        match_players = [[], []]
        players_streaks = [[], []]
        for part in range(10):
            curaccid = match['participantIdentities'][part]['player']['accountId']
            team = int(match['participants'][part]['stats']['win'])
            match_players[team].append(curaccid)
            players_streaks[team].append(self.get_streak(curaccid, matchid))
        # constructing streaks data
        local_streak_count = [0, 0]
        team_streak_count = [0, 0, 0, 0]
        local_imbalance = 0
        for strk in range(2):
            local_streak_count[strk] += players_streaks[0].count(strk) + players_streaks[1].count(strk)
        for tm in range(2):
            for strk in range(2):
                team_streak_count[tm * 2 + strk] = players_streaks[tm].count(strk)
        # computing game imbalance
        for dat in range(4):
            local_imbalance += team_streak_count[dat] - local_streak_count[dat % 2]
        # removing bias
        local_imbalance -= 2 * (local_streak_count[0] % 2 + local_streak_count[1] % 2)

        self.total_imbalance += local_imbalance


    def get_streak(self, accountid, match_id):
        if USEMOCK:
            matches = mock.players_games[accountid]
        else:
            matches = get_matches(accountid, 3)
        try:
            if matches[0]['gameId'] == match_id:
                oc1 = get_outcome(accountid, matches[1])
                oc2 = get_outcome(accountid, matches[2])
                if oc1 and oc2:
                    result = 0
                elif oc1 or oc2:
                    result = 2
                else:
                    result = 1
                self.streak_count[result] += 1
                self.data_count += 1
                return result
        except Exception as e:
            print(e)
        return -1


    def get_imbalance(self):
        return round(float(self.total_imbalance) / self.data_count, 1)


    def get_stats(self):
        print("Average imbalance is " + str(self.get_imbalance()))
        print("Total win streak players: " + str(self.streak_count[0]))
        print("Total lose streak players: " + str(self.streak_count[1]))
        print("Total neutral players: " + str(self.streak_count[2]))


def create_db_file():
    save = MM()
    with open('db.dat', 'wb') as file:
        pickle.dump(save, file)


def run(playername):
    try:
        with open('db.dat', 'rb') as file:
            db = pickle.load(file)
    except IOError:
        print("db file missing, creating it")
        create_db_file()
        with open('db.dat', 'rb') as file:
            db = pickle.load(file)

    if USEMOCK:
        match = mock.main_game
    else:
        match = get_recent_match(playername)

    db.main(match)
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

run(REFERENCE_PLAYER)
