from pantheon import pantheon
import asyncio
import json
import pickle


server = "euw1"
api_key = "RGAPI-591df5d2-9d77-4d90-a325-4f6958105052"


def requestsLog(url, status, headers):
    print(url)
    print(status)
    print(headers)


panth = pantheon.Pantheon(server, api_key, errorHandling=True, requestsLoggingFunction=requestsLog, debug=True)


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


async def getChallengerNames():
    try:
        data = await panth.getChallengerLeague()
        return data
    except Exception as e:
        print(e)


def save_names():
    print('Getting challenger names')
    chall_names = []
    loop = asyncio.get_event_loop()
    data = loop.run_until_complete(getChallengerNames())
    for chall in data['entries']:
        chall_names.append(chall['summonerName'])
    with open('challenger_names.txt', 'ab') as file:
        pickle.dump(chall_names, file)


def load_names():
    with open('challenger_names.txt', 'rb') as file:
        chall_names = pickle.load(file)
    save_recent_matches(chall_names[0])


def save_recent_matches(name):
    loop = asyncio.get_event_loop()
    (summonerId, accountId) = loop.run_until_complete(getSummonerId(name))
    matches = loop.run_until_complete(getRecentMatches(accountId, 1))
    with open('data.txt', 'ab') as file:
        pickle.dump(matches, file)
    print(matches)


def getStreak(name, matchid):
    doable = True
    # get X lasts games
    # for i in X - 2:
    # if id == matchid:
    # assign streak depending on neext two matches
    # else doable = False


load_names()
# matches[x]['participants']['stats']['win']
# matches[x]['participantIdentities'][y]['player']['summonerName']

