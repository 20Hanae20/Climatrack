"""
 CLIMATRACK MAROC - Dashboard Météo en Temps Réel
===================================================
Application de visualisation météorologique interactive avec stockage MongoDB
et mise à jour en temps réel des données pour les villes marocaines.

Auteur: Hanae Chaiboub
Date: 2026
"""

# ============================================================================
# IMPORTS - Bibliothèques nécessaires
# ============================================================================

import streamlit as st  # Framework web pour créer l'interface
import pandas as pd  # Manipulation et analyse de données
import plotly.express as px  # Graphiques interactifs (express API)
import plotly.graph_objects as go  # Graphiques interactifs (API avancée)
from datetime import datetime, timedelta  # Gestion des dates et heures
import time  # Pour les délais et le timing

# Modules personnalisés du projet
from db import get_db  # Gestionnaire de base de données MongoDB
from weather_service import update_weather_data  # Service de récupération météo

# ============================================================================
# CONFIGURATION DE LA PAGE
# ============================================================================

st.set_page_config(
    page_title="ClimaTrack Maroc - Didier",  # Titre de l'onglet du navigateur
    page_icon="��🇦",  # Drapeau du Maroc
    layout="wide",  # Utiliser toute la largeur de l'écran
    initial_sidebar_state="expanded"  # Barre latérale ouverte par défaut
)

# ============================================================================
# CONSTANTES - Valeurs utilisées dans toute l'application
# ============================================================================

# Couleur de fond transparente pour les graphiques (évite la duplication)
TRANSPARENT_BG = 'rgba(0,0,0,0)'

# Liste complète des villes marocaines - Couverture nationale
MOROCCAN_CITIES = [
    # Grandes métropoles
    "Casablanca",      # Capitale économique
    "Rabat",           # Capitale administrative
    "Marrakech",       # Ville impériale et touristique
    "Fès",             # Ville impériale
    "Tanger",          # Ville du détroit
    "Agadir",          # Capitale du Souss
    
    # Villes impériales et régionales
    "Meknès",          # Ville impériale
    "Oujda",           # Capitale de l'Oriental
    "Tétouan",         # Capitale du Nord
    "Kenitra",         # Ville du Gharb
    
    # Villes côtières atlantiques
    "Essaouira",       # Ville côtière artistique
    "El Jadida",       # Ville côtière historique
    "Safi",            # Port de pêche
    "Mohammedia",      # Ville portuaire
    "Larache",         # Ville côtière nord
    "Asilah",          # Station balnéaire
    
    # Villes côtières méditerranéennes
    "Nador",           # Ville du Rif oriental
    "Al Hoceima",      # Perle de la Méditerranée
    
    # Villes de l'intérieur
    "Béni Mellal",     # Capitale du Tadla
    "Khouribga",       # Ville minière
    "Taza",            # Porte de l'Oriental
    "Khemisset",       # Ville du plateau central
    "Settat",          # Ville agricole
    
    # Villes du Sud
    "Laâyoune",        # Capitale des provinces du Sud
    "Dakhla",          # Ville saharienne côtière
    "Guelmim",         # Porte du désert
    "Tan-Tan",         # Ville saharienne
    "Taroudant",       # Petite Marrakech
    "Ouarzazate",      # Porte du désert
    
    # Autres villes importantes
    "Errachidia",      # Capitale du Tafilalet
    "Ifrane",          # Petite Suisse marocaine
    "Ksar El Kebir"    # Ville du Nord-Ouest
]

# Labels pour les métriques (évite la duplication)
LABEL_WIND_SPEED = "Wind Speed"
LABEL_HUMIDITY = "Humidity"
LABEL_TEMPERATURE = "Temperature"

# ============================================================================
# STYLES CSS PERSONNALISÉS
# ============================================================================

