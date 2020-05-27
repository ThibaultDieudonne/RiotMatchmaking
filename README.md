# RiotMatchmaking

# Abstract

It's been a while a lot of League of Legends streamers claim matchmaking is rigged. Complaining players are convinced matchmaking algorithm controls players streaks to maximize their play time.
This program goal is to get a statistical certainty on this question, by analysing game data to determine whether or not the algorithm is streak dependant (as games MMR are obviously not imbalanced).
We will both study game composition (standard deviation for average amount of win/lose streak players per game) and teams composition (average team imbalance).

# Process

We define streaks as follow: if last two games were wins/loses, the player is considered win/lose streaking, otherwise he's neutral.

Note this metric is unbiased: if matchmaking algorithm is considering streaks over a bigger game history, we would necessarily see some repercussions by only observing last two games.

As we observe a game we get every player's current streak. Then we compute a "riot_imbalance" value, proportionnal to team imbalance from a streak perspective.

We can compare riot_imbalance average for a large game sample with the same "imbalance" concept applied to a streak-independant team making algorithm respecting the amount of win streaks, lose streaks and neutrals players. In pratice we just create a large amount of "fake lobbies" by sampling players' streaks with probabilities from the real sample.

If riot_imbalance is much greater than streak independant then Riot is definitely rigging team making to control player's streaks.
If the values are close Riot team making might not be rigged.
If riot_imbalance is much lower, it means that Riot team making is streak dependant, but it tends to balance winning/losing players over teams.

We also compute standard deviation for average amount of win/lose streak players per game, for real games and our fake lobbies.
Again, if riot's values are higher, then it would be a proof that Riot matchmaking is streak dependant.

# Results

To be published.

# How to run

To see database statistics run "stats.py".

To fill the database or create a fresh one, you will need pantheon (install with "pip install pantheon"). Then run "analysis.py" by setting REFERENCE_PLAYER to any player who ended a ranked in the current hour. You also need to fill "api_binder.py" with your own Riot API key.

The program will update the database with 50 recent games at each run (this can take a huge while). This limitation is dued to riot API not making it easy to look for game histories before a particular game (in case it is not recent).

# todo

- Run big sample

- Implement simulation

- Implement stats.py




