import os
from datetime import datetime, timezone, timedelta
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from zoneinfo import ZoneInfo

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = 1341756314969815060  # Remplace par TON ID serveur
VOICE_CHANNEL_ID = 1341756315487436830  # Lounge

# Bot avec tree pour slash
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

PARIS_TZ = ZoneInfo("Europe/Paris")
EMOJI_MATIERE = {"python": "🐍", "japonais": "🇯🇵"}

@bot.event
async def setup_hook():
    # Sync slash pour TON serveur seulement (instantané)
    guild = discord.Object(id=GUILD_ID)
    bot.tree.copy_global_to(guild=guild)
    synced = await bot.tree.sync(guild=guild)
    print(f"Synced {len(synced)} slash commands pour {bot.user}")

@bot.event
async def on_ready():
    print(f"{bot.user} connecté ! Slash dispo sur le serveur.")

# ----- 1. SLASH COMMAND SIMPLE -----
@bot.tree.command(name="ping", description="Test du bot")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong ! 🏓", ephemeral=True)

# ----- 2. SLASH AVEC PARAMS -----
@bot.tree.command(name="add", description="Additionne 2 nombres")
@app_commands.describe(a="Premier nombre", b="Deuxième nombre")
async def add(interaction: discord.Interaction, a: int, b: int):
    await interaction.response.send_message(f"{a} + {b} = **{a+b}**")

# ----- 3. MODAL (formulaire popup) -----
class TestModal(discord.ui.Modal, title="Test Modal"):
    mon_texte = discord.ui.TextInput(
        label="Écris quelque chose",
        placeholder="Bonjour...",
        max_length=200,
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"Tu as écrit : **{self.mon_texte.value}**",
            ephemeral=True
        )

@bot.tree.command(name="modal", description="Ouvre un formulaire")
async def modal(interaction: discord.Interaction):
    await interaction.response.send_modal(TestModal())

# ----- 4. VIEW + BUTTONS -----
class ButtonsView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)

    @discord.ui.button(label="Clique moi !", style=discord.ButtonStyle.primary)
    async def button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Clic détecté !", ephemeral=True)

@bot.tree.command(name="buttons", description="Test boutons")
async def buttons(interaction: discord.Interaction):
    view = ButtonsView()
    await interaction.response.send_message("Clique les boutons :", view=view, ephemeral=True)

# ----- 5. VIEW + SELECT MENU -----
class SelectView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)

    @discord.ui.select(
        placeholder="Choisis une option",
        options=[
            discord.SelectOption(label="Option 1", value="1"),
            discord.SelectOption(label="Option 2", value="2", emoji="👍"),
            discord.SelectOption(label="Option 3", value="3"),
        ]
    )
    async def select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        await interaction.response.send_message(
            f"Tu as choisi : **{select.values[0]}**", ephemeral=True
        )

@bot.tree.command(name="select", description="Test menu déroulant")
async def select(interaction: discord.Interaction):
    view = SelectView()
    await interaction.response.send_message("Choisis :", view=view, ephemeral=True)

# ----- 6. TON COURS COMPLET (slash + view + modal) -----
class CoursModal(discord.ui.Modal, title="Planifier cours"):
    date = discord.ui.TextInput(label="Date (YYYY-MM-DD)", placeholder="2026-03-15")
    heure = discord.ui.TextInput(label="Heure (HH:MM)", placeholder="15:00")
    prof = discord.ui.TextInput(label="Prof", placeholder="Aless")

    def __init__(self, matiere, format_cours, interaction):
        super().__init__()
        self.matiere = matiere
        self.format_cours = format_cours
        self.interaction = interaction

    async def on_submit(self, interaction: discord.Interaction):
        try:
            dt_naive = datetime.strptime(f"{self.date} {self.heure}", "%Y-%m-%d %H:%M")
            dt_paris = dt_naive.replace(tzinfo=PARIS_TZ)
            dt_utc = dt_paris.astimezone(timezone.utc)
        except ValueError:
            await interaction.response.send_message("❌ Format date/heure invalide !", ephemeral=True)
            return

        emoji = EMOJI_MATIERE.get(self.matiere.lower(), "📚")
        name = f"{emoji} {self.matiere} - {self.prof.value}"

        channel = interaction.guild.get_channel(VOICE_CHANNEL_ID)
        try:
            if "présentiel" in self.format_cours.lower():
                event = await interaction.guild.create_scheduled_event(
                    name=name,
                    start_time=dt_utc,
                    end_time=None,
                    privacy_level=2,  # guild_only
                    entity_type=3,  # voice
                    channel=channel
                )
            else:
                event = await interaction.guild.create_scheduled_event(
                    name=name,
                    start_time=dt_utc,
                    end_time=dt_utc + timedelta(hours=2),
                    privacy_level=2,
                    entity_type=2,  # external
                    location="En ligne"
                )
            await interaction.response.send_message(
                f"✅ **{event.name}** créé !\n📅 {dt_paris:%Y-%m-%d %H:%M}\n🔗 {event.url}"
            )
        except Exception as e:
            await interaction.response.send_message(f"❌ Erreur : {e}", ephemeral=True)

class CoursView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=120)
        self.matiere = None
        self.format_cours = None

    @discord.ui.select(placeholder="Matière", options=[
        discord.SelectOption(label="Python", value="python", emoji="🐍"),
        discord.SelectOption(label="Japonais", value="japonais", emoji="🇯🇵")
    ])
    async def select_matiere(self, i: discord.Interaction, select: discord.ui.Select):
        self.matiere = select.values[0]
        await i.response.defer()

    @discord.ui.select(placeholder="Format", options=[
        discord.SelectOption(label="Présentiel", value="Présentiel"),
        discord.SelectOption(label="Distanciel", value="Distanciel")
    ])
    async def select_format(self, i: discord.Interaction, select: discord.ui.Select):
        self.format_cours = select.values[0]
        if not self.matiere:
            await i.response.send_message("👆 Choisis d'abord la matière !", ephemeral=True)
            return
        modal = CoursModal(self.matiere, self.format_cours, i)
        await i.response.send_modal(modal)

@bot.tree.command(name="prochaincours", description="Planifie un cours")
async def prochain_cours(interaction: discord.Interaction):
    view = CoursView()
    await interaction.response.send_message("**Planifie ton cours :**", view=view, ephemeral=True)

# ----- Messages texte (bonus) -----
@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author == bot.user:
        return
    if "bonjour" in message.content.lower():
        await message.reply("Bonjour ! 😊")
    await bot.process_commands(message)  # IMPORTANT après custom logic

if __name__ == "__main__":
    if not TOKEN:
        print("❌ DISCORD_TOKEN manquant dans .env")
    else:
        bot.run(TOKEN)
