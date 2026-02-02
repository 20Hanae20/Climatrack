[//]: # (README professionnel — version réécrite)
# CLIMATRACK MAROC

Solution de surveillance météorologique destinée au Maroc — interface Streamlit, collecte d'API et stockage MongoDB.

Badges
: ![Python](https://img.shields.io/badge/Python-3.8+-blue.svg) ![Streamlit](https://img.shields.io/badge/Streamlit-1.31-red.svg) ![MongoDB](https://img.shields.io/badge/MongoDB-Latest-green.svg)

Description
-----------
ClimaTrack Maroc collecte, stocke et visualise des données météorologiques pour un jeu de villes marocaines. Elle est conçue pour être simple à déployer, claire pour l'utilisateur final et extensible pour des analyses temporelles et comparatives.

Principales fonctionnalités
---------------------------
- Tableaux de bord interactifs (conditions actuelles, tendances, comparaisons, historique)
- Récupération automatique depuis des fournisseurs API (OpenWeatherMap, WeatherAPI)
- Stockage historique dans MongoDB pour analyses et exports CSV
- Mode mock pour tests sans clé API
- Visualisations réactives avec Plotly

Architecture et fichiers clés
----------------------------
- `app.py` — Application Streamlit (interface utilisateur)
- `weather_service.py` — Module d'accès aux APIs météo et mode mock
- `db.py` — Gestion de la connexion et des opérations MongoDB
- `.env.example` — Variables d'environnement nécessaires
- `requirements.txt` — Dépendances Python

Prérequis
---------
- Python 3.8+
- MongoDB (local ou Atlas)
- (Optionnel) Clé API météo (OpenWeatherMap ou WeatherAPI)

Installation rapide
------------------
1. Cloner le dépôt

2. Installer les dépendances
```bash
pip install -r requirements.txt
```

3. Copier et configurer les variables d'environnement
```bash
copy .env.example .env
# puis éditez .env (MONGO_URI, WEATHER_API_KEY, WEATHER_API_PROVIDER)
```

Exécution (développement)
-------------------------
Lancer l'application Streamlit locale :
```bash
python -m streamlit run app.py
```
Par défaut l'interface sera disponible sur `http://localhost:8501`.

Configuration des variables d'environnement
------------------------------------------
- `MONGO_URI` — Chaîne de connexion MongoDB (ex. `mongodb://localhost:27017/` ou Atlas)
- `WEATHER_API_KEY` — Clé API fournie par le fournisseur météo (laisser vide pour mode mock)
- `WEATHER_API_PROVIDER` — `openweather` ou `weatherapi`

Mode mock (tests)
------------------
Pour développer sans clé API, activez le mode mock dans l'interface Streamlit ou laissez `WEATHER_API_KEY` vide ; `weather_service.py` détecte ce mode et renvoie des jeux de données simulés.

Schéma de données (collection `weather_realtime`)
-----------------------------------------------
Exemple de document stocké dans MongoDB :
```json
{
  "_id": "ObjectId",
  "city": "Casablanca",
  "timestamp": "2026-01-26T14:30:00",
  "temperature": 19.5,
  "humidity": 60,
  "pressure": 1012,
  "wind_speed": 14,
  "weather": "Clear",
  "description": "clear sky",
  "icon": "01d"
}
```

Bonnes pratiques
----------------
- Ne stockez pas de clés en clair dans le dépôt ; utilisez `.env` et un gestionnaire de secrets pour la production.
- Pour déploiement, configurez un utilisateur MongoDB limité et restreignez les accès réseau.

Dépannage rapide
-----------------
- Erreur de connexion MongoDB : vérifier `MONGO_URI`, état du service et règles réseau.
- Erreurs API : vérifier la clé, le fournisseur et respecter les quotas.
- Pas de données affichées : tester le mode mock et cliquer sur "Refresh Data Now".

Déploiement (suggestions)
-------------------------
- Déploiement simple : héberger l'app Streamlit sur une VM ou sur Streamlit Cloud.
- Utiliser Docker pour reproducibility : créer un `Dockerfile` basé sur Python 3.8, copier le projet, installer `requirements.txt`, exposer le port Streamlit et démarrer l'app.

Contribuer
---------
Contributions bienvenues : ouvrez une issue pour proposer une amélioration ou un bug, puis créez une branche dédiée et soumettez une pull request.

Licence
-------
Projet fourni à titre éducatif.

Contact
-------
Pour questions ou contributions : ouvrir une issue sur le dépôt.

---
Version professionnelle du `README.md` — mise à jour par l'équipe de maintenance.
