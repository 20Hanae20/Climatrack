"""
Module de Service API Météo - Climatrack Maroc
================================================
Récupère les données météorologiques en temps réel depuis des APIs externes.
Ce module supporte OpenWeatherMap et WeatherAPI avec un système de données simulées.
"""

import os  # Pour accéder aux variables d'environnement
import requests  # Pour effectuer les requêtes HTTP vers les APIs météo
from datetime import datetime  # Pour gérer les timestamps
from typing import Dict, Optional  # Pour le typage des fonctions
from dotenv import load_dotenv  # Pour charger les variables depuis le fichier .env

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

class WeatherService:
    """
    Service de récupération des données météorologiques.
    Gère les appels API vers OpenWeatherMap ou WeatherAPI.
    """
    
    def __init__(self):
        """
        Initialise le service météo avec les identifiants API.
        Charge la clé API et le fournisseur depuis les variables d'environnement.
        """
        # Récupérer la clé API depuis le fichier .env
        self.api_key = os.getenv("WEATHER_API_KEY", "")
        
        # Récupérer le fournisseur API (openweather ou weatherapi)
        self.provider = os.getenv("WEATHER_API_PROVIDER", "openweather")
        
    def fetch_weather(self, city: str) -> Optional[Dict]:
        """
        Récupère les données météo actuelles pour une ville.
        
        Args:
            city (str): Nom de la ville (ex: "Casablanca", "Rabat")
            
        Returns:
            Optional[Dict]: Dictionnaire avec les données météo standardisées ou None en cas d'erreur
        """
        # Vérifier quel fournisseur API utiliser
        if self.provider == "openweather":
            return self._fetch_openweather(city)
        elif self.provider == "weatherapi":
            return self._fetch_weatherapi(city)
        else:
            print(f"[ERREUR] Fournisseur inconnu: {self.provider}")
            return None
    
    def _fetch_openweather(self, city: str) -> Optional[Dict]:
        """
        Récupère les données depuis l'API OpenWeatherMap.
        
        Args:
            city (str): Nom de la ville
            
        Returns:
            Optional[Dict]: Données météo standardisées ou None
        """
        try:
            # URL de l'API OpenWeatherMap pour la météo actuelle
            url = "http://api.openweathermap.org/data/2.5/weather"
            
            # Paramètres de la requête
            params = {
                "q": city,  # Nom de la ville
                "appid": self.api_key,  # Clé API
                "units": "metric",  # Unités métriques (Celsius, km/h)
                "lang": "fr"  # Langue française pour les descriptions
            }
            
            # Effectuer la requête HTTP GET avec un timeout de 10 secondes
            response = requests.get(url, params=params, timeout=10)
            
            # Vérifier si la requête a réussi (code 200)
            response.raise_for_status()
            
            # Convertir la réponse JSON en dictionnaire Python
            data = response.json()
            
            # Standardiser la réponse dans un format uniforme
            return {
                "city": city,  # Nom de la ville
                "timestamp": datetime.now(),  # Horodatage actuel
                "temperature": data["main"]["temp"],  # Température en °C
                "humidity": data["main"]["humidity"],  # Humidité en %
                "pressure": data["main"]["pressure"],  # Pression en hPa
                "wind_speed": data["wind"]["speed"] * 3.6,  # Convertir m/s en km/h
                "weather": data["weather"][0]["main"],  # Condition principale (Clear, Rain, etc.)
                "description": data["weather"][0]["description"],  # Description détaillée
                "icon": data["weather"][0]["icon"]  # Code de l'icône météo
            }
            
        except requests.exceptions.RequestException as e:
            # Erreur lors de la requête HTTP (timeout, connexion, etc.)
            print(f"[ERREUR] Échec de la requête API pour {city}: {e}")
            return None
        except KeyError as e:
            # Erreur si la structure de la réponse est inattendue
            print(f"[ERREUR] Format de réponse API inattendu: {e}")
            return None
    
    def _fetch_weatherapi(self, city: str) -> Optional[Dict]:
        """
        Récupère les données depuis l'API WeatherAPI.com.
        
        Args:
            city (str): Nom de la ville
            
        Returns:
            Optional[Dict]: Données météo standardisées ou None
        """
        try:
            # URL de l'API WeatherAPI pour la météo actuelle
            url = "http://api.weatherapi.com/v1/current.json"
            
            # Paramètres de la requête
            params = {
                "key": self.api_key,  # Clé API
                "q": city,  # Nom de la ville
                "aqi": "no",  # Ne pas inclure l'indice de qualité de l'air
                "lang": "fr"  # Langue française
            }
            
            # Effectuer la requête HTTP GET
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Standardiser la réponse
            return {
                "city": city,
                "timestamp": datetime.now(),
                "temperature": data["current"]["temp_c"],  # Température en Celsius
                "humidity": data["current"]["humidity"],
                "pressure": data["current"]["pressure_mb"],  # Pression en millibars
                "wind_speed": data["current"]["wind_kph"],  # Vitesse du vent en km/h
                "weather": data["current"]["condition"]["text"],
                "description": data["current"]["condition"]["text"],
                "icon": data["current"]["condition"]["icon"]
            }
            
        except requests.exceptions.RequestException as e:
            print(f"[ERREUR] Échec de la requête API pour {city}: {e}")
            return None
        except KeyError as e:
            print(f"[ERREUR] Format de réponse API inattendu: {e}")
            return None
    
    def generate_mock_data(self, city: str) -> Dict:
        """
        Génère des données météo simulées pour les tests.
        Utile pour développer sans consommer de quota API.
        
        Args:
            city (str): Nom de la ville
            
        Returns:
            Dict: Données météo simulées réalistes
        """
        import random  # Pour générer des valeurs aléatoires
        
        # Températures de base réalistes pour les villes marocaines
        base_temps = {
            # Grandes métropoles
            "Casablanca": 19,
            "Rabat": 18,
            "Marrakech": 22,
            "Fès": 17,
            "Tanger": 16,
            "Agadir": 21,
            
            # Villes impériales et régionales
            "Meknès": 16,
            "Oujda": 15,
            "Tétouan": 17,
            "Kenitra": 18,
            
            # Villes côtières atlantiques
            "Essaouira": 18,
            "El Jadida": 19,
            "Safi": 19,
            "Mohammedia": 19,
            "Larache": 17,
            "Asilah": 17,
            
            # Villes côtières méditerranéennes
            "Nador": 17,
            "Al Hoceima": 18,
            
            # Villes de l'intérieur
            "Béni Mellal": 18,
            "Khouribga": 17,
            "Taza": 16,
            "Khemisset": 16,
            "Settat": 18,
            
            # Villes du Sud
            "Laâyoune": 22,
            "Dakhla": 21,
            "Guelmim": 23,
            "Tan-Tan": 22,
            "Taroudant": 21,
            "Ouarzazate": 20,
            
            # Autres villes importantes
            "Errachidia": 19,
            "Ifrane": 12,  # Plus fraîche (montagne)
            "Ksar El Kebir": 17
        }
        
        # Obtenir la température de base ou utiliser 20°C par défaut
        base_temp = base_temps.get(city, 20)
        
        # Générer des données aléatoires mais réalistes
        return {
            "city": city,
            "timestamp": datetime.now(),
            # Température avec variation de ±3°C
            "temperature": round(base_temp + random.uniform(-3, 3), 1),
            # Humidité entre 40% et 80%
            "humidity": random.randint(40, 80),
            # Pression atmosphérique entre 1005 et 1020 hPa
            "pressure": random.randint(1005, 1020),
            # Vitesse du vent entre 5 et 25 km/h
            "wind_speed": round(random.uniform(5, 25), 1),
            # Condition météo aléatoire
            "weather": random.choice(["Ensoleillé", "Nuageux", "Pluie", "Brume"]),
            # Description détaillée
            "description": random.choice([
                "ciel dégagé", 
                "quelques nuages", 
                "nuages épars", 
                "pluie légère",
                "brume"
            ]),
            "icon": "01d"  # Icône par défaut
        }


def update_weather_data(cities: list, db, use_mock: bool = False):
    """
    Récupère et sauvegarde les données météo pour plusieurs villes.
    Cette fonction est appelée pour mettre à jour la base de données.
    
    Args:
        cities (list): Liste des noms de villes
        db: Instance de la base de données MongoDB
        use_mock (bool): Si True, utilise des données simulées au lieu de l'API
    """
    # Créer une instance du service météo
    service = WeatherService()
    
    # Parcourir chaque ville
    for city in cities:
        # Vérifier si on utilise des données simulées ou réelles
        if use_mock or not service.api_key:
            # Générer des données simulées
            data = service.generate_mock_data(city)
            print(f"[MOCK] Données simulées générées pour {city}")
        else:
            # Récupérer les données réelles depuis l'API
            data = service.fetch_weather(city)
            
            if data:
                print(f"[OK] Météo récupérée pour {city}: {data['temperature']}°C")
            else:
                # En cas d'échec, utiliser des données simulées
                print(f"[ERREUR] Échec de récupération pour {city}, utilisation de données simulées")
                data = service.generate_mock_data(city)
        
        # Sauvegarder les données dans MongoDB si elles existent
        if data:
            db.save_weather_data(data)
