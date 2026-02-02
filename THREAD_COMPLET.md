# 🧵 THREAD COMPLET - ClimaTrack Maroc

## 📌 À CONSULTER À CHAQUE FOIS

---

# 🏛️ 1. ARCHITECTURE GÉNÉRALE

```
┌─────────────────────────────────────────────────┐
│         PRESENTATION (UI - app.py)              │
│  • Streamlit (dashboards interactifs)           │
│  • Plotly (graphiques interactifs)              │
│  • 4 Tabs (Vue générale, Tendances, ...)        │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│    SERVICES (Logique métier)                    │
│  • weather_service.py (API externes)            │
│  • db.py (MongoDB)                              │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│    BASE DE DONNÉES                              │
│  • MongoDB (climatrack.weather_realtime)        │
└─────────────────────────────────────────────────┘
```

---

# 📦 2. LES 3 FICHIERS PRINCIPAUX

## **A. db.py** 🗄️ (Base de données MongoDB)

### Classe: `WeatherDB`

| Méthode | Rôle | Retourne |
|---------|------|----------|
| `connect()` | Connexion MongoDB | bool |
| `save_weather_data(data)` | Ajouter un document | bool |
| `get_latest_weather(city)` | Données actuelles d'une ville | dict |
| `get_historical_weather(city, hours)` | Historique sur N heures | list[dict] |
| `get_all_cities()` | Toutes les villes en BD | list[str] |
| `get_comparison_data(cities)` | Données pour plusieurs villes | dict |

### Pattern Singleton

```python
_db_instance = None

def get_db() -> WeatherDB:
    global _db_instance
    if _db_instance is None:
        _db_instance = WeatherDB()
        _db_instance.connect()
    return _db_instance
```

**Utilisation:** Une seule connexion MongoDB pour toute l'app

### Structure Document MongoDB

```json
{
  "city": "Casablanca",
  "temperature": 22.5,
  "humidity": 65,
  "pressure": 1013,
  "wind_speed": 15.3,
  "weather": "Clear",
  "description": "ciel dégagé",
  "icon": "01d",
  "timestamp": "2026-01-26T14:30:00Z"
}
```

---

## **B. weather_service.py** 🌐 (APIs externes)

### Classe: `WeatherService`

| Méthode | Rôle |
|---------|------|
| `fetch_weather(city)` | Route vers le bon API |
| `_fetch_openweather(city)` | Appel OpenWeatherMap |
| `_fetch_weatherapi(city)` | Appel WeatherAPI |
| `generate_mock_data(city)` | Données simulées (tests) |

### Fonction Globale

```python
def update_weather_data(cities, db, use_mock=False):
    """Récupère et sauvegarde les données pour TOUTES les villes"""
    # Boucle sur chaque ville
    # Appelle fetch_weather() ou generate_mock_data()
    # Sauvegarde dans MongoDB
```

### Conversion Importante

**OpenWeatherMap donne le vent en m/s, pas km/h!**

```
m/s → km/h: multiplier par 3.6
4.25 m/s × 3.6 = 15.3 km/h
```

### Formats API

**OpenWeatherMap Response:**
```json
{
  "main": {"temp": 22.5, "humidity": 65, "pressure": 1013},
  "wind": {"speed": 4.25},
  "weather": [{"main": "Clear", "description": "ciel dégagé"}]
}
```

**Réponse Standardisée (les 3 fichiers utilisent ça):**
```json
{
  "city": "Casablanca",
  "temperature": 22.5,
  "humidity": 65,
  "pressure": 1013,
  "wind_speed": 15.3,
  "weather": "Clear",
  "description": "ciel dégagé",
  "timestamp": "2026-01-26T14:30:00Z"
}
```

---

## **C. app.py** 🎨 (Interface Streamlit)

### Configuration Page

```python
st.set_page_config(
    page_title="ClimaTrack Maroc",
    page_icon="🇲🇦",
    layout="wide"
)
```

### Initialisation DB (une fois)

