# NewPunkyBot

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![discord.py](https://img.shields.io/badge/discord.py-v2.4%2B-5865F2.svg?logo=discord&logoColor=white)](https://discordpy.readthedocs.io/)
[![Status](https://img.shields.io/badge/Status-WIP-orange.svg)]
[![Issues](https://img.shields.io/github/issues/Punkyherisson/NewPunkyBot?logo=github)](https://github.com/Punkyherisson/NewPunkyBot/issues)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Bot Discord modulaire pour apprendre Python**  
**Multi-bots spécialisés** : organisation, modération, jeux, langues.  
**Auteur** : Emmanuel (Punkyherisson) | **Serveur cible** : Punkyherisson + multi-serveurs

## 🎯 Objectifs

NewPunkyBot est un **projet d'apprentissage Python concret** via bots Discord modulaires.  
**Approche multi-bots** : 1 bot = 1 mission (débutant-friendly, sur plusieurs mois).

**Priorités :**
- Progresser Python (discord.py, parsing, APIs)
- Multi-serveurs (Punkyherisson principal)
- Démarche agile : v0.1 simple → v1.0 complète
- Sécurité : pouvoirs < admin

## 🚀 Fonctionnalités (Spécifications v0.3)

### **Bot 1 : Organisation (v0.1 Priorité IMMÉDIATE)**
!ProchainCours Python 2026-02-14 14:00 Presenciel Aless
→ Crée événement Discord 🐍 + Aless/toi

!ProchainDevoir Japonais "Leçon 12 Minna" [lien]
→ Événement devoir + 🇯🇵

text

### 🛡️ **Bot 2 : Modération (v0.2)**
- Avertir/mute/kick/ban auto
- Filtrage injurieux/spam
- Logs quotidiens
- Niveaux utilisateurs (permissions/expertise)

### 🎮 **Bot 3 : Social/Jeux (v1.0)**
- Trivia, pendu, RPG texte
- XP anti-procrastination
- Spotify, traductions (anglais/allemand/espagnol/japonais)
- Yoga/krav maga/méditation

### 📅 **Bot 4 : Productivité/Intégrations (v1.0+)**
- GitHub push/issues/PR
- Météo Lyon (ski)
- Conversationnel langues (Talkpal-style)

## 📋 Roadmap Multi-bots

| Version | Bot | Statut | Features clés |
|---------|-----|--------|---------------|
| **v0.1** | Organisation | ⏳ TODO | `!ProchainCours`, `!ProchainDevoir` |
| **v0.2** | Modération | ⏳ Plan | `!kick`, `!mute`, logs |
| **v0.3** | Social | 🔄 Plan | Jeux, XP, Spotify |
| **v1.0** | Intégrations | 🔮 Futur | GitHub, météo, chat langues |

## 🗂️ Arborescence Répertoires (v0.3)

NewPunkyBot/ (Repo parent)
├── bot-organisation/ # v0.1 PRIORITÉ
│ ├── main.py
│ ├── requirements.txt
│ └── .env.example
├── bot-moderation/ # v0.2
│ ├── main.py
│ └── requirements.txt
├── docs/
│ ├── 01-spec-v0.3.md # Cette spec
│ ├── 00-echanges-perplexity.md
│ └── 02-roadmap.md
├── .gitignore
├── requirements-dev.txt # pytest, etc.
└── README.md
## 📚 Documentation
- [Spécifications v0.3](Doc/SpecNewPunkyBot_03)
- [Références Discord.py](Doc/References/discord-py.md)