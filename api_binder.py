from pantheon import pantheon
import asyncio


LOGS = True
server = "euw1"
api_key = "RGAPI-2ca4b71c-de28-489c-af4b-fc45f6cb9ace"


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
        print(e)


async def getRecentMatchlist(maccountId, n):
    try:
        data = await panth.getMatchlist(maccountId, params={"endIndex": n})
        return data
    except Exception as e:
        print(e)


async def getRecentMatches(maccountId, n):
    try:
        matchlist = await getRecentMatchlist(maccountId, n)
        tasks = [panth.getMatch(match['gameId']) for match in matchlist['matches']]
        return await asyncio.gather(*tasks)
    except Exception as e:
        print(e)


def get_matches(accountid, n):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(getRecentMatches(accountid, n))


def get_match(matchId):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(getMatch(matchId))


def get_outcome(accountid, game):
    for part in range(10):
        if game['participantIdentities'][part]['player']['accountId'] == accountid:
            return game['participants'][part]['stats']['win']


def get_recent_match(playername):
    loop = asyncio.get_event_loop()
    (summonerId, accountId) = loop.run_until_complete(getSummonerId(playername))
    match = loop.run_until_complete(getRecentMatches(accountId, 1))[0]
    return match