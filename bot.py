# Pour utiliser ce code, vous devez d'abord créer un bot sur le portail des développeurs Discord et obtenir son token.
# Ensuite, vous devez installer les bibliothèques nécessaires : pip install discord.py python-dotenv
# Créez un fichier .env avec : DISCORD_TOKEN=your_token_here
# Le bot répond à "bonjour"/"konnichiwa" et gère les commandes !ProchainCours et !AnnulerCours pour les événements.

import os
from datetime import datetime, timezone, timedelta
import discord
from discord.ext import commands
from dotenv import load_dotenv
from zoneinfo import ZoneInfo  # ← NOUVEAU

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Bot à commandes (préfixe !)
bot = commands.Bot(command_prefix="!", intents=intents)

# Mapping matière → emoji
EMOJI_MATIERE = {
    "python": "🐍",
    "japonais": "🇯🇵",
}

# Offset Paris (UTC+1 hiver ; +2 été : change manuellement si besoin)
# PARIS_OFFSET = timedelta(hours=1)
# AJOUTE ÇA À LA PLACE
PARIS_TZ = ZoneInfo("Europe/Paris")  # ← NOUVEAU

@bot.event
async def on_ready():
    print(f"{bot.user} est connecté à Discord !")

# ---------- Commande !ProchainCours ----------
@bot.command(name="ProchainCours")
async def prochain_cours(
    ctx: commands.Context,
    matiere: str,
    date_str: str,
    heure_str: str,
    format_str: str,
    prof: str,
):
    """
    !ProchainCours Python 2026-02-14 15:00 Distanciel Aless
    Crée un événement de cours sur le serveur.
    """
    # Normaliser les entrées
    matiere_norm = matiere.lower()
    format_norm = format_str.lower()

    # Vérif matière
    emoji = EMOJI_MATIERE.get(matiere_norm, "📚")

    # Vérif format
    if format_norm not in ("presenciel", "distanciel"):
        await ctx.send(
            "❌ Format invalide. Utilise soit `Presenciel` soit `Distanciel`.\n"
            "Exemple : `!ProchainCours Python 2026-02-14 15:00 Distanciel Aless`"
        )
        return

    # Parsing date / heure (heure locale Paris → UTC)
    """ try:
        dt_paris = datetime.strptime(f"{date_str} {heure_str}", "%Y-%m-%d %H:%M")
        dt_utc = dt_paris.replace(tzinfo=timezone.utc) - PARIS_OFFSET  # Paris → UTC
    except ValueError: """

    # Parsing date / heure (heure locale Paris → UTC)
    try:
        dt_naive = datetime.strptime(f"{date_str} {heure_str}", "%Y-%m-%d %H:%M")
        dt_paris = dt_naive.replace(tzinfo=PARIS_TZ)  # ← Paris time
        dt_utc = dt_paris.astimezone(timezone.utc)    # ← Convert to UTC
    except ValueError:
        await ctx.send(
            "❌ Format de date/heure invalide.\n"
            "Attendu : `YYYY-MM-DD HH:MM` (ex: `2026-02-14 15:00`).\n"
            "Tu as peut-être mis `14/02/2026` au lieu de `2026-02-14`."
        )
        return

    # Construire le nom de l'événement
    name = f"{emoji} {matiere} avec {prof}"

    # Params spécifiques au format ✅ FIXÉ
    channel = None
    location = None
    if format_norm == "presenciel":
        entity_type = discord.EntityType.voice
        channel = ctx.channel  # Channel actuel pour présentiel
    else:  # distanceliel → EXTERNAL (channel=None obligatoire)
        entity_type = discord.EntityType.external
        location = "En ligne"

    try:
        event = await ctx.guild.create_scheduled_event(
            name=name,
            description=f"Cours de {matiere} avec {prof} ({format_str}). Créé par {ctx.author.display_name}.",
            start_time=dt_utc,
            end_time=None,
            privacy_level=discord.PrivacyLevel.guild_only,
            entity_type=entity_type,
            channel=channel,  # None pour distanceliel
            location=location,
        )
    except discord.Forbidden:
        await ctx.send(
            "❌ Permissions manquantes :\n"
            "- **Créer/Gérer événements** (serveur)\n"
            "- Présentiel : **View Channel** sur ce channel"
        )
        return
    except Exception as e:
        await ctx.send(f"❌ Erreur création : `{e}`")
        return

    await ctx.send(
        f"✅ Événement créé : **{event.name}** (ID: `{event.id}`)\n"
        f"📅 Début (heure de Paris) : `{dt_paris:%Y-%m-%d %H:%M}`\n"
        f"🔗 Lien : {event.url}\n"
        f"ℹ️ Pour l'annuler : `!AnnulerCours {event.id}`\n"

    )

# ---------- Commande !AnnulerCours ----------
@bot.command(name="AnnulerCours")
async def annuler_cours(ctx: commands.Context, event_id: int):
    """
    !AnnulerCours 123456789012345678
    Supprime un événement programmé par ID.
    """
    try:
        event = await ctx.guild.fetch_scheduled_event(event_id)
    except discord.NotFound:
        await ctx.send(f"❌ Aucun événement trouvé avec l'ID `{event_id}`.")
        return
    except discord.Forbidden:
        await ctx.send("❌ Je n'ai pas la permission de voir les événements programmés.")
        return
    except Exception as e:
        await ctx.send(f"❌ Erreur en récupérant l'événement : `{e}`")
        return

    try:
        await event.delete()
    except discord.Forbidden:
        await ctx.send("❌ Je n'ai pas la permission de supprimer cet événement.")
        return
    except Exception as e:
        await ctx.send(f"❌ Erreur en supprimant l'événement : `{e}`")
        return

    await ctx.send(f"✅ Événement `{event.name}` (ID: `{event_id}`) annulé.")

# ---------- Réponses basiques ----------
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

if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN manquant dans .env")

print("On va lancer le bot Discord...")
bot.run(TOKEN)
print("Le bot est mort.")