# RiotMatchmaking

# Abstract

It's been a while a lot of League of Legends streamers claim matchmaking is rigged. Complaining players are convinced matchmaking algorithm controls players streaks to maximize their play time based on learning algorithm.
This program goal is to get a statistical certainty on this question, by analysing game data to determine whether or not the algorithm is streak dependant (as games MMR are obviously not imbalanced).
We will both study games composition (over mates and opponents) and teams composition (mates only).

# Process

We define streaks as follow: if last two games were wins/loses, the player is in win/lose streak, otherwise he's neutral.
Note this metric is unbiased: if matchmaking algorithm is considering streaks over more game history, we would necessarily see some repercussions by only observing last two games.
As we observe a game we get every player's current streak. We compute a "riot_imbalance" value, proportionnal to team imbalance from a streak perspective.

We can compare riot_imbalance average for a large game sample with the same "imbalance" comcept applied to a streak-independant team making algorithm respecting the amount of win streaks, lose streaks and neutrals. In pratice we can just create a large amount of "fake lobbies" by sampling players' streaks with according probabilities.
If riot_imbalance is much greater than streak independant then Riot is definitely rigging team making to control player's streaks.
If the values are close Riot team making might not be rigged.
If riot_imbalance is much lower, it means that Riot team making is streak dependant, but it tends to balance winning/losing players over teams.

We can compute standard deviation for each streak count, for real games and fake lobbies and compare value.
Again, if riot's values are higher, then it would be a proof that game compositions are streak dependant.

# Results

To be published.



