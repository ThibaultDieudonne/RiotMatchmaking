from pantheon import pantheon
import asyncio


api_key = "RGAPI-40b2254a-682a-44a5-90bc-4fd30e880c23"
LOGS = False  # turn to True in case nothing is shown for more than 2 minutes
server = "euw1"  # don't touch


def requestsLog(url, status, headers):
    if LOGS:
        print(url)
        print(status)
        print(headers)


panth = pantheon.Pantheon(server, api_key, errorHandling=True, requestsLoggingFunction=requestsLog, debug=LOGS)


async def getSummonerId(mname):
    try:
        data = await panth.getSummonerByName(mname)
        return data['id'], data['accountId']
    except Exception as e:
        print(str(e) + " in getSummonerId")


async def getRecentMatchlist(maccountId, n):
    try:
        data = await panth.getMatchlist(maccountId, params={"queueId": 420, "endIndex": n})
        return data
    except Exception as e:
        print(e)


async def getRecentMatches(maccountId, n):
    try:
        matchlist = await getRecentMatchlist(maccountId, n)
        tasks = [panth.getMatch(match['gameId']) for match in matchlist['matches']]
        return await asyncio.gather(*tasks)
    except:
        print("Unable to get a match history from Riot API")


def get_matches(accountid, n):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(getRecentMatches(accountid, n))


def get_match(matchId):
    try:
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(panth.getMatch(matchId))
    except:
        return -1


def get_outcome(accountid, game):
    for part in range(10):
        if game['participantIdentities'][part]['player']['accountId'] == accountid:
            return game['participants'][part]['stats']['win']