```python
@st.cache_resource
def init_database():
    db = get_db()
    return db

db = init_database()
```

### Sidebar (Contrôles)

| Élément | Type | Usage |
|---------|------|-------|
| `selected_city` | selectbox | 1 ville pour vue générale |
| `comparison_cities` | multiselect | Plusieurs villes pour comparaison |
| `time_range` | slider | Plage temporelle (1-72h) |
| `use_mock` | checkbox | Utiliser données simulées? |
| `Actualiser` | button | Rafraîchir les données |

### 4 Dashboards (Tabs)

**Tab 1: Vue Générale**
- 4 métriques KPI (Température, Humidité, Vent, Pression)
- Données actuelles: `db.get_latest_weather(selected_city)`

**Tab 2: Tendances**
- Graphique température (ligne)
- Graphique humidité + vent (double axe Y)
- Analyse automatique (augmentation/baisse)
- Données: `db.get_historical_weather(selected_city, hours=time_range)`

**Tab 3: Comparaison**
- 3 graphiques (températures, humidité, vent)
- Identification extrêmes (plus chaud, plus froid, plus venteux)
- Données: `db.get_comparison_data(comparison_cities)`

**Tab 4: Historique**
- Tableau interactif
- Statistiques (max, min, moyenne)
- Bouton export CSV
- Données: `db.get_historical_weather(selected_city, hours=time_range)`

---

# 🔄 3. FLUX D'EXÉCUTION COMPLET

```
[1] UTILISATEUR OUVRE L'APP
         ↓
[2] Streamlit charge app.py
         ↓
[3] @st.cache_resource initialise DB (une fois)
         ↓
[4] Interface affichée avec Sidebar + 4 Tabs
         ↓
[5] UTILISATEUR CLIQUE "ACTUALISER MAINTENANT"
         ↓
[6] update_weather_data(MOROCCAN_CITIES, db) lancée
         │
         ├─ Pour chaque ville:
         │  ├─ fetch_weather(city)
         │  │  └─ Appel API OpenWeatherMap
         │  └─ db.save_weather_data(data)
         │     └─ Insertion MongoDB
         │
         └─ Toutes les villes mises à jour
         ↓
[7] st.rerun() - Page recharge
         ↓
[8] DASHBOARDS SE METTENT À JOUR
         ├─ Dashboard 1: get_latest_weather()
         ├─ Dashboard 2: get_historical_weather()
         ├─ Dashboard 3: get_comparison_data()
         └─ Dashboard 4: get_historical_weather()
```

---

# 📋 4. QUERIES MONGODB IMPORTANTES

### Query 1: Dernière météo d'une ville
```javascript
db.weather_realtime.findOne(
  { city: "Casablanca" },
  { sort: { timestamp: -1 } }
)
// ← get_latest_weather()
```

### Query 2: Historique sur 24h
```javascript
db.weather_realtime.find({
  city: "Casablanca",
  timestamp: { $gte: ISODate("2026-01-25T14:30:00Z") }
}).sort({ timestamp: 1 })
// ← get_historical_weather(city, hours=24)
```

### Query 3: Toutes les villes
```javascript
db.weather_realtime.distinct("city")
// ← get_all_cities()
```

---

# 🎯 5. CAS D'USAGE

## Cas 1: Afficher la température actuellement à Casablanca

```
Utilisateur sélectionne Casablanca
         ↓
Clic Tab "Vue Générale"
         ↓
app.py: latest = db.get_latest_weather("Casablanca")
         ↓
MongoDB: Cherche le dernier document pour Casablanca
         ↓
Affiche: "TEMPÉRATURE: 22.5°C"
```

## Cas 2: Voir les tendances température des 24h dernières

```
Utilisateur sélectionne Casablanca
Slider: 24h (par défaut)
         ↓
Clic Tab "Tendances"
         ↓
app.py: historical = db.get_historical_weather("Casablanca", hours=24)
         ↓
MongoDB: Cherche tous les documents des 24h
         ↓
Crée DataFrame pandas
         ↓
Affiche graphique Plotly (ligne rouge)
```

