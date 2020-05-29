# RiotMatchmaking

# Abstract

It's been a while a lot of League of Legends streamers claim matchmaking is rigged. Part of complaining players are convinced matchmaking algorithm imbalances games on purpose.

There might be an interest for Riot to do so, because the probability for a player to start a new game is correlated to his previous results, at every time scale: 

- players losing several games in a row are likely to lower their play time in a near future, while players winning several games in a row are not likely to increase their play time as much.

- players having a bad winrate over a whole season can lose their global motivation to play the game, hence move to another game.

Moreover, playtime is strongly correlated with the money Riot earn (more overall playtime leads to higher game popularity, and both these factors make overall money spending grow). So there might be a capital gain for Riot to try to avoid long lose streaks and very bad overall winrates.

From an entertaining view, it would be pretty bad for League of Legends if the player realised games quality and/or team compositions were purposely imbalanced. The more a player would be doing good, the more likely he would be to play with players doing bad (with all the tilt issues that comes with).

If the matchmaking system was rigged, there would be no way to know which component is responsible. It could be either MMR calculator offering compensations to players with bad results, or team making algorithm imbalancing games on purpose.

This program goal is to get a statistical certainty, by analysing game data to make an unbiased conclusion.

We will study both games composition (standard deviation for average amount of win/lose streak players per game) and teams composition (average team balance).

# Metric description

We needed a metric to quantify how imbalanced a particular game is, considering one binary parameter for each player in a game.

Let b be a binary parameter in {0, 1}.

For any game G and any binary parameter b, we define B(G, b) = B(b), as the number of winning/losing players in game G.

We define a team t as set of players with five or less items (since we don't account for neutral players when using the first parameter described in "# Parameters description" section).

Let t(G, i) = t(i), i in {0, 1} be the two teams in game G, and B(t, b) be the number of winning/losing players in the team t.

In a balanced game from b perspective we ideally expect to have the same amount of winning/losing players in each team.

Now consider the function f1(b, i) = |B(b) - 2 * B(t(i), b)|

It gives us twice the difference between the expected B(t, b) if the game was balanced and the actual amount of B(t, b).

As the differences are symetrical this function also gives the sum for both teams. Furthermore it allows us to only work with integers.

This expression remains biased because if B(b) is an odd value then f1 will return a strictly positive value. Since we want our metric minimum being zero for every scenario, we have to remove bias from f1.

It leads us to function f2(b, i) = f1(b, i) - (B(b) % 2)

We finally have our metric balance_value: balance_value(G) = sum(f2(b, i)), for arbitrary i and every b.

# Parameters description

We define streaks as follow: if last two games were wins/loses, the player is considered in win/lose streak, otherwise he's neutral. We neglect neutral players in our analysis sinced we are only concerned about tendancies on players in win/lose streak. A missing game history will make the corresponding player neutral, since it shouldn't bias our results, but if the program fails to recover more than two game histories, the current game is skipped to avoid having poor data).

Note this streak parameter is unbiased: if matchmaking algorithm is considering streaks over a bigger game history, we may necessarily see some repercussions by only observing the last two games. If matchmaking algorithm was considering other parameters, they may have repercussions on winrate, so on streaks (as a player with winrate > 0.5 will win two games in a row with a probability p > 1/4).

However if Riot is using the biggest game history possible (i.e. season winrate) the game sample needed to see repercussions on the last two games may be very long to compute (see time restrictions on "# How to run" section).

To over come this issue, we could define winrate as a binary parameter representing either a losing player (season winrate < 0.5) or a winning player (season winrate >= 0.5). Note this parameter has not been implemented because of how hard Riot API made it to get player's winrates (only way of doing so is to keep a a local database with every ranked game played this season, or do web scrapping on a similar service). Anyway, the following content describe how we would have managed it.

# Process

1) Observing game sample

As we observe a game we proceed as follow for both our parameters:

- Get b for every player in the game

- Compute and store balance_value(G)

- Store B(b) values

2) Creating reference sample

To make effective interpretations, we implemented a result-independant team making algorithm. Parameters are sampled with the probability distribution of the real games sample.

We run a large number of iterations of our model, proceeding as described in 1).

3) Comparating values

For both our parameters we compute the standard deviation for the B(b) values stored (riot_sd and model_sd for both winning and losing players).

It is important to check if the whole games are imbalanced because it would produce biased results for team making analysis.

We expect riot_sd and model_sd values to be the same, because separating winning and losing players shouldn't have a strong impact on game result.

Then, we compare standard deviations for balance_value(G) values (riot_balance and model_balance). It is also important, because some games could be rigged in the opposite way as expected to compensate for the average values.

Finally, we compare average values on both samples for our two parameters.

# Interpretations

We consider what a big imbalance would have been to make unbiased interpretations.

Following interpretations are the same for both parameters:

If riot_balance is much greater than model_balance: team making is rigged. Winning players are more likely to play in the same team, and against losing players (and reciprocally).
We don't expect to see this result since it would produce the opposite effect to the one described in abstract.

If riot_balance is equal to model_balance: team making is not result-dependant. Complaining players would have been misled because of human brain variance perception.

If riot_balance is much lower than model_balance: team making is rigged and balances winning and losing players over teams. Winning players are more likely to play with losing players (and reciprocally).
This is the result complaining players can expect.

# Results

As mentioned in "# Parameters desciption" section, the results presented only concern the streak parameter.

In practice a balanced game produces a balance_value of 0, and a strongly imbalanced game produces a balance_value greater than 4.

For the firsts 200 games (relatively small sample, even if it already took more than 6 hours to compute), standards deviations over games are relatively close (1.6/1.4 for win streaks, 1.5/1.3 for lose streaks).
Average riot_balance is 2.6 while average model_balance is 2.9. It is likely that Riot matchmaking is result-independant. 

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






