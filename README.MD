# NewPunkyBot

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![discord.py](https://img.shields.io/badge/discord.py-v2.4%2B-purple.svg)](https://discordpy.readthedocs.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Bot Discord modulaire pour apprendre Python**  
Bot personnel polyvalent : modération, productivité, jeux, langues, GitHub.  
**Auteur** : Emmanuel (Punkyherisson) | **Serveur cible** : Punkyherisson + multi-serveurs

## 🎯 Objectifs

NewPunkyBot est un **projet d'apprentissage Python concret** via développement d'un bot Discord modulaire (cogs).  
Démarche **agile** : v0.1 simple/testable → v1.0 complète.

**Priorités :**
- Progresser en Python (discord.py, cogs, APIs externes)
- Bot utilisable sur serveur Punkyherisson + autres serveurs
- Architecture sécurisée (pouvoirs < admin)

## 🚀 Fonctionnalités (Spécifications v0.2)

### 🛡️ **Modération & Administration**
- Avertir/mute/kick/ban/temp-ban automatique
- Filtrage spam/injurieux/raciste
- Logs détaillés quotidiens
- Système de niveaux (permissions + expertise domaine)
- Liens rapides (règles, forums, ressources)

### 📅 **Productivité & Organisation** 
- Rappels cours/devoirs/to-do lists
- Sondages, votes, collecte d'idées
- Agendas partagés par personne/sujet
- Statistiques temps passé (salons/jeux)

### 🎮 **Social & Développement Personnel**
- Jeux texte : trivia, pendu, RPG simple
- Système XP (jeux + tâches accomplies)
- Musique Spotify (abonnement famille)
- Mini-traductions : anglais, allemand, espagnol, japonais
- Exercices : yoga, sport (krav maga), méditation

### 🔌 **Intégrations Externes**
- GitHub : push/issues/PR → apprendre Git
- Météo Lyon (prévisions ski)
- Conversationnel langues (Talkpal/Duolingo style)

## 📋 Roadmap

| Version | Statut | Features principales |
|---------|--------|---------------------|
| **v0.1** | ⏳ TODO | `!ping`, `!info`, logs, liens rapides |
| **v0.2** | ⏳ TODO | Modération (`!mute`, `!kick`), filtrage |
| **v0.3** | 🔄 Plan | Productivité (to-do, rappels, météo) |
| **v1.0** | 🔮 Futur | Jeux, XP, Spotify, langues avancées |

## 🛠️ Architecture

NewPunkyBot/
├── bot/
│ ├── main.py # Chargeur principal
│ └── cogs/ # Modules spécialisés
│ ├── basic.py # !ping, !info
│ ├── moderation.py # !kick, !mute
│ └── productivite.py # !todo, !rappel
├── docs/ # Spécifications et utilisation Perplexity
├── requirements.txt
└── README.md