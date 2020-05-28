import numpy as np
from api_binder import *
from mock import make_mock
import pickle
import math


ITERATIONS = 200
INITIAL_GAME_ID = 4627415281
USEMOCK = False  # Don't touch
np.random.seed(0)


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
        nonecount = 0
        for part in range(10):
            curaccid = match['participantIdentities'][part]['player']['accountId']
            team = int(match['participants'][part]['stats']['win'])
            match_players[team].append(curaccid)
            curstreak = self.get_streak(curaccid, matchid)
            if curstreak == 3:
                nonecount += 1
                if nonecount > 2:
                    print("Skipping this game (lack of data)")
                    return None
            players_streaks[team].append(curstreak)
        # constructing streaks data
        local_streak_count = [0, 0]
        team_streak_count = [0, 0, 0, 0]
        local_balance = 0
        for strk in range(2):
            local_streak_count[strk] += players_streaks[0].count(strk) + players_streaks[1].count(strk)
        for tm in range(2):
            for strk in range(2):
                team_streak_count[tm * 2 + strk] = 2 * players_streaks[tm].count(strk)
        # computing game balance
        for dat in range(4):
            local_balance += abs(team_streak_count[dat] - local_streak_count[dat % 2])
        # removing bias
        bias = 2 * (local_streak_count[0] % 2 + local_streak_count[1] % 2)
        local_balance -= bias
        # updating data
        self.total_imbalance += local_balance
        self.data_count += 1
        self.nwinstreaks.append(local_streak_count[0])
        self.nlosestreaks.append(local_streak_count[1])
        # writing to disk (as time cost is negligible considering API response time)
        with open('db.dat', 'wb') as file:
            pickle.dump(self, file)
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


    def get_balance(self):
        return round(float(self.total_imbalance) / self.data_count, 1)


    def get_stats(self):
        print("\nAverage riot_balance is " + str(self.get_balance()))
        print("riot_sd for win streaks is " + str(get_sd(self.nwinstreaks, self.data_count)))
        print("riot_sd for lose streaks is " + str(get_sd(self.nlosestreaks, self.data_count)))
        print("Games in db: " + str(self.data_count))
        print("Last game id: " + str(self.current_game_id))
        print("Total win streak players: " + str(sum(self.nwinstreaks)))
        print("Total lose streak players: " + str(sum(self.nlosestreaks)))
        print(f"Cumulated riot_balance: {self.total_imbalance}")
        self.make_simulation()


    def make_simulation(self):
        n_lobbies = 1000
        print(f"\nCreating {n_lobbies} fake lobbies")
        total_imbalance = 0
        nwinstreaks = []
        nlosestreaks = []
        divisor = float(10 * self.data_count)
        total_wins = sum(self.nwinstreaks)
        total_loses = sum(self.nlosestreaks)
        params = [total_wins, total_loses, divisor - total_wins - total_loses]
        for i in range(3):
            params[i] /= divisor
        for fake_lobby in range(n_lobbies):
            # filling lobby with random players and constructing streaks data
            players_streaks = [[], []]
            local_streak_count = [0, 0]
            team_streak_count = [0, 0, 0, 0]
            for tm in range(2):
                for part in range(5):
                    strk = np.random.choice([0, 1, 2], p=params)
                    players_streaks[tm].append(strk)
                    if strk < 2:
                        local_streak_count[strk] += 1
                        team_streak_count[2 * tm + strk] += 1
            local_balance = 0
            # computing game balance
            for dat in range(4):
                local_balance += abs(team_streak_count[dat] - local_streak_count[dat % 2])
            # removing bias
            bias = 2 * (local_streak_count[0] % 2 + local_streak_count[1] % 2)
            local_balance -= bias
            # updating data
            total_imbalance += local_balance
            nwinstreaks.append(local_streak_count[0])
            nlosestreaks.append(local_streak_count[1])
        # printing results
        print("Average model_balance is " + str(round(total_imbalance / 1000., 1)))
        print("riot_sd for win streaks is " + str(get_sd(nwinstreaks, n_lobbies)))
        print("riot_sd for lose streaks is " + str(get_sd(nlosestreaks, n_lobbies)))


def create_db_file():
    save = MM()
    with open('db.dat', 'wb') as file:
        pickle.dump(save, file)


def get_sd(values, n):
    res = 0.
    av = sum(values) / float(n)
    for r in values:
        res += (r - av)**2
    res /= n
    return round(math.sqrt(res), 1)


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


if __name__ == "__main__":
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
