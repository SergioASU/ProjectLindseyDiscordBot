#Project Lindsey Discord Bot Alpha v 1.3
#Author: Sergio Corral

import discord
import asyncio
import sys, traceback
import requests
import random
import praw
import os

#Get codes via text files. Sensitive informaiton so not shown to public
riotAPIFile = open(os.path.join(os.pardir, "RiotAPI.txt"), "r")
redditClientIdFile = open(os.path.join(os.pardir, "RedditClientID.txt"), "r")
redditClientSecretFile = open(os.path.join(os.pardir, "RedditClientSecret.txt"), "r") 
redditUserAgentFile = open(os.path.join(os.pardir, "RedditUserAgent.txt"), "r")
discordCodeFile = open(os.path.join(os.pardir, "DiscordCode.txt"), "r")

APIKey = riotAPIFile.readline()
redditClientID = redditClientIdFile.readline()
redditClientSecret = redditClientSecretFile.readline()
redditUserAgent = redditUserAgentFile.readline()
discordCode = discordCodeFile.readline()

listOfStuff = []

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event 
async def on_message(message):
    if message.content.startswith('!dismiss'):
        await client.send_message(message.channel, 'Thank you master. Goodbye')
        client.logout()
        sys.exit(0)

    elif message.content.startswith('!rank'):
        summonerName = message.content[6:]
        summonerName = summonerName.lower()
        initialResponse = requests.get("https://na.api.pvp.net/api/lol/na/v1.4/summoner/by-name/" + summonerName + "?api_key=" + APIKey)
        data = initialResponse.json()
        summonerID = str(data[summonerName]['id'])
        print(summonerID)
        rankedRequest = requests.get("https://na1.api.riotgames.com/lol/league/v3/positions/by-summoner/" + summonerID + "?api_key=" + APIKey)
        rankedData = rankedRequest.json()
        print(rankedData)
        leagueName = rankedData[0]['leagueName']
        tier = rankedData[0]['tier']
        queueType = rankedData[0]['queueType']
        rank = str(rankedData[0]['rank'])
        leaguePoints = str(rankedData[0]['leaguePoints'])
        wins = str(rankedData[0]['wins'])
        losses = str(rankedData[0]['losses'])
        name = rankedData[0]['playerOrTeamName']

        discordResponse = name + " is in " + tier + " " + rank + " " + leaguePoints + "lp " + "with " + wins + " wins and " + losses + " losses"
        await client.send_message(message.channel,discordResponse)

    elif message.content.startswith('!themes'):
        textFile = open("leagueThemes.txt", "r")
        messageToSend = ""

        while True:
            line = textFile.readline()
            if not line: break
            
            lastSpaceIndex = 0
            index = 0
            for letter in line:

                if (letter == ' '):
                    lastSpaceIndex = index
                index += 1
            theme = line[0:lastSpaceIndex]
            numberOfSkins = int(line[lastSpaceIndex:])
            entry = []
            entry.append(theme)
            print(theme)
            print(numberOfSkins)
            messageToSend += theme + "\n"
            for i in range(0,numberOfSkins):
                getRidOf = textFile.readline()
                entry.append(getRidOf)

            listOfStuff.append(entry)
        print(messageToSend)
        print(listOfStuff)
        await client.send_message(message.channel,messageToSend)

    elif message.content.startswith('!randomtheme'):

        textFile = open("leagueThemes.txt", "r")
        messageToSend = ""

        while True:
            line = textFile.readline()
            if not line: break

            lastSpaceIndex = 0
            index = 0
            for letter in line:

                if (letter == ' '):
                    lastSpaceIndex = index
                index += 1
            theme = line[0:lastSpaceIndex]
            numberOfSkins = int(line[lastSpaceIndex:])
            entry = []
            entry.append(theme)
            print(theme)
            print(numberOfSkins)
            messageToSend += theme + "\n"
            for i in range(0,numberOfSkins):
                getRidOf = textFile.readline()
                entry.append(getRidOf.rstrip())

            listOfStuff.append(entry)
        print(messageToSend)
        print(listOfStuff)

        lengthOfList = len(listOfStuff)
        randomNumber = random.randint(0,lengthOfList)

        print(listOfStuff[randomNumber])

        randomTheme = ""
        for thing in listOfStuff[randomNumber]:
            randomTheme += (thing + "\n")
        await client.send_message(message.channel,randomTheme)

    elif message.content.startswith('!meme'):
       
        reddit = praw.Reddit(client_id = redditClientID, client_secret= redditClientSecret,user_agent= redditUserAgent)
        
        subreddit = reddit.subreddit('me_irl')

        memeList = []

        randomNumber = random.randint(0,200)
        index = 0
        messageToSend = ""
        for submission in subreddit.hot(limit=200):
            if(randomNumber == index):
                messageToSend = submission.url
                break
            index += 1
        await client.send_message(message.channel,messageToSend)

client.run(discordCode)

