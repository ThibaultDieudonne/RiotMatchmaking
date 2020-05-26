# RiotMatchmaking

Algorithm based on League of Legends game data to determine whether or not RIOT is biasing matchmaking to team up players in lose/win streak.

DuoQ may be a bias.

# todo

Still bugged, need to save to disk while requesting API to make debug reruns

# Code Structure

 players = []

 streaks = ['win', 'neutral', 'lose']

 teammates = [win_win, win_neutral, win_lose,
             neutral_win, neutral_neutral, neutral_lose,
             lose_win, lose_neutral, lose_lose]

 opponents = [win_win, win_neutral, win_lose,
             neutral_win, neutral_neutral, neutral_lose,
             lose_win, lose_neutral, lose_lose]

 streak_count = [n_win, n_neutral, n_lose]



