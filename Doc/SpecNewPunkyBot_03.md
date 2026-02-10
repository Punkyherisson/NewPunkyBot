# NewPunkyBot - Spécifications v0.3 (Multi-bots)

## 🎯 Objectifs Généraux
- Apprentissage Python concret/modulaire
- Multi-serveurs (Punkyherisson + autres)
- **Multi-bots** : 1 bot = 1 mission (débutant-friendly)
- Sécurité : Pouvoirs < admin

## 📋 Roadmap Multi-bots (plusieurs mois)

### **Bot 1 : Organisation v0.1** (Priorité IMMÉDIATE)
Commandes principales :
!ProchainCours <matière> <date> <heure> <format> <personne>
Exemples :
!ProchainCours Python 2026-02-14 14:00 Presenciel Aless
→ Crée événement Discord + emoji 🐍 Python + Aless/toi

!ProchainCours Japonais 2026-02-16 18:00 Presenciel Ludchal
→ Événement + emoji 🇯🇵 Japon + Ludchal/toi

!ProchainDevoir Python "Faire spec BOT" [lien discussion]
→ Événement devoir + lien

text

### **Bot 2 : Modération** (v0.2+)
- !mute, !kick, !ban auto
- Filtrage spam/injurieux
- Logs quotidiens

### **Bot 3 : Social/Jeux** (v1.0)
- Trivia, pendu, RPG
- Système XP/niveaux
- Spotify, traductions langues

### **Bot 4 : Productivité/Intégrations** (v1.0+)
- GitHub, météo Lyon
- Conversationnel langues (Talkpal-style)

## 🔧 Architecture Projet
NewPunkyBot/ (repo parent)
├── bot-organisation/ # v0.1
├── bot-moderation/ # v0.2
├── bot-social/ # v1.0
└── docs/