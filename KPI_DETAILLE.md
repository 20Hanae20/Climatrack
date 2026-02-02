# 📊 EXPLICATION DÉTAILLÉE DES KPI - ClimaTrack Maroc

---

## 🎯 **QUE SONT LES KPI?**

**KPI = Key Performance Indicator (Indicateur Clé de Performance)**

Les KPI sont des **métriques chiffrées** qui donnent une vue rapide et précise de la situation.

Dans ClimaTrack, ce sont les **8 valeurs principales** affichées dans les dashboards.

---

# 📍 **GROUPE 1: LES 4 KPI ACTUELS (Dashboard 1)**

## **Emplacement dans l'interface**

```
┌───────────────────────────────────────────────────────────────┐
│           CLIMATRACK MAROC - Casablanca                        │
├───────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────┐
│  │ TEMPÉRATURE  │  │   HUMIDITÉ   │  │    VENT      │  │PRES  │
│  │   22.5°C     │  │     65%      │  │  15.3 km/h   │  │1013  │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────┘
│
│ Ces 4 KPI changent à chaque minute (si auto-refresh)
│ ou quand vous cliquez "Actualiser maintenant"
└───────────────────────────────────────────────────────────────┘
```

---

## **1️⃣ KPI: TEMPÉRATURE (°C)**

### 📌 Définition
La **température actuelle** de l'air dans la ville sélectionnée, mesurée en degrés Celsius.

### 📊 Code dans app.py
```python
with col1:
    st.metric(
        label="🌡️ TEMPÉRATURE",
        value=f"{latest['temperature']:.1f}°C"
    )
```

### 🔍 Source des données
```python
latest = db.get_latest_weather(selected_city)
# Récupère le DERNIER document de cette ville dans MongoDB
# Et extrait: latest['temperature']
```

### 📈 Exemple concret

**Scenario:** Vous sélectionnez "Casablanca" le 26 janvier 2026 à 14h30

```
ÉTAPE 1: Vous ouvrez l'app
    ↓
ÉTAPE 2: Vous sélectionnez "Casablanca" dans le sidebar
    ↓
ÉTAPE 3: Cliquez "Actualiser maintenant"
    ↓
ÉTAPE 4: update_weather_data() se lance
    - Appel API OpenWeatherMap pour Casablanca
    - API retourne: {"main": {"temp": 22.5}}
    - Convertis en: {"temperature": 22.5, "city": "Casablanca", "timestamp": "..."}
    - Sauvegardé dans MongoDB
    ↓
ÉTAPE 5: Page recharge (st.rerun())
    ↓
ÉTAPE 6: db.get_latest_weather("Casablanca") récupère ce document
    ↓
RÉSULTAT AFFICHAGE:
    ┌──────────────┐
    │ TEMPÉRATURE  │
    │   22.5°C     │
    └──────────────┘
```

### 🌡️ Interprétation

| Température | Situation | Conseil |
|-------------|-----------|---------|
| < 0°C | Très froid (rare au Maroc) | 🧥 Vêtements chauds |
| 0-10°C | Froid | 🧥 Manteau léger |
| 10-15°C | Frais | 👕 Pulls/Chemises |
| 15-20°C | Agréable | 👕 Vêtements légers |
| 20-25°C | Chaud | 👕 T-shirt |
| 25-30°C | Très chaud | ☀️ Crème solaire |
| > 30°C | Extrêmement chaud | ☀️ Hydratation critique |

### 💾 Stockage MongoDB

```json
{
  "_id": ObjectId("507f1f77bcf86cd799439011"),
  "city": "Casablanca",
  "temperature": 22.5,
  "timestamp": ISODate("2026-01-26T14:30:00Z"),
  ...
}
```

### 📊 Query MongoDB
```javascript
// Récupère la dernière température de Casablanca
db.weather_realtime.findOne(
  { city: "Casablanca" },
  { sort: { timestamp: -1 } }
)
// Résultat: { temperature: 22.5, ... }
```

