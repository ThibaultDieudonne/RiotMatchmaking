# RiotMatchmaking

# Abstract

It's been a while a lot of League of Legends streamers claim matchmaking is rigged. Part of complaining players are convinced matchmaking algorithm imbalances games on purpose, in order to maximize their play time.

It would theoretically be possible, because the probability for a player to start a new game is correlated to his previous results: players losing several games in a row are likely to lower their play time in a near future, while players winning several games in a row are not that likely to increase their play time as much. Moreover, playtime is strongly correlated with the money Riot earn (more overall playtime leads to higher game popularity, and both these factors make overall money spending grow). So their might be a capital gain trying to avoid long lose streaks.

From an entertaining view, it would be pretty bad for League of Legends if the quality of the games and/or the team compositions were purposely imbalanced.

This program goal is to get a statistical certainty on this question, by analysing game data to determine whether or not the algorithm is streak dependant (as games MMR are obviously not imbalanced).
We will study both game composition (standard deviation for average amount of win/lose streak players per game) and teams composition (average team balance).

# Process

We define streaks as follow: if last two games were wins/loses, the player is considered in win/lose streak, otherwise he's neutral (a missing data for a player will make him neutral since it doesn't bias our results, but if a game lacks more than 2 players' data, it is just skipped).

Note this whole metric is unbiased: if matchmaking algorithm is considering streaks over a bigger game history, we may necessarily see some repercussions by only observing last two games. If matchmaking algorithm was considering other parameters than streaks it may also have repercussions on it. 

As we observe a game we get every player's current streak (previous two games results).

To make effective interpretations, we implemented a streak-independant team making algorithm. Previous games results are sampled with frequencies calculated from the real games sample.

We keep track of each game results separately in order to compute their standard deviation (riot_sd). Then we compare with the same standard deviations for our own streak independant model (model_sd).

We also compute a "riot_balance" value, proportionnal to team balance from a streak perspective.

We compare riot_balance average for a large game sample with the same "streak balance" concept applied to our model (model_balance).

#Interpretations

1) Standard deviations

It is important to check if the whole games are imbalanced because it would produce biased results for team making analysis.

We expect riot_sd and model_sd values to be close because we wan't think of a capital gain to fill games according to recent games results.

2) Balance values

To compare balance values we consider what a big imbalance would have been to make unbiased interpretations.

If riot_balance is much greater than model_balance: team making is streak dependant. Win streak players are more likely to play in the same team, and against lose streak players (and reciprocally).
We don't expect to see this result since it would produce the opposite effect to the one described in abstract.

If riot_balance is close to model_balance: team making is not streak dependant. Complaining players would have been misled because of human brain variance perception.

If riot_balance is much lower than model_balance: team making is streak dependant and balances winning and losing players over teams. Win streak players are more likely to play with lose streak players.
This is the result complaining players can expect.

We also compute standard deviation for average amount of win/lose streak players per game, for real games and our fake lobbies.
Again, if Riot's values are higher, then it would be a proof that Riot matchmaking is streak dependant (i.e. players with the same streak are more likely to play in the same games).

# Results

In practice a balanced game returns a value of 0, and a strongly imbalanced game produces a value greater than 4.

For the firsts 200 games (relatively small sample, even if it already took more than 6 hours to compute), standards deviations are relatively close (1.6/1.4 for win streaks, 1.5/1.3 for lose streaks).
Average riot_balance is 2.6 while average model_balance is 2.9. With a 95% confidence interval, Riot team making is streak independant.

1000 games to be published.

# How to run

Get a python3 distribution.

To see database statistics: run "python3 -m stats.py".

To fill the current database or create a fresh one (by deleting db.dat file):

- install pantheon (python API binder) with "pip install pantheon"

- fill your own Riot API key into "api_binder.py".

- run script with "python3 -m analysis.py".

The program will update the database with an ITERATIONS (in "analysis.py") number of games at each run. The very low speed issue is dued to riot API not making it easy to look for game histories before a particular game, and high limitation of requests per minute.

When creating a fresh database it is strongly recommended to update INITIAL_GAME_ID in "analysis.py" with the "Last game id" value shown by stats.py (updated each time database is filled).





