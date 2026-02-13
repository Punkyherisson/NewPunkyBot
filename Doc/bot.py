# Pour utiliser ce code, vous devez d'abord créer un bot sur le portail des développeurs Discord et obtenir son token.
# Ensuite, vous devez installer les bibliothèques nécessaires en utilisant pip, comme discord.py et python-dotenv.
# Assurez-vous de créer un fichier .env dans le même répertoire que votre script Python
# Ajouter votre token de bot sous la forme DISCORD_TOKEN=your_token_here.
# Une fois que tout est configuré, vous pouvez exécuter le script pour lancer votre bot Discord.
# ici j'ai utilisé la bibliothèque discord.py pour créer un bot Discord simple qui répond à un message spécifique.
# Le bot se connecte à Discord, écoute les messages et répond lorsque on ecrit bonjour dans une channel ou en DM.
#  N'oubliez pas de remplacer 'your_token_here' par le token réel de votre bot dans le fichier .env.
# Vous pouuvez regarder ce tuto pour comprendre comment fonctionne le code : https://www.youtube.com/watch?v=SPTfmiYiuok&t=1s&ab_channel=TechWithTim
import discord
# pour lire le .env et acceder au token du bot
from dotenv import load_dotenv
# pour interagir avec le systeme d'exploitation et acceder aux variables d'environnement
import os


load_dotenv()

bot=discord.Client(intents=discord.Intents.all())
print("on va lancer le bot discord")

# Sans ce decorateur la fonction ne sera pas reconnue par le bot et ne sera pas executée
@bot.event
async def on_ready():
    print(f'{bot.user} est connecte à Discord!')  

@bot.event
async def on_message(message: discord.Message):
    if message.content.lower()=='bonjour':
        author= message.author
        channel= message.channel
        # sans await ca ne s'execute pas
        # ca envoit dans la channel et en dm
        await channel.send('Comment vas tu?')
        await author.send('Salut, comment vas tu?')
    if message.content.lower()=='konnichiwa':
        author= message.author
        channel= message.channel
        japonais_channel_id=bot.get_channel(1384420383205101618)
        await japonais_channel_id.send('Ogenki desu ka?')
        await author.send('Konnichiwa, ogenki desu ka?')

# c'est l'identifiant du channel de test de bot 1384420383205101618



bot_token = os.getenv('DISCORD_TOKEN')
bot.run(bot_token)

print("le bot est mort")