### 🎓 Conversions utiles
```
Celsius → Fahrenheit: (°C × 9/5) + 32
Exemple: 22.5°C = (22.5 × 9/5) + 32 = 72.5°F

Celsius → Kelvin: °C + 273.15
Exemple: 22.5°C = 22.5 + 273.15 = 295.65 K
```

---

## **2️⃣ KPI: HUMIDITÉ (%)**

### 📌 Définition
Le **pourcentage d'eau** présent dans l'air ambiant.

- **Basse humidité (< 30%):** Air très sec
- **Humidité normale (30-60%):** Confortable
- **Haute humidité (> 60%):** Air humide/moite

### 📊 Code dans app.py
```python
with col2:
    st.metric(
        label="💧 HUMIDITÉ",
        value=f"{latest['humidity']}%"
    )
```

### 🔍 Source des données
```python
latest = db.get_latest_weather(selected_city)
# Extrait: latest['humidity']
# Plage: 0-100%
```

### 📈 Exemple concret

**Scenario:** À Casablanca à 14h30
```
Température: 22.5°C
Humidité: 65%

INTERPRÉTATION:
L'air contient 65% de sa capacité maximale d'eau.
C'est une humidité "normale" - confortable pour la plupart.
Vous pouvez respirer normalement, pas de moiteur excessive.
```

### 💧 Interprétation détaillée

| Humidité | Ressenti    | Impact santé            | Confort            |
|----------|-------------|-------------------------|--------------------|
| 0-20%    | Très sec    | Lèvres gercées, toux    | Inconfortable      |
| 20-35%   | Sec         | Irritations ORL         | Pas idéal          |
| 35-60%   | Normal      | Aucun                   | ✅ Optimal        |
| 60-80%   | Humide      | Transpiration excessive | Moite              |
| 80-100%  | Très humide | Sensation de moiteur    | Très inconfortable |

### 📊 Variations au Maroc

**Casablanca (côtière):**
```
Matin: 75% (humidité du large)
Midi: 65% (assèchement)
Soir: 80% (retour humidité)
```

**Marrakech (intérieur):**
```
Matin: 45% (air très sec)
Midi: 35% (air très sec)
Soir: 50% (légère augmentation)
```

### 💾 Stockage MongoDB
```json
{
  "city": "Casablanca",
  "humidity": 65,
  "timestamp": ISODate("2026-01-26T14:30:00Z")
}
```

### 🌡️ Relation Température-Humidité

**Point de rosée:** Température à laquelle l'eau condense

```
Formule approchée:
Point de rosée ≈ T - ((100 - RH) / 5)

Exemple:
Température: 22.5°C
Humidité: 65%
Point de rosée = 22.5 - ((100 - 65) / 5)
                = 22.5 - 7
                = 15.5°C

Si la température chute à 15.5°C, il y aura rosée/brouillard
```

---

## **3️⃣ KPI: VENT (km/h)**

### 📌 Définition
La **vitesse du vent** à la surface, mesurée en kilomètres par heure.

### 📊 Code dans app.py
```python
with col3:
    st.metric(
        label="💨 VENT",
        value=f"{latest['wind_speed']:.1f} km/h"
    )
```

### 🔍 Source des données
```python
latest = db.get_latest_weather(selected_city)
# Extrait: latest['wind_speed']

# ⚠️ IMPORTANT: OpenWeatherMap donne le vent en m/s
# weather_service.py convertit automatiquement:
wind_speed: data["wind"]["speed"] * 3.6  # m/s × 3.6 = km/h
```

### 🔄 Conversion m/s → km/h

**Formula:**
```
km/h = m/s × 3.6
```

**Exemples:**
```
1 m/s  = 3.6 km/h    (très calme)
2.5 m/s = 9 km/h     (léger)
4.25 m/s = 15.3 km/h (modéré)
7 m/s = 25.2 km/h    (fort)
10 m/s = 36 km/h     (très fort)
```

### 📈 Exemple concret

**Scenario:** OpenWeatherMap retourne
```json
{
  "wind": {
    "speed": 4.25  // En m/s !
  }
}
```

**Conversion dans weather_service.py:**
```python
wind_speed = 4.25 * 3.6 = 15.3 km/h
```

