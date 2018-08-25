# Work with Python 3.6
import discord
import requests
import json

TOKEN = 'NDgzMDIzNzA4MDI2NTY4NzA0.DmNmsQ.XwADZhbxNb3XGNeoG6PvIH4d8hw'
url = "https://api.royaleapi.com/clan/2UOQ98J8"


headers = {
    'auth': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTU2NSwiaWRlbiI6IjI2NzY4MTcxOTUzOTIwNDA5NyIsIm1kIjp7fSwidHMiOjE1MzUyMzc5MjI0NTl9.CJp7Ezu6ylH7FMZBB2EoeLidD5ZB983ZvKSC5LXBVbg"
    }

client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)
    elif message.content.startswith('!test'):
        response = requests.request("GET", url, headers=headers)
        data = response.json()
        msg = data['name'].format(message)
        await client.send_message(message.channel, msg)

@client.event
async def on_ready():
    print('Logged in as '+ client.user.name +' (ID: '+ client.user.id + ')')
    print('---------------------------')

client.run(TOKEN)
