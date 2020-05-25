# RiotMatchmaking
Algorithm based on League of Legends game data to determine whether or not RIOT is biasing matchmaking to team up players in lose/win streak

# PSEUDO PYTHON CODE

# possible bias: duoQs

# vars:

 players = []

 streaks = ['win', 'neutral', 'lose']

 teammates = [win_win, win_neutral, win_lose,
             neutral_win, neutral_neutral, neutral_lose,
             lose_win, lose_neutral, lose_lose]

 opponents = [win_win, win_neutral, win_lose,
             neutral_win, neutral_neutral, neutral_lose,
             lose_win, lose_neutral, lose_lose]

 streak_count = [n_win, n_neutral, n_lose]

# internal functions:

 p(streak): return streak_count[streak] / sum(streak_count)

 p_play_with(streak0, streak1): return teammates[streak0 * 3 + streak1] / sum(teammates[streak0:])

 p_play_against(streak0, streak1): return teammates[streak0 * 3 + streak1] / sum(teammates[streak0:])

 main():
  players = get_players()
  for current_player in players:
   last_game_id = get_last_game_id(current_player)
   current_streak = get_player_streak()
   for mplayer != player in game_player(last_game_id):
    mplayer_streak = get_player_streak(mplayer, last_game_id)
    streak_count[mplayer_streak] += 1
    teammates/opponents[current_streak * 3 + mplayer_streak] += 1

  for i,s in enumerate(streaks):
   print("Expected " + s + " streak probability: " + str(100*p(i)) + "%")
  print('\n')
  for i,s0 in enumerate(streaks):
   for j,s1 in enumerate(streaks):
    print(s0 + " streak plays with " + s1 + " streak " +  str(100*p_play_with(i,j)) + "%")
    print(s0 + " streak plays against " + s1 + " streak " +  str(100*p_play_against(i,j)) + "%\n")

# external functions:

get_last_game_id: returns int game_id of last ranked played by a given player
get_player_streak: use heuristic based on history to return int in [0,2]