**Affichage dans KPI:**
```
┌──────────────┐
│    VENT      │
│  15.3 km/h   │
└──────────────┘
```

### 💨 Échelle de Beaufort (Vent)

| Vitesse (km/h) | Force | Terme | Observation | Impact |
|---|---|---|---|---|
| 0-1 | 0 | Calme | Pas de vent | Fumée monte droit |
| 2-5 | 1 | Très léger | À peine perceptible | Fumée dévie légèrement |
| 6-11 | 2 | Léger | Sensation sur le visage | Feuilles bougent |
| 12-19 | 3 | Léger brise | Vent perceptible | Petites branches bougent |
| 20-28 | 4 | Modéré | Cheveux s'ébouriffent | Poussière vole |
| 29-38 | 5 | Assez fort | Difficile de marcher | Arbres se plient |
| 39-49 | 6 | Fort | Danger marche | Branches cassent |
| 50-61 | 7 | Très fort | Vent violent | Dommages bâtiments |
| 62-74 | 8 | Tempête | TRÈS DANGEREUX | Toitures endommagées |
| > 74 | 9+ | Ouragan | EXTRÊMEMENT DANGEREUX | Destruction massive |

### 📊 Interprétation pour le Maroc

```
< 10 km/h: Beau temps
10-20 km/h: Normal, agréable
20-30 km/h: Vent modéré, attention
> 30 km/h: ALERTE VENT FORT ⚠️
```

### 🚨 Alerte Automatique dans Dashboard 2

```python
if df['wind_speed'].max() > 20:
    st.warning(f"Vents forts détectés! Pic: {df['wind_speed'].max():.1f} km/h")
```

**Affichage:**
```
⚠️ Vents forts détectés! Pic: 25.3 km/h
```

### 💾 Stockage MongoDB
```json
{
  "city": "Casablanca",
  "wind_speed": 15.3,  // En km/h (après conversion)
  "timestamp": ISODate("2026-01-26T14:30:00Z")
}
```

---

## **4️⃣ KPI: PRESSION (hPa)**

### 📌 Définition
La **force exercée par l'air** sur la surface, mesurée en hectopascals (hPa).

Also called: **Pression atmosphérique** ou **Pression barométrique**

### 📊 Code dans app.py
```python
with col4:
    st.metric(
        label="🔽 PRESSION",
        value=f"{latest['pressure']} hPa"
    )
```

### 🔍 Source des données
```python
latest = db.get_latest_weather(selected_city)
# Extrait: latest['pressure']
# Unité: hPa (hectopascals)
```

### 📈 Exemple concret

**Au niveau de la mer:**
```
Pression normale: 1013 hPa
Pression basse (mauvais temps): 990 hPa
Pression haute (beau temps): 1020+ hPa
```

