# Work with Python 3.6
import discord
import requests
import json

TOKEN = 'NDgzMDIzNzA4MDI2NTY4NzA0.DmNmsQ.XwADZhbxNb3XGNeoG6PvIH4d8hw'
urlClan = "https://api.royaleapi.com/clan/"
urlJoueur = "https://api.royaleapi.com/player/"
CLAN_DEFAUT='2UOQ98J8'

headers = {
    'auth': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTU2NSwiaWRlbiI6IjI2NzY4MTcxOTUzOTIwNDA5NyIsIm1kIjp7fSwidHMiOjE1MzUyMzc5MjI0NTl9.CJp7Ezu6ylH7FMZBB2EoeLidD5ZB983ZvKSC5LXBVbg"
    }

client = discord.Client()

# fonctions utilitaires
def suiviClan(data):
    msg = ""
    msg += "Tag: "           + data['tag']         + "\n"
    msg += "Description: "   + data['description'] + "\n"
    msg += "Score du clan: " + str(data['score'])       + "\n"
    msg += "Membres: "       + str(data["memberCount"]) + "/50\n\n"
    # top 5
    msg += "----- Top 5 des membres: -----\n"
    for i in range(0,5):
        membre = data['members'][i]
        msg += "    #" + str(i+1) + " " + membre['name'] + " ("+ str(membre['tag']) + ") avec " + str(membre['trophies']) + " trophés.\n"
    return msg

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
    
    # ne répond qu'aux messages privés
    if isinstance(message.channel, discord.channel.PrivateChannel) == False:
        print('Message ignoré')
        return

    msg=""
    # commande !clan [tag]
    if message.content.startswith('!clan'):
        tab = message.content.split()
        length = len(tab)
        if length == 1: # pas d'argument
            response = requests.request("GET", urlClan+CLAN_DEFAUT, headers=headers)
            data = response.json()
            msg += suiviClan(data)
        elif length == 2: # 1 argument
            response = requests.request("GET", urlClan+tab[1], headers=headers)
            if response.status_code == 200:
                data = response.json()
                msg += suiviClan(data)
            else:
                msg += "Clan non trouvé (tag non existant)\n"
        else: # trop d'argument
            msg += "usage: `!clan [tag]`\n"
    else:
        msg = 'Désolé, je ne parle pas encoe le gobelin.'
    # envoi
    msg = msg.format(message)
    await client.send_message(message.channel, msg)

@client.event
async def on_ready():
    print('Logged in as '+ client.user.name +' (ID: '+ client.user.id + ')')
    print('---------------------------')

client.run(TOKEN)