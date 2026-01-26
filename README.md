# CLIMATRACK MAROC

**Didier au Maroc · Système météo classique et simple** pour le Royaume du Maroc avec analyses interactives, stockage MongoDB et mise à jour automatique.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31-red.svg)
![MongoDB](https://img.shields.io/badge/MongoDB-Latest-green.svg)

## Aperçu du Projet

ClimaTrack Maroc est une application météo classique et simple, dédiée à 100% au territoire marocain:

- Couverture météorologique complète de 35+ villes marocaines
- Récupération des données météo en direct via API (OpenWeatherMap/WeatherAPI)
- Stockage de l'historique dans MongoDB pour analyses temporelles
- Dashboards interactifs avec Plotly
- Mise à jour automatique des données à intervalles réguliers
- Analyse automatique des tendances météorologiques
- Interface classique, sobre et lisible

## Fonctionnalités

### Dashboard 1: Vue Générale
- Indicateurs temps réel (Température, Humidité, Vent, Pression)
- Conditions météorologiques actuelles avec indicateurs visuels
- Sélection instantanée de ville

### Dashboard 2: Tendances et Évolution
- Graphiques temporels interactifs
- Suivi de l'évolution de la température
- Visualisation multi-métriques (Humidité et Vent)
- Analyse automatique des tendances

### Dashboard 3: Comparaison Multi-Villes
- Comparaison météorologique entre plusieurs villes
- Analyse comparative des métriques
- Identification automatique des extrêmes (plus chaud, plus froid, plus venteux)

### Dashboard 4: Données et Historique
- Tableau complet des données historiques
- Enregistrements triables et filtrables
- Fonctionnalité d'export CSV
- Résumés statistiques

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- MongoDB (local or Atlas)
- Weather API key (optional - mock data available)

### Installation

1. **Clone or download the project**

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables**
```bash
# Copy the example file
copy .env.example .env

# Edit .env with your credentials
# MONGO_URI=mongodb://localhost:27017/
# WEATHER_API_KEY=your_api_key_here
# WEATHER_API_PROVIDER=openweather
```

4. **Run the application**
```bash
python -m streamlit run app.py
```

5. **Accéder au dashboard**
Ouvrez votre navigateur à `http://localhost:8501`

## Couverture Géographique

### 35+ Villes Marocaines

**Grandes Métropoles**
- Casablanca, Rabat, Marrakech, Fès, Tanger, Agadir

**Villes Impériales et Régionales**
- Meknès, Oujda, Tétouan, Kenitra

**Villes Côtières Atlantiques**
- Essaouira, El Jadida, Safi, Mohammedia, Larache, Asilah

**Villes Côtières Méditerranéennes**
- Nador, Al Hoceima

**Villes de l'Intérieur**
- Béni Mellal, Khouribga, Taza, Khemisset, Settat

**Villes du Sud**
- Laâyoune, Dakhla, Guelmim, Tan-Tan, Taroudant, Ouarzazate

**Autres Villes Importantes**
- Errachidia, Ifrane, Ksar El Kebir

## 🔧 Configuration

### MongoDB Setup

**Option 1: Local MongoDB**
```
MONGO_URI=mongodb://localhost:27017/
```

**Option 2: MongoDB Atlas (Cloud)**
```
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/
```

### Weather API Setup

**OpenWeatherMap** (Recommended)
1. Sign up at https://openweathermap.org/api
2. Get your free API key
3. Set in `.env`:
```
WEATHER_API_KEY=your_key_here
WEATHER_API_PROVIDER=openweather
```

**WeatherAPI.com** (Alternative)
1. Sign up at https://www.weatherapi.com/
2. Get your API key
3. Set in `.env`:
```
WEATHER_API_KEY=your_key_here
WEATHER_API_PROVIDER=weatherapi
```

### Mock Data Mode

For testing without API keys, enable mock data in the sidebar:
- ✅ Check "Use Mock Data (for testing)"
- Click "🔄 Refresh Data Now"

## 📁 Project Structure

```
climatrack/
│
├── app.py                 # Main Streamlit application
├── db.py                  # MongoDB database handler
├── weather_service.py     # Weather API service
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## 🎮 Usage

### Contrôles de la Barre Latérale

- **Ville sélectionnée**: Choisir la ville à afficher
- **Comparaison multi-villes**: Sélectionner plusieurs villes pour comparaison
- **Plage temporelle**: Ajuster la plage de données historiques (1-72 heures)
- **Actualiser maintenant**: Récupérer manuellement de nouvelles données météo
- **Auto-refresh**: Activer les mises à jour automatiques toutes les 30 secondes

### Dashboard Navigation

Use the tabs at the top to switch between:
1. **📊 Live Overview** - Current conditions
2. **📈 Trends & Evolution** - Historical charts
3. **🌐 City Comparison** - Multi-city analysis
4. **📋 Data & History** - Raw data table

## 🧠 Intelligent Analysis

L'application fournit automatiquement des analyses:
- Détection de changement de température
- Analyse des tendances de pression
- Alertes de vitesse du vent
- Classements comparatifs des villes

## 📊 Data Schema

MongoDB collection `weather_realtime`:
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

## Pour Présentations Académiques

**Points Clés:**
- Récupération de données en temps réel depuis des APIs externes
- Stockage persistant dans MongoDB
- Visualisations interactives avec Plotly
- Actualisation automatique des données (pseudo temps réel)
- Analyse intelligente des tendances
- Capacités de comparaison multi-villes
- Fonctionnalité d'export de données
- **Couverture complète du territoire marocain (35+ villes)**
- **Interface professionnelle moderne et épurée**

**Stack Technique:**
- **Frontend**: Streamlit (framework web Python)
- **Base de données**: MongoDB (stockage de documents NoSQL)
- **Visualisation**: Plotly (graphiques interactifs)
- **API**: OpenWeatherMap / WeatherAPI
- **Traitement de données**: Pandas
- **Design**: Système de design professionnel inspiré du Maroc

## 🛠️ Troubleshooting

**MongoDB Connection Failed**
- Ensure MongoDB is running locally, or
- Check your Atlas connection string
- Verify network connectivity

**API Errors**
- Verify your API key is correct
- Check API rate limits
- Use mock data mode for testing

**No Data Displayed**
- Click "Refresh Data Now" to fetch initial data
- Ensure at least one city is selected
- Check MongoDB connection

## 📝 License

This project is created for educational purposes.

## 👨‍💻 Author

Créé dans le cadre d'un projet de fin d'études (PFE) démontrant:
- Traitement de données en temps réel
- Intégration de base de données
- Dashboards web interactifs
- Consommation d'API
- Visualisation de données
- **Application professionnelle dédiée au Maroc**

---

**CLIMATRACK MAROC** - Système Professionnel de Surveillance Météorologique pour le Royaume du Maroc
