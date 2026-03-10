import os
from datetime import datetime, timezone, timedelta
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from zoneinfo import ZoneInfo

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

SERVER_ID = 1341756314967085096  # remplace par l’ID de ton serveur

VOICE_CHANNEL_ID = 1341756315487436830
Lounge = 1341756315487436830
SalleEtude = 1341756315877376072

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)
        self.PARIS_TZ = ZoneInfo("Europe/Paris")
        self.EMOJI_MATIERE = {
            "python": "🐍",
            "japonais": "🇯🇵",
        }

    async def setup_hook(self):
        # Sync des slash commands pour la guilde (plus rapide que global) [web:3][web:14]
        GUILD_ID = 1341756314969815060  # remplace par l’ID de ton serveur
        guild = discord.Object(id=GUILD_ID)
        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)

bot = MyBot()

PARIS_TZ = ZoneInfo("Europe/Paris")
EMOJI_MATIERE = bot.EMOJI_MATIERE

# ----- Slash command ProchainCours -----
class ProchainCoursModal(discord.ui.Modal, title="Planifier un cours"):
    date = discord.ui.TextInput(
        label="Date (YYYY-MM-DD)",
        placeholder="2026-03-15",
        required=True,
    )
    heure = discord.ui.TextInput(
        label="Heure (HH:MM)",
        placeholder="15:00",
        required=True,
    )
    prof = discord.ui.TextInput(
        label="Professeur",
        placeholder="Aless",
        required=True,
    )

    def __init__(self, matiere: str, format_str: str, interaction: discord.Interaction):
        super().__init__()
        self.matiere = matiere
        self.format_str = format_str
        self.interaction = interaction

    async def on_submit(self, interaction: discord.Interaction):
        matiere_norm = self.matiere.lower()
        format_norm = self.format_str.lower()

        emoji = EMOJI_MATIERE.get(matiere_norm, "📚")

        try:
            dt_naive = datetime.strptime(
                f"{self.date.value} {self.heure.value}", "%Y-%m-%d %H:%M"
            )
            dt_paris = dt_naive.replace(tzinfo=PARIS_TZ)
            dt_utc = dt_paris.astimezone(timezone.utc)
        except ValueError:
            await interaction.response.send_message(
                "❌ Format de date/heure invalide. Attendu : `YYYY-MM-DD` et `HH:MM`.",
                ephemeral=True,
            )
            return

        name = f"{emoji} {self.matiere} avec {self.prof.value}"

        try:
            if format_norm == "présentiel" or format_norm == "presenciel":
                channel = interaction.guild.get_channel(VOICE_CHANNEL_ID)
                if not channel or not isinstance(channel, discord.VoiceChannel):
                    await interaction.response.send_message(
                        "❌ Salon vocal non trouvé, vérifie VOICE_CHANNEL_ID.",
                        ephemeral=True,
                    )
                    return

                event = await interaction.guild.create_scheduled_event(
                    name=name,
                    description=(
                        f"Cours de {self.matiere} avec {self.prof.value} "
                        f"({self.format_str}). Créé par {interaction.user.display_name}."
                    ),
                    start_time=dt_utc,
                    end_time=None,
                    privacy_level=discord.PrivacyLevel.guild_only,
                    entity_type=discord.EntityType.voice,
                    channel=channel,
                )
            else:
                event = await interaction.guild.create_scheduled_event(
                    name=name,
                    description=(
                        f"Cours de {self.matiere} avec {self.prof.value} "
                        f"({self.format_str}). Créé par {interaction.user.display_name}."
                    ),
                    start_time=dt_utc,
                    end_time=dt_utc + timedelta(hours=2),
                    privacy_level=discord.PrivacyLevel.guild_only,
                    entity_type=discord.EntityType.external,
                    location="En ligne",
                )
        except discord.Forbidden:
            await interaction.response.send_message(
                "❌ Permissions manquantes pour créer un événement.",
                ephemeral=True,
            )
            return
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Erreur création : `{e}`", ephemeral=True
            )
            return

        await interaction.response.send_message(
            f"✅ Événement créé : **{event.name}** (ID: `{event.id}`)\n"
            f"📅 Début (heure de Paris) : `{dt_paris:%Y-%m-%d %H:%M}`\n"
            f"🔗 Lien : {event.url}\n"
            f"ℹ️ Pour l'annuler : `/annulercours` avec l'ID",
            ephemeral=False,
        )

