import discord
from dotenv import load_dotenv
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
    if message.content=='bonjour':
        channel= message.channel
        # sans await ca ne s'execute pas
        await channel.send('Comment vas tu?')



bot_token = os.getenv('DISCORD_TOKEN')
bot.run(bot_token)

print("le bot est mort")