## Cas 3: Comparer Casablanca vs Rabat vs Marrakech

```
Utilisateur multiselect: [Casablanca, Rabat, Marrakech]
         ↓
Clic Tab "Comparaison"
         ↓
app.py: comp_data = db.get_comparison_data([...])
         ↓
MongoDB: get_latest_weather() pour chacune
         ↓
Crée DataFrame: Villes × Températures/Humidité/Vent
         ↓
Affiche 3 graphiques bar + identifie extrêmes
```

---

# ⚙️ 6. VARIABLES D'ENVIRONNEMENT (.env)

```env
# Connexion MongoDB
MONGO_URI=mongodb://localhost:27017/

# Clé API OpenWeatherMap
WEATHER_API_KEY=897718d195d4a8e7652d1a0698eefd3e

# Fournisseur API
WEATHER_API_PROVIDER=openweather
# Options: "openweather" | "weatherapi"
```

---

# 🌍 7. COUVERTURE GÉOGRAPHIQUE (35+ villes)

**Grandes métropoles:** Casablanca, Rabat, Marrakech, Fès, Tanger, Agadir

**Villes côtières:** Essaouira, El Jadida, Safi, Nador, Al Hoceima, Dakhla

**Villes intérieures:** Meknès, Oujda, Béni Mellal, Khouribga, Taza, Ifrane

**Villes du sud:** Ouarzazate, Guelmim, Tan-Tan, Laâyoune

---

# 🔧 8. DÉPENDANCES

```
streamlit==1.31.0          # UI web
pymongo==4.6.1             # MongoDB
requests==2.31.0           # Requêtes HTTP
pandas==2.2.0              # Manipulation données
plotly==5.18.0             # Graphiques
python-dotenv==1.0.1       # Variables .env
```

---

# ✅ 9. CHECKLIST MAINTENANCE

- [ ] Clé API OpenWeatherMap valide (.env)?
- [ ] MongoDB connectée et accessible?
- [ ] 35+ villes présentes dans MOROCCAN_CITIES?
- [ ] Données collectées récemment (timestamps)?
- [ ] Graphiques Plotly s'affichent correctement?
- [ ] Export CSV fonctionne (Tab 4)?
- [ ] Auto-refresh activé si souhaité?

---

# 🚀 10. COMMANDES ESSENTIELLES

```bash
# Lancer l'app
streamlit run app.py

# Installer dépendances
pip install -r requirements.txt

# Tester connexion MongoDB
mongosh mongodb://localhost:27017/

# Vérifier clé API
curl "http://api.openweathermap.org/data/2.5/weather?q=Casablanca&appid=YOUR_KEY&units=metric"
```

---

# 📊 11. STRUCTURE DATA

### Base de Données
```
climatrack (database)
  └─ weather_realtime (collection)
      ├─ Document 1: {city: "Casablanca", temp: 22.5, timestamp: ...}
      ├─ Document 2: {city: "Casablanca", temp: 21.5, timestamp: ...}
      ├─ Document 3: {city: "Rabat", temp: 19.8, timestamp: ...}
      └─ ... (100s de documents)
```

### DataFrame Pandas (utilisé dans app.py)
```
   timestamp           city    temperature  humidity  pressure  wind_speed  weather
0  2026-01-25 14:00:00  Casablanca  20.0       68        1013     12.5      Clear
1  2026-01-25 15:00:00  Casablanca  21.5       65        1013     14.2      Clear
2  2026-01-25 16:00:00  Casablanca  22.3       63        1012     15.3      Clouds
```

---

# 🎨 12. THÈME COULEURS