class CoursView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)
        self.matiere = None
        self.format_str = None

    @discord.ui.select(
        placeholder="Choisis la matière",
        min_values=1,
        max_values=1,
        options=[
            discord.SelectOption(label="Python", value="python", emoji="🐍"),
            discord.SelectOption(label="Japonais", value="japonais", emoji="🇯🇵"),
        ],
    )
    async def select_matiere(
        self, select: discord.ui.Select, interaction: discord.Interaction
    ):
        self.matiere = select.values[0]
        await interaction.response.defer()
        # Rien à envoyer tout de suite, on attend le format

    @discord.ui.select(
        placeholder="Présentiel ou Distanciel",
        min_values=1,
        max_values=1,
        options=[
            discord.SelectOption(label="Présentiel", value="Presenciel"),
            discord.SelectOption(label="Distanciel", value="Distanciel"),
        ],
    )
    async def select_format(
        self, select: discord.ui.Select, interaction: discord.Interaction
    ):
        self.format_str = select.values[0]
        if not self.matiere:
            await interaction.response.send_message(
                "Choisis d'abord une matière.", ephemeral=True
            )
            return

        modal = ProchainCoursModal(self.matiere, self.format_str, interaction)
        await interaction.response.send_modal(modal)

@bot.tree.command(name="prochaincours", description="Créer un cours (événement Discord)")
async def prochaincours(interaction: discord.Interaction):
    view = CoursView()
    await interaction.response.send_message(
        "Configure ton prochain cours :", view=view, ephemeral=True
    )

# ----- Slash command AnnulerCours -----
@bot.tree.command(name="annulercours", description="Annuler un cours (événement) par ID")
@app_commands.describe(event_id="ID de l'événement à annuler")
async def annulercours(interaction: discord.Interaction, event_id: str):
    try:
        event_id_int = int(event_id)
    except ValueError:
        await interaction.response.send_message(
            "❌ L'ID doit être un nombre.", ephemeral=True
        )
        return

    try:
        event = await interaction.guild.fetch_scheduled_event(event_id_int)
    except discord.NotFound:
        await interaction.response.send_message(
            f"❌ Aucun événement trouvé avec l'ID `{event_id}`.", ephemeral=True
        )
        return
    except discord.Forbidden:
        await interaction.response.send_message(
            "❌ Je n'ai pas la permission de voir les événements programmés.",
            ephemeral=True,
        )
        return
    except Exception as e:
        await interaction.response.send_message(
            f"❌ Erreur en récupérant l'événement : `{e}`", ephemeral=True
        )
        return

    try:
        await event.delete()
    except discord.Forbidden:
        await interaction.response.send_message(
            "❌ Je n'ai pas la permission de supprimer cet événement.",
            ephemeral=True,
        )
        return
    except Exception as e:
        await interaction.response.send_message(
            f"❌ Erreur en supprimant l'événement : `{e}`", ephemeral=True
        )
        return

    await interaction.response.send_message(
        f"✅ Événement `{event.name}` (ID: `{event_id}`) annulé.",
        ephemeral=False,
    )

# ----- Réponses basiques (messages texte) -----
@bot.event
async def on_message(message: discord.Message):
    await bot.process_commands(message)
    if message.author == bot.user:
        return

    if message.content.lower() == "bonjour":
        await message.channel.send("Comment vas-tu ?")
        await message.author.send("Salut, comment vas-tu ?")

    if message.content.lower() == "konnichiwa":
        await message.channel.send("Konnichiwa, ogenki desu ka ?")
        await message.author.send("Konnichiwa, ogenki desu ka ?")

@bot.event
async def on_ready():
    print(f"{bot.user} est connecté à Discord !")

if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN manquant dans .env")

print("On va lancer le bot Discord...")
bot.run(TOKEN)
print("Le bot est mort.")