from api_binder import *
import pickle


class Mock:
    def __init__(self, matchid):
        self.main_game = get_match(matchid)
        self.players_games = {}
        for part in range(10):
            accountid = self.main_game['participantIdentities'][part]['player']['accountId']
            self.players_games[accountid] = get_matches(accountid, 3)


def make_mock(playername):
    mock = Mock(playername)
    with open('mock.dat', 'wb') as file:
        pickle.dump(mock, file)