| Élément | Couleur | Code |
|---------|---------|------|
| Fond principal | Très sombre | #0f172a |
| Cartes métrique | Sombre | #1e293b |
| Texte | Clair | #e2e8f0 |
| Texte muted | Grisé | #94a3b8 |
| Accent (Maroc) | Or/Bronze | #c79a61 |
| Température | Rouge-orange | #FF6B6B |
| Humidité | Cyan | #4ECDC4 |
| Vent | Vert clair | #95E1D3 |

---

# 📞 13. POINTS DE CONTACT (Appels de fonction)

```
app.py
  ├─ Appelle db.py
  │   ├─ get_latest_weather(city)
  │   ├─ get_historical_weather(city, hours)
  │   └─ get_comparison_data(cities)
  │
  └─ Appelle weather_service.py
      └─ update_weather_data(cities, db, use_mock)
          └─ fetch_weather(city)
```

---

# 🔐 14. GESTION ERREURS

| Erreur | Source | Fallback |
|--------|--------|----------|
| API timeout | OpenWeatherMap | generate_mock_data() |
| Clé API invalide | .env | generate_mock_data() |
| MongoDB offline | Base de données | None (affiche warning) |
| Ville non trouvée | BD vide | affiche "Aucune donnée" |

---

# 💾 15. SAUVEGARDES & HISTORIQUE

**Fréquence de mise à jour:** Manuel (bouton) ou Auto (case à cocher 1 min)

**Rétention des données:** Tous les documents sauvegardés indéfiniment

**Volume estimé:**
- 35 villes × 24 mises à jour/jour = 840 documents/jour
- MongoDB stocke tout → analyse historique sur plusieurs mois

---

# 🎓 16. CONCEPTS CLÉS À RETENIR

| Concept | Explication |
|---------|-------------|
| **Singleton** | Une seule instance DB pour toute l'app |
| **Standardisation** | Tous les APIs convertis au même format |
| **Cache Streamlit** | @st.cache_resource = créé qu'une fois |
| **Requête aggregation** | MongoDB find_one vs find vs distinct |
| **Pivot Data** | Pandas pour transformer données pour graphiques |
| **Rerun** | st.rerun() recharge la page sans perdre session |

---

# 📈 17. MÉTRIQUES À MONITORER

- **Temps réponse API:** < 2 secondes
- **Nombre documents/jour:** ~840
- **Taille moyenne document:** ~500 bytes
- **Espace MongoDB estimé:** ~400 MB/an
- **Utilisateurs simultanés:** Streamlit supporte bien 1-10

---

# 🔄 18. MISE À JOUR COMPLÈTE

```python
# Clic "Actualiser maintenant" déclenche:

update_weather_data(
    cities=MOROCCAN_CITIES,  # 35 villes
    db=db,                   # Instance MongoDB
    use_mock=False           # Ou True si test
)

# Internement:
# Pour chaque ville:
#   1. Appel API (ou mock)
#   2. Standardisation données
#   3. Sauvegarde MongoDB
#   4. Print status
# PUIS: st.rerun() → Reload tous les dashboards
```

---

# 🎯 19. QUICK REFERENCE - Quelles données où?

| Besoin | Méthode | Retourne | Usage |
|--------|---------|----------|-------|
| Temp actuelle | `get_latest_weather(city)` | dict | Tab 1: KPI |
| Graphique 24h | `get_historical_weather(city, 24)` | list[dict] | Tab 2: Lignes |
| Comparer 3 villes | `get_comparison_data([cities])` | dict | Tab 3: Barres |
| Tableau export | `get_historical_weather(city, 24)` | list[dict] | Tab 4: CSV |

---

# 🛑 20. DÉPANNAGE RAPIDE

**Problème:** "Aucune donnée disponible"
- **Solution:** Cliquer "Actualiser maintenant"

**Problème:** Graphiques vides
- **Solution:** Vérifier que time_range ≥ 2 points de données

**Problème:** API timeout
- **Solution:** Utiliser checkbox "Utiliser données simulées"

**Problème:** MongoDB connection refused
- **Solution:** Vérifier MONGO_URI dans .env et que MongoDB tourne

---

Besoin de clarification sur un point? 🤔
