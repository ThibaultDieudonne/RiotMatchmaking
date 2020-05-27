# RiotMatchmaking

# Abstract

It's been a while a lot of League of Legends streamers claim matchmaking is rigged. Part of complaining players are convinced matchmaking algorithm unbalances games on purpose, in order to maximize their play time.

It would theoretically be possible, because the probability for a player to start a new game is correlated to his previous games results. Modern learning algorithms would definitely be able to find such tendancies. Moreover, players' playtime is strongly correlated with the money Riot earn (more overall playtime leads to higher game popularity, and both these factors make overall money spending grow). So why not ?

From an entertaining view, it would be pretty bad for League of Legends if the games' quality and/or the team compositions were purposely unbalanced.

This program goal is to get a statistical certainty on this question, by analysing game data to determine whether or not the algorithm is streak dependant (as games MMR are obviously not imbalanced).
We will study both game composition (standard deviation for average amount of win/lose streak players per game) and teams composition (average team imbalance).

# Process

We define streaks as follow: if last two games were wins/loses, the player is considered win/lose streaking, otherwise he's neutral (a missing data for a player will make him neutral since it doesn't bias our results, but if a game lacks more than 2 players' data, it is just skipped).

Note this whole metric is unbiased: if matchmaking algorithm is considering streaks over a bigger game history, we may necessarily see some repercussions by only observing last two games. If matchmaking algorithm was considering other parameters than streaks it may also have repercussions on it. 

As we observe a game we get every player's current streak. Then we compute a "riot_imbalance" value, proportionnal to team imbalance from a streak perspective.

We can compare riot_imbalance average for a large game sample with the same "imbalance" concept applied to a streak-independant team making algorithm, respecting the amount of win streaks, lose streaks and neutrals players. In pratice we just create a large amount of "fake lobbies" by sampling players' streaks with probabilities from the real games sample.

If riot_imbalance is much greater than streak independant imbalance then Riot is definitely rigging team making, in order to control players' streaks.
If the values are close, Riot team making might not be rigged.
If riot_imbalance is much lower, it means that Riot team making is streak dependant, but it tends to balance winning/losing players over teams.

We also compute standard deviation for average amount of win/lose streak players per game, for real games and our fake lobbies.
Again, if Riot's values are higher, then it would be a proof that Riot matchmaking is streak dependant (i.e. players with the same streak are more likely to play in the same games).

# Results

To be published.

# How to run

To see database statistics: run "python3 stats.py".

To fill the database or create a fresh one (by deleting db.dat file):

- install pantheon (python API binder) with "pip install pantheon"

- fill your own Riot API key into "api_binder.py".

- run script with "python3 analysis.py".

The program will update the database with ITERATIONS games' data at each run. The very low speed issue is dued to riot API not making it easy to look for game histories before a particular game, and high limitation of requests per minute.

When creating a fresh database it is strongly recommended to update INITIAL_GAME_ID in "analysis.py" with the "Last game id" value shown by stats.py (updated each time database is filled).