**À Marrakech (480 m d'altitude):**
```
Pression réduite au niveau mer: 1013 hPa
Pression réelle: ~955 hPa
(1 hPa perdu par 8 m d'altitude)
```

### 📊 Interprétation détaillée

| Pression (hPa) | Météo | Tendance | Altitude |
|---|---|---|---|
| < 980 | Très mauvaise | Dépression | ⬇️ Baisse |
| 980-1000 | Mauvaise | Baisse | ⬇️ Baisse |
| 1000-1010 | Variable | Instable | ➡️ Stable |
| 1010-1020 | Bonne | Montée | ⬆️ Hausse |
| > 1020 | Très bonne | Hausse | ⬆️ Hausse |

### 🎓 Conversions de Pression

```
hPa → mmHg: 1 hPa = 0.75 mmHg
hPa → atm: 1 hPa = 0.000987 atm
hPa → Pascal: 1 hPa = 100 Pa

Exemples:
1013 hPa = 759.75 mmHg = 1 atm = 101300 Pa
```

### 🌍 Pression à différentes altitudes

**Formule barométrique simplifiée:**
```
P = P₀ × (1 - L × h / T₀)^(g × M / (R × L))

Ou plus simplement:
Pression diminue de ~10% par 1000 m d'altitude
```

**Au Maroc:**
```
Casablanca (niveau mer): ~1013 hPa
Fès (500 m): ~955 hPa
Marrakech (470 m): ~960 hPa
Ouarzazate (1160 m): ~880 hPa
Ifrane (1650 m): ~815 hPa ← La plus haute altitude
```

### 📊 Relation Pression-Météo

```
BAISSE RAPIDE DE PRESSION
    ↓
Tempête/Orage approche (12-24h)
    ↓
Conseillez prudence aux navigateurs


HAUSSE DE PRESSION
    ↓
Amélioration du temps
    ↓
Beau temps arrivant
```

### 💾 Stockage MongoDB
```json
{
  "city": "Casablanca",
  "pressure": 1013,
  "timestamp": ISODate("2026-01-26T14:30:00Z")
}
```

### 🔍 Query MongoDB
```javascript
// Récupère la pression actuelle et historique
db.weather_realtime.find(
  { city: "Casablanca" }
).sort({ timestamp: -1 }).limit(24)
// 24 derniers enregistrements pour voir la tendance
```

---

# 📍 **GROUPE 2: LES 4 KPI STATISTIQUES (Dashboard 4)**

## **Emplacement dans l'interface**

```
┌───────────────────────────────────────────────────────────────┐
│                    STATISTIQUES                                │
├───────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────┐
│  │ 🔥 Temp Max  │  │ ❄️ Temp Min  │  │📊 Temp Moy   │  │📋 Nb │
│  │   25.3°C     │  │   18.2°C     │  │   21.8°C     │  │  24  │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────┘
│
│ Ces 4 KPI CHANGENT selon la plage temporelle sélectionnée
└───────────────────────────────────────────────────────────────┘
```

---

## **5️⃣ KPI: TEMPÉRATURE MAXIMALE (°C)**

### 📌 Définition
La **plus haute température** enregistrée pendant la période sélectionnée.

### 📊 Code dans app.py
```python
df = pd.DataFrame(historical)  # Tous les enregistrements
max_temp = df['temperature'].max()  # Valeur maximale

st.metric("🔥 Temp Max", f"{max_temp:.1f}°C")
```

### 🔍 Source des données
```python
historical = db.get_historical_weather(selected_city, hours=time_range)
# Récupère TOUS les documents de la période

# Si time_range = 24h:
# Récupère tous les enregistrements des 24 dernières heures
# Puis cherche le maximum
```

### 📈 Exemple concret

**Scenario:** Casablanca, 24 dernières heures
```
Timestamps et températures:
14:00  → 20.0°C
15:00  → 21.5°C
16:00  → 22.3°C  ← Pic de l'après-midi
17:00  → 23.1°C
18:00  → 22.5°C
19:00  → 21.0°C
20:00  → 19.8°C
21:00  → 18.5°C
22:00  → 17.2°C
...
09:00 (lendemain) → 15.0°C

RÉSULTAT: Temp Max = 23.1°C (à 17:00)
```

### 📊 Formule
```
Temp Max = MAX(T₁, T₂, T₃, ..., Tₙ)

Exemple:
Temp Max = MAX(20.0, 21.5, 22.3, 23.1, 22.5, 21.0, 19.8, 17.2, 15.0)
         = 23.1°C
```

### 🎓 Utilité

- **Planifier vêtements:** Savoir qu'il fera au maximum 23°C
- **Avertissements:** Si max > 35°C → Alerte canicule
- **Comparaisons:** Jour 1 max = 23°C, Jour 2 max = 28°C (plus chaud)

### 💾 Stockage MongoDB
```
Les données brutes sont sauvegardées:
{temperature: 20.0, timestamp: ...}
{temperature: 21.5, timestamp: ...}
{temperature: 22.3, timestamp: ...}
...

Puis Python calcule: max(20.0, 21.5, 22.3, ...) = 23.1°C
```

---

## **6️⃣ KPI: TEMPÉRATURE MINIMALE (°C)**

### 📌 Définition
La **plus basse température** enregistrée pendant la période sélectionnée.

### 📊 Code dans app.py
```python
df = pd.DataFrame(historical)  # Tous les enregistrements
min_temp = df['temperature'].min()  # Valeur minimale

st.metric("❄️ Temp Min", f"{min_temp:.1f}°C")
```

### 📈 Exemple concret

**Scenario:** Casablanca, 24 dernières heures (SUITE)
```
Temperatures enregistrées:
14:00  → 20.0°C
15:00  → 21.5°C
...
09:00  → 15.0°C  ← Plus basse (avant le lever du soleil)
08:00  → 14.5°C  ← MINIMUM !
07:00  → 14.8°C
06:00  → 15.2°C
...

RÉSULTAT: Temp Min = 14.5°C (à 08:00)
```

### 📊 Formule
```
Temp Min = MIN(T₁, T₂, T₃, ..., Tₙ)

Exemple:
Temp Min = MIN(20.0, 21.5, ..., 15.0, 14.5, 14.8, 15.2, ...)
         = 14.5°C
```

### 🎓 Utilité

- **Nuit:** Savoir à quel point il fera froid la nuit
- **Chauffage:** Si min = 10°C, prévoir chauffage
- **Gel:** Si min < 0°C, risque de gelée

### 💾 Stockage MongoDB
```
Les données brutes sont sauvegardées:
{temperature: 15.0, timestamp: "09:00"}
{temperature: 14.5, timestamp: "08:00"} ← Min
{temperature: 14.8, timestamp: "07:00"}
...

Puis Python calcule: min(20.0, 21.5, ..., 14.5, ...) = 14.5°C
```

---

## **7️⃣ KPI: TEMPÉRATURE MOYENNE (°C)**

### 📌 Définition
La **moyenne arithmétique** de toutes les températures de la période.

### 📊 Code dans app.py
```python
df = pd.DataFrame(historical)
avg_temp = df['temperature'].mean()  # Moyenne

st.metric("📊 Temp Moy", f"{avg_temp:.1f}°C")
```

### 🔍 Source des données
```python
historical = db.get_historical_weather(selected_city, hours=time_range)
# Récupère TOUS les enregistrements de la période
# Puis calcule la moyenne
```

### 📈 Exemple concret

**Scenario:** Casablanca, 24 dernières heures
```
Temperatures enregistrées (24 points):
20.0, 21.5, 22.3, 23.1, 22.5, 21.0, 19.8, 17.2, 15.0, 14.5,
15.2, 16.5, 18.0, 19.5, 21.0, 22.5, 23.5, 22.8, 21.5, 20.0,
18.5, 17.0, 16.2, 15.8

SOMME = 20.0 + 21.5 + 22.3 + ... = 486.3°C
NOMBRE = 24 points
MOYENNE = 486.3 / 24 = 20.26°C

RÉSULTAT: Temp Moy = 20.3°C (arrondie à 1 décimale)
```

### 📊 Formule

```
Temp Moy = (T₁ + T₂ + T₃ + ... + Tₙ) / n

Où:
T₁, T₂, ... = chaque température
n = nombre total de mesures

Exemple:
Temp Moy = (20.0 + 21.5 + 22.3 + ... + 15.8) / 24
          = 486.3 / 24
          = 20.26°C
```

### 🎓 Utilité

- **Résumé:** Température "typique" de la journée
- **Comparaisons:** Jour 1 moy = 20°C, Jour 2 moy = 23°C
- **Tendances:** Si moyennes augmentent jour après jour = réchauffement
- **Normalisation:** Comparer avec moyenne historique (normale saisonnière)

### 📊 Interprétation

```
Si Max = 23.1°C, Min = 14.5°C, Moy = 20.3°C
    ↓
Amplitude = 23.1 - 14.5 = 8.6°C

Midi chaud (23°C), nuit froide (14.5°C)
Moyenne: 20.3°C = tendance générale

Écart = Max - Moy = 23.1 - 20.3 = 2.8°C
        = Il a fait 2.8°C au-dessus de la moyenne
```

### 💾 Stockage & Calcul

```
MongoDB stocke les valeurs brutes (chaque point)
Pandas calcule: df['temperature'].mean()
Résultat: 20.3°C
```

### ⚙️ Code Pandas Détaillé

```python
# 1. Récupérer les données
historical = db.get_historical_weather("Casablanca", hours=24)

# 2. Convertir en DataFrame
df = pd.DataFrame(historical)
#    _id         city           temperature timestamp
# 0  5f3a...  Casablanca       20.0        2026-01-25 14:00
# 1  5f3b...  Casablanca       21.5        2026-01-25 15:00
# 2  5f3c...  Casablanca       22.3        2026-01-25 16:00
# ...

# 3. Calculer la moyenne
avg_temp = df['temperature'].mean()
# Pandas additionne tous les éléments et divise par le nombre

# 4. Afficher avec 1 décimale
st.metric("📊 Temp Moy", f"{avg_temp:.1f}°C")
# Résultat: "20.3°C"
```

---

## **8️⃣ KPI: NOMBRE D'ENREGISTREMENTS**

### 📌 Définition
Le **nombre de points de données** collectés pendant la période sélectionnée.

Indique aussi la **fréquence de mise à jour** et la **couverture temporelle**.

### 📊 Code dans app.py
```python
df = pd.DataFrame(historical)
nb_records = len(df)  # Nombre de lignes

st.metric("📋 Enregistrements", nb_records)
```

### 🔍 Source des données
```python
historical = db.get_historical_weather(selected_city, hours=time_range)
# Retourne une liste de documents
nb_records = len(historical)  # Longueur de la liste
```

### 📈 Exemple concret

**Scenario:** Casablanca, 24 heures
```
Si mise à jour toutes les heures:
14:00  → Document 1
15:00  → Document 2
16:00  → Document 3
...
13:00 (lendemain) → Document 24

TOTAL: 24 enregistrements

RÉSULTAT AFFICHAGE:
┌──────────────┐
│ 📋 Nb records│
│      24      │
└──────────────┘
```

### 📊 Relation Nombre-Période

```
time_range = 1h   → ~1 document (1 mise à jour)
time_range = 6h   → ~6 documents (si 1/h)
time_range = 24h  → ~24 documents (si 1/h)
time_range = 72h  → ~72 documents (si 1/h)

Avec auto-refresh (1 min):
time_range = 24h  → ~1440 documents (24h × 60 min)
```

### 🎓 Utilité

- **Validité des graphiques:** Besoin au moins 2 points pour tracer une ligne
- **Qualité des données:** Plus d'enregistrements = meilleure analyse
- **Fréquence mise à jour:** 24 records en 24h = 1 par heure

### ⚙️ Code Pandas Détaillé

```python
# 1. Récupérer les données (24h)
historical = db.get_historical_weather("Casablanca", hours=24)
# Retourne: [doc1, doc2, doc3, ..., doc24]

# 2. Convertir en DataFrame
df = pd.DataFrame(historical)
# Crée une table avec colonnes: city, temperature, humidity, etc.
# 24 lignes (une par enregistrement)

# 3. Compter les lignes
nb_records = len(df)
# len([doc1, ..., doc24]) = 24

# 4. Afficher
st.metric("📋 Enregistrements", nb_records)
# Affiche: "24"
```

### 💾 Stockage MongoDB

```
Pour chaque mise à jour:
  update_weather_data(["Casablanca", ...])
    Pour Casablanca:
      db.save_weather_data({...})  ← 1 document inséré

Après 24h avec 1 mise à jour/heure:
  24 documents pour Casablanca dans weather_realtime

Query MongoDB:
db.weather_realtime.countDocuments({city: "Casablanca"})
// Retourne: 24 (ou plus, si plusieurs jours)
```

---

# 🔗 **RELATIONS ENTRE LES KPI**

## **Relation 1: Temp Max vs Min vs Moy**

```
┌─────────────────────────────────────┐
│ Graphique Température (24h)         │
├─────────────────────────────────────┤
│                     Max: 23.1°C
│                    /    \
│                   /      \
│         Moy: 20.3° -------\
│                 / \        \
│                /   \        \
│   Min: 14.5°C                ─────
│
│ Moy est toujours entre Min et Max
└─────────────────────────────────────┘

Formula:
Min ≤ Moy ≤ Max
14.5 ≤ 20.3 ≤ 23.1 ✓
```

## **Relation 2: Pression vs Météo**

```
Pression BAISSE (1020 → 1010 → 1000 hPa)
    ↓
Système dépressionnaire arrive
    ↓
Vent augmente
Humidité augmente
Température peut chuter
    ↓
Alerte tempête/orage


Pression HAUSSE (1000 → 1010 → 1020 hPa)
    ↓
Anticyclone (beau temps)
    ↓
Vent diminue
Humidité peut baisser
Température stable/augmente
    ↓
Beau temps persistent
```

## **Relation 3: Température vs Humidité**

```
Température AUGMENTE
    ↓
Air se dilate
Capacité à retenir l'eau augmente
Humidité RELATIVE baisse (si pas d'eau ajoutée)

Exemple:
Matin: 15°C, 75% humidité (moite)
Midi: 25°C, 45% humidité (sec mais même quantité d'eau!)

Point de rosée = même (eau réelle constante)
```

---

# 📊 **TABLEAU COMPLET DES 8 KPI**

| # | KPI | Unité | Dashboard | Type | Source | Formule/Extraction |
|---|-----|-------|-----------|------|--------|-------------------|
| 1 | Température | °C | 1 | Actuel | get_latest_weather() | latest['temperature'] |
| 2 | Humidité | % | 1 | Actuel | get_latest_weather() | latest['humidity'] |
| 3 | Vent | km/h | 1 | Actuel | get_latest_weather() | latest['wind_speed'] |
| 4 | Pression | hPa | 1 | Actuel | get_latest_weather() | latest['pressure'] |
| 5 | Temp Max | °C | 4 | Stat | get_historical_weather() | MAX(df['temperature']) |
| 6 | Temp Min | °C | 4 | Stat | get_historical_weather() | MIN(df['temperature']) |
| 7 | Temp Moy | °C | 4 | Stat | get_historical_weather() | MEAN(df['temperature']) |
| 8 | Enreg. | count | 4 | Stat | get_historical_weather() | len(df) |

---

# 🎯 **UTILISATION PRATIQUE DES KPI**

## **Cas 1: Planifier une sortie**
```
1. Vérifier Température (KPI 1) → 22°C
2. Vérifier Vent (KPI 3) → 15 km/h
3. Vérifier Humidité (KPI 2) → 65%

Conclusion: Beau temps, vêtements légers, peut sortir ✓
```

## **Cas 2: Surveillance météo**
```
1. Vérifier Pression (KPI 4) → 1000 hPa (en baisse)
2. Vérifier Vent (KPI 3) → 28 km/h (augmentation)
3. Regarder Temp Min (KPI 6) → 10°C

Conclusion: Tempête approche, ne pas sortir ✗
```

## **Cas 3: Analyse climatique**
```
1. Comparer Temp Moy (KPI 7) d'hier vs aujourd'hui
2. Vérifier Temp Max (KPI 5) et Min (KPI 6) pour amplitude
3. Compter Enregistrements (KPI 8) pour fiabilité

Conclusion: Évolution jour par jour du climat local
```

---

# 🔄 **CYCLE DE VIE D'UN KPI**

```
[1] API OpenWeatherMap récupère
     └─ {"temp": 22.5, "humidity": 65, ...}
        
[2] weather_service.py standardise
     └─ {"temperature": 22.5, "humidity": 65, ...}
     
[3] db.py sauvegarde dans MongoDB
     └─ {city: "Casablanca", temperature: 22.5, timestamp: ...}
     
[4] app.py récupère les données
     └─ latest = db.get_latest_weather("Casablanca")
     
[5] Streamlit affiche le KPI
     └─ ┌──────────────┐
        │ TEMPÉRATURE  │
        │   22.5°C     │
        └──────────────┘
        
[6] Utilisateur consulte le KPI
     └─ Prend décision basée sur la valeur
```

---

Vous avez besoin d'une explication supplémentaire sur un KPI spécifique? 🎯