st.markdown("""
<style>
    /* ===== THÈME DARK CALME - MAROC ===== */
    :root {
        --night: #0f172a;
        --slate: #1e293b;
        --ink: #e2e8f0;
        --muted: #94a3b8;
        --border: #2b364a;
        --accent: #c79a61;
    }

    /* Arrière-plan principal - sombre et doux */
    .main {
        background: radial-gradient(circle at top, #182235 0%, #0b1220 60%, #070b13 100%);
        font-family: "Georgia", "Times New Roman", serif;
        color: var(--ink);
    }

    /* Cartes métriques - sobres */
    .stMetric {
        background: rgba(30, 41, 59, 0.85);
        border-radius: 10px;
        padding: 20px;
        border: 1px solid var(--border);
        box-shadow: 0 2px 10px rgba(15, 23, 42, 0.4);
    }

    /* Labels des métriques */
    .stMetric label {
        color: var(--muted) !important;
        font-weight: 600 !important;
        font-size: 0.8rem !important;
        text-transform: uppercase;
        letter-spacing: 0.4px;
    }

    /* Valeurs des métriques */
    .stMetric [data-testid="stMetricValue"] {
        color: var(--ink) !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
    }

    /* Titres */
    h1 {
        color: var(--ink) !important;
        font-weight: 700 !important;
        letter-spacing: -0.3px;
    }

    h2, h3 {
        color: var(--ink) !important;
        font-weight: 600 !important;
    }

    /* Onglets - calme */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background: rgba(30, 41, 59, 0.6);
        padding: 6px;
        border-radius: 10px;
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        color: var(--muted);
        padding: 10px 20px;
        font-weight: 600;
        transition: all 0.2s ease;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(199, 154, 97, 0.15);
        color: var(--ink);
    }

    .stTabs [aria-selected="true"] {
        background: rgba(30, 41, 59, 0.9) !important;
        color: var(--ink) !important;
        border: 1px solid var(--border);
        box-shadow: 0 2px 6px rgba(15, 23, 42, 0.5);
    }

    /* Sidebar - texte clair */
    .css-1d391kg, [data-testid="stSidebar"] {
        background: #0d1626;
        border-right: 1px solid var(--border);
    }

    [data-testid="stSidebar"] * {
        color: var(--ink) !important;
    }

    /* Boutons */
    .stButton button {
        border-radius: 6px;
        font-weight: 600;
        background: var(--accent);
        color: #1b1f2a;
        border: 1px solid #a87f4b;
    }

    .stButton button:hover {
        background: #b88952;
        border-color: #916a3a;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# INITIALISATION DE LA BASE DE DONNÉES
# ============================================================================

@st.cache_resource  # Cache la connexion pour éviter les reconnexions
def init_database():
    """
    Initialise et retourne la connexion à la base de données MongoDB.
    Utilise le cache Streamlit pour ne créer qu'une seule connexion.
    
    Returns:
        WeatherDB: Instance de la base de données
    """
    db = get_db()  # Récupérer l'instance singleton
    return db

# Créer la connexion à la base de données
db = init_database()

# ============================================================================
# INTERFACE UTILISATEUR - BARRE LATÉRALE (SIDEBAR)
# ============================================================================

st.sidebar.title("Configuration")

# Utiliser uniquement les villes marocaines pour la configuration
available_cities = MOROCCAN_CITIES

# --- Sélection de ville unique ---
selected_city = st.sidebar.selectbox(
    "Ville sélectionnée",  # Label professionnel
    options=available_cities,  # Liste des options
    index=0  # Index par défaut (première ville)
)

# --- Sélection multi-villes pour la comparaison ---
comparison_cities = st.sidebar.multiselect(
    "Comparaison multi-villes",  # Label professionnel
    options=available_cities,  # Liste des options
    # Par défaut: sélectionner les 3 premières villes
    default=available_cities[:3] if len(available_cities) >= 3 else available_cities
)

# --- Sélecteur de plage temporelle ---
time_range = st.sidebar.slider(
    "Plage temporelle (heures)",  # Label professionnel
    min_value=1,  # Minimum: 1 heure
    max_value=72,  # Maximum: 72 heures (3 jours)
    value=24,  # Valeur par défaut: 24 heures
    step=1  # Incrément de 1 heure
)

# ============================================================================
# CONTRÔLES DE RAFRAÎCHISSEMENT DES DONNÉES
# ============================================================================

st.sidebar.markdown("---")  # Ligne de séparation
st.sidebar.subheader("Mise à jour des données")

# Case à cocher pour utiliser des données simulées
use_mock = st.sidebar.checkbox(
    "Utiliser données simulées (test)", 
    value=False  # Désactivé par défaut pour utiliser l'API réelle
)

# Bouton de rafraîchissement manuel
if st.sidebar.button("Actualiser maintenant"):
    with st.spinner("Récupération des données météo..."):
        # Mettre à jour les données pour toutes les villes disponibles
        update_weather_data(available_cities, db, use_mock=use_mock)
        st.sidebar.success("Données mises à jour avec succès")
        time.sleep(1)  # Pause de 1 seconde
        st.rerun()  # Recharger l'application pour afficher les nouvelles données

# Case à cocher pour l'auto-rafraîchissement
auto_refresh = st.sidebar.checkbox("Auto-refresh (1 min)", value=False)

# Si l'auto-refresh est activé
if auto_refresh:
    st.sidebar.info("Actualisation automatique activée (1 min)")
    time.sleep(60)  # Attendre 60 secondes
    # Mettre à jour les données
    update_weather_data(available_cities, db, use_mock=use_mock)
    st.rerun()  # Recharger l'application

# ============================================================================
# EN-TÊTE PRINCIPAL
# ============================================================================

st.title("CLIMATRACK MAROC")
st.markdown("### Didier au Maroc · Système météo classique et simple")
st.caption(" réalisé par Hanae Chaiboub")

# ============================================================================
# CRÉATION DES ONGLETS (TABS) - 4 DASHBOARDS
# ============================================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "Vue Générale",      # Dashboard 1: Données actuelles
    "Tendances",         # Dashboard 2: Évolution temporelle
    "Comparaison",       # Dashboard 3: Multi-villes
    "Historique"         # Dashboard 4: Tableau de données
])

# ============================================================================
# DASHBOARD 1: VUE GÉNÉRALE (DONNÉES ACTUELLES)
# ============================================================================

with tab1:
    st.header(f"Conditions Météorologiques Actuelles - {selected_city}")
    
    # Récupérer les données les plus récentes pour la ville sélectionnée
    latest = db.get_latest_weather(selected_city)
    
    if latest:
        # --- CARTES KPI (Key Performance Indicators) ---
        # Créer 4 colonnes de même largeur
        col1, col2, col3, col4 = st.columns(4)
        
        # Colonne 1: Température
        with col1:
            st.metric(
                label="TEMPÉRATURE",
                value=f"{latest['temperature']:.1f}°C",  # Format: 1 décimale
                delta=None  # Pas de variation affichée
            )
        
        # Colonne 2: Humidité
        with col2:
            st.metric(
                label="HUMIDITÉ",
                value=f"{latest['humidity']}%",
                delta=None
            )
        
        # Colonne 3: Vitesse du vent
        with col3:
            st.metric(
                label="VENT",
                value=f"{latest['wind_speed']:.1f} km/h",
                delta=None
            )
        
        # Colonne 4: Pression atmosphérique
        with col4:
            st.metric(
                label="PRESSION",
                value=f"{latest['pressure']} hPa",
                delta=None
            )
        
        # --- SECTION DÉTAILS MÉTÉO ---
        st.markdown("---")  # Ligne de séparation
        col1, col2 = st.columns([2, 1])  # 2/3 et 1/3 de largeur
        
        # Colonne gauche: Conditions météo
        with col1:
            st.subheader("Conditions Actuelles")
            st.markdown(f"**{latest['weather']}** - {latest['description'].capitalize()}")
            # Afficher l'horodatage de la dernière mise à jour
            st.caption(f"Dernière mise à jour: {latest['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Colonne droite: Indicateur météo textuel professionnel
        with col2:
            # Dictionnaire de correspondance condition -> description professionnelle
            weather_status = {
                "Clear": "Ciel Dégagé",
                "Ensoleillé": "Ciel Dégagé",
                "Clouds": "Nuageux",
                "Nuageux": "Nuageux",
                "Rain": "Pluvieux",
                "Pluie": "Pluvieux",
                "Mist": "Brumeux",
                "Brume": "Brumeux",
                "Snow": "Neigeux",
                "Neige": "Neigeux",
                "Thunderstorm": "Orageux",
                "Orage": "Orageux"
            }
            # Récupérer le statut correspondant ou utiliser la valeur par défaut
            status = weather_status.get(latest['weather'], "Variable")
            # Afficher le statut de manière professionnelle
            st.markdown(
                f"<div style='text-align: center; padding: 16px; background: #111827; border-radius: 8px; border: 1px solid #2b364a;'>"
                f"<h2 style='margin: 0; color: #e2e8f0;'>{status}</h2>"
                f"</div>",
                unsafe_allow_html=True
            )
    else:
        # Aucune donnée disponible
        st.warning(
            f"Aucune donnée disponible pour {selected_city}. "
            "Cliquez sur 'Actualiser maintenant' pour récupérer les données météo."
        )

# ============================================================================
# DASHBOARD 2: TENDANCES & ÉVOLUTION TEMPORELLE
# ============================================================================

with tab2:
    st.header(f"Analyse des Tendances Météorologiques - {selected_city}")
    
    # Récupérer l'historique météo pour la plage temporelle sélectionnée
    historical = db.get_historical_weather(selected_city, hours=time_range)
    
    # Vérifier qu'il y a au moins 2 points de données pour tracer un graphique
    if historical and len(historical) > 1:
        # Convertir les données en DataFrame pandas pour faciliter la manipulation
        df = pd.DataFrame(historical)
        # Convertir la colonne timestamp en type datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # --- GRAPHIQUE 1: ÉVOLUTION DE LA TEMPÉRATURE ---
        fig_temp = px.line(
            df,  # DataFrame source
            x='timestamp',  # Axe X: temps
            y='temperature',  # Axe Y: température
            title='Évolution de la Température',  # Titre du graphique
            labels={
                'temperature': 'Température (°C)',  # Label axe Y
                'timestamp': 'Temps'  # Label axe X
            }
        )
        # Personnaliser la ligne
        fig_temp.update_traces(
            line_color='#FF6B6B',  # Couleur rouge-orangé
            line_width=3  # Épaisseur de la ligne
        )
        # Personnaliser le style du graphique
        fig_temp.update_layout(
            plot_bgcolor=TRANSPARENT_BG,  # Fond transparent
            paper_bgcolor=TRANSPARENT_BG,  # Papier transparent
            font={'color': '#e2e8f0'},  # Texte clair
            hovermode='x unified'  # Tooltip unifié sur l'axe X
        )
        # Afficher le graphique (pleine largeur)
        st.plotly_chart(fig_temp, use_container_width=True)
        
        # --- GRAPHIQUE 2: HUMIDITÉ & VENT (DOUBLE AXE Y) ---
        fig_multi = go.Figure()  # Créer une figure vide
        
        # Ajouter la trace pour l'humidité (axe Y gauche)
        fig_multi.add_trace(go.Scatter(
            x=df['timestamp'],  # Axe X
            y=df['humidity'],  # Axe Y
            name='Humidité (%)',  # Nom dans la légende
            line={'color': '#4ECDC4', 'width': 2}  # Style de ligne
        ))
        
        # Ajouter la trace pour le vent (axe Y droit)
        fig_multi.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['wind_speed'],
            name='Vent (km/h)',
            line={'color': '#95E1D3', 'width': 2},
            yaxis='y2'  # Utiliser le deuxième axe Y
        ))
        
        # Configuration du layout avec double axe Y
        fig_multi.update_layout(
            title='Humidité et Vitesse du Vent',
            plot_bgcolor=TRANSPARENT_BG,
            paper_bgcolor=TRANSPARENT_BG,
            font={'color': '#e2e8f0'},
            hovermode='x unified',
            yaxis={'title': 'Humidité (%)'},  # Axe Y gauche
            yaxis2={  # Axe Y droit
                'title': 'Vent (km/h)',
                'overlaying': 'y',  # Superposer sur le même graphique
                'side': 'right'  # Positionner à droite
            }
        )
        
        st.plotly_chart(fig_multi, use_container_width=True)
        
        # --- ANALYSE AUTOMATIQUE ---
        st.markdown("---")
        st.subheader("Analyse Automatique")
        
        # Calculer la variation de température
        temp_change = df['temperature'].iloc[-1] - df['temperature'].iloc[0]
        
        # Déterminer la tendance de pression
        pressure_trend = "en hausse" if df['pressure'].iloc[-1] > df['pressure'].iloc[0] else "en baisse"
        
        # Afficher les insights
        st.info(
            f"La température a {'augmenté' if temp_change > 0 else 'diminué'} "
            f"de {abs(temp_change):.1f}°C sur les {time_range} dernières heures."
        )
        st.info(f"La pression atmosphérique est {pressure_trend}.")
        
        # Alerte vent fort
        if df['wind_speed'].max() > 20:
            st.warning(
                f"Vents forts détectés ! "
                f"Pic: {df['wind_speed'].max():.1f} km/h"
            )
    else:
        # Données insuffisantes
        st.warning(
            f"Données historiques insuffisantes pour {selected_city}. "
            "Les données doivent être collectées sur une période de temps."
        )

# ============================================================================
# DASHBOARD 3: COMPARAISON MULTI-VILLES
# ============================================================================

with tab3:
    st.header("Comparaison Multi-Villes")
    
    # Vérifier qu'au moins une ville est sélectionnée
    if comparison_cities:
        # Récupérer les données pour toutes les villes sélectionnées
        comparison_data = db.get_comparison_data(comparison_cities)
        
        if comparison_data:
            # Créer un DataFrame pour la comparaison
            comp_df = pd.DataFrame([
                {
                    'Ville': city,
                    LABEL_TEMPERATURE: data['temperature'],
                    LABEL_HUMIDITY: data['humidity'],
                    LABEL_WIND_SPEED: data['wind_speed'],
                    'Pression': data['pressure']
                }
                for city, data in comparison_data.items()
            ])
            
            # --- GRAPHIQUE 1: COMPARAISON DES TEMPÉRATURES ---
            fig_comp_temp = px.bar(
                comp_df,
                x='Ville',
                y=LABEL_TEMPERATURE,
                title='Comparaison des Températures',
                color=LABEL_TEMPERATURE,  # Couleur basée sur la température
                color_continuous_scale='RdYlBu_r'  # Palette: Rouge (chaud) -> Bleu (froid)
            )
            fig_comp_temp.update_layout(
                plot_bgcolor=TRANSPARENT_BG,
                paper_bgcolor=TRANSPARENT_BG,
                font={'color': '#e2e8f0'}
            )
            st.plotly_chart(fig_comp_temp, use_container_width=True)
            
            # --- GRAPHIQUES 2 & 3: HUMIDITÉ ET VENT (CÔTE À CÔTE) ---
            col1, col2 = st.columns(2)
            
            # Colonne gauche: Humidité
            with col1:
                fig_humidity = px.bar(
                    comp_df,
                    x='Ville',
                    y=LABEL_HUMIDITY,
                    title='Comparaison de l\'Humidité',
                    color=LABEL_HUMIDITY,
                    color_continuous_scale='Blues'  # Palette bleue
                )
                fig_humidity.update_layout(
                    plot_bgcolor=TRANSPARENT_BG,
                    paper_bgcolor=TRANSPARENT_BG,
                    font={'color': '#e2e8f0'}
                )
                st.plotly_chart(fig_humidity, use_container_width=True)
            
            # Colonne droite: Vent
            with col2:
                fig_wind = px.bar(
                    comp_df,
                    x='Ville',
                    y=LABEL_WIND_SPEED,
                    title='Comparaison du Vent',
                    color=LABEL_WIND_SPEED,
                    color_continuous_scale='Greens'  # Palette verte
                )
                fig_wind.update_layout(
                    plot_bgcolor=TRANSPARENT_BG,
                    paper_bgcolor=TRANSPARENT_BG,
                    font={'color': '#e2e8f0'}
                )
                st.plotly_chart(fig_wind, use_container_width=True)
            
            # --- ANALYSE COMPARATIVE AUTOMATIQUE ---
            st.markdown("---")
            st.subheader("Analyse Comparative")
            
            # Identifier les extrêmes
            hottest = comp_df.loc[comp_df[LABEL_TEMPERATURE].idxmax()]
            coldest = comp_df.loc[comp_df[LABEL_TEMPERATURE].idxmin()]
            windiest = comp_df.loc[comp_df[LABEL_WIND_SPEED].idxmax()]
            
            # Afficher les résultats en 3 colonnes
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.success(
                    f"Plus chaud: **{hottest['Ville']}** "
                    f"({hottest[LABEL_TEMPERATURE]:.1f}°C)"
                )
            
            with col2:
                st.info(
                    f"Plus froid: **{coldest['Ville']}** "
                    f"({coldest[LABEL_TEMPERATURE]:.1f}°C)"
                )
            
            with col3:
                st.warning(
                    f"Plus venteux: **{windiest['Ville']}** "
                    f"({windiest[LABEL_WIND_SPEED]:.1f} km/h)"
                )
        else:
            st.warning("Aucune donnée de comparaison disponible. Actualisez les données.")
    else:
        st.info("Sélectionnez des villes dans la barre latérale pour les comparer.")

# ============================================================================
# DASHBOARD 4: HISTORIQUE & TABLEAU DE DONNÉES
# ============================================================================

with tab4:
    st.header("Données Historiques")
    
    # Récupérer l'historique
    historical = db.get_historical_weather(selected_city, hours=time_range)
    
    if historical:
        # Convertir en DataFrame
        df = pd.DataFrame(historical)
        
        # Supprimer le champ _id de MongoDB (non nécessaire pour l'affichage)
        if '_id' in df.columns:
            df = df.drop('_id', axis=1)
        
        # Formater le timestamp en chaîne lisible
        df['timestamp'] = pd.to_datetime(df['timestamp']).dt.strftime('%Y-%m-%d %H:%M:%S')
        
        # Réorganiser les colonnes dans un ordre logique
        column_order = [
            'timestamp', 'city', 'temperature', 'humidity', 
            'pressure', 'wind_speed', 'weather', 'description'
        ]
        # Garder seulement les colonnes qui existent
        df = df[[col for col in column_order if col in df.columns]]
        
        # Afficher le tableau interactif
        st.dataframe(
            df,
            use_container_width=True,  # Utiliser toute la largeur
            height=400  # Hauteur fixe avec scroll
        )
        
        # --- STATISTIQUES RÉSUMÉES ---
        st.markdown("---")
        st.subheader(" Statistiques")
        
        # Afficher 4 métriques statistiques
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Temp Max", f"{df['temperature'].max():.1f}°C")
        
        with col2:
            st.metric("Temp Min", f"{df['temperature'].min():.1f}°C")
        
        with col3:
            st.metric("Temp Moy", f"{df['temperature'].mean():.1f}°C")
        
        with col4:
            st.metric("Enregistrements", len(df))
        
        # --- EXPORT CSV ---
        st.markdown("---")
        
        # Convertir le DataFrame en CSV
        csv = df.to_csv(index=False).encode('utf-8')
        
        # Bouton de téléchargement
        st.download_button(
            label="Télécharger CSV",
            data=csv,
            file_name=f"climatrack_{selected_city}_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    else:
        st.warning(f"Aucune donnée historique pour {selected_city}.")

# ============================================================================
# PIED DE PAGE
# ============================================================================

st.markdown("---")
