"""
Module de Base de Données MongoDB - Climatrack Maroc
====================================================
Gère toutes les opérations de base de données pour le stockage et la récupération
des données météorologiques en temps réel.
"""

import os  # Pour accéder aux variables d'environnement
from datetime import datetime, timedelta  # Pour gérer les dates et heures
from typing import List, Dict, Optional  # Pour le typage des fonctions
from pymongo import MongoClient, DESCENDING  # Client MongoDB et constantes
from dotenv import load_dotenv  # Pour charger les variables d'environnement

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

class WeatherDB:
    """
    Gestionnaire de base de données MongoDB pour les données météorologiques.
    Fournit des méthodes pour sauvegarder et récupérer les données météo.
    """
    
    def __init__(self):
        """
        Initialise la connexion à MongoDB.
        Configure l'URI de connexion depuis les variables d'environnement.
        """
        # Récupérer l'URI MongoDB depuis .env (par défaut: localhost)
        self.mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
        
        # Initialiser les variables de connexion
        self.client = None  # Client MongoDB
        self.db = None  # Base de données
        self.collection = None  # Collection pour les données météo
        
    def connect(self):
        """
        Établit la connexion à MongoDB.
        Crée la base de données 'climatrack' et la collection 'weather_realtime'.
        
        Returns:
            bool: True si la connexion réussit, False sinon
        """
        try:
            # Créer le client MongoDB avec l'URI de connexion
            self.client = MongoClient(self.mongo_uri)
            
            # Sélectionner la base de données 'climatrack'
            self.db = self.client["climatrack"]
            
            # Sélectionner la collection 'weather_realtime'
            self.collection = self.db["weather_realtime"]
            
            # Tester la connexion avec une commande ping
            self.client.admin.command('ping')
            
            print("[OK] Connexion MongoDB réussie")
            return True
            
        except Exception as e:
            # Afficher l'erreur si la connexion échoue
            print(f"[ERREUR] Échec de connexion MongoDB: {e}")
            return False
    
    def save_weather_data(self, data: Dict) -> bool:
        """
        Sauvegarde les données météo dans MongoDB.
        Chaque appel crée un nouveau document dans la collection.
        
        Args:
            data (Dict): Dictionnaire contenant les informations météo
                        (city, temperature, humidity, etc.)
            
        Returns:
            bool: True si la sauvegarde réussit, False sinon
        """
        try:
            # Ajouter un timestamp si absent
            if "timestamp" not in data:
                data["timestamp"] = datetime.now()
            
            # Insérer le document dans la collection
            self.collection.insert_one(data)
            
            return True
            
        except Exception as e:
            # Afficher l'erreur en cas d'échec
            print(f"Erreur de sauvegarde des données: {e}")
            return False
    
    def get_latest_weather(self, city: str) -> Optional[Dict]:
        """
        Récupère les données météo les plus récentes pour une ville.
        Utile pour afficher la météo actuelle.
        
        Args:
            city (str): Nom de la ville (ex: "Casablanca")
            
        Returns:
            Optional[Dict]: Dictionnaire avec les données météo ou None si aucune donnée
        """
        try:
            # Rechercher le document le plus récent pour cette ville
            # find_one() retourne un seul document
            # sort() trie par timestamp décroissant (le plus récent en premier)
            result = self.collection.find_one(
                {"city": city},  # Filtre: chercher cette ville
                sort=[("timestamp", DESCENDING)]  # Trier par date décroissante
            )
            
            return result
            
        except Exception as e:
            print(f"[ERREUR] Erreur de récupération des données: {e}")
            return None
    
    def get_historical_weather(
        self, 
        city: str, 
        hours: int = 24
    ) -> List[Dict]:
        """
        Récupère l'historique météo pour une ville sur une période donnée.
        Utilisé pour afficher les graphiques d'évolution temporelle.
        
        Args:
            city (str): Nom de la ville
            hours (int): Nombre d'heures à récupérer (par défaut: 24h)
            
        Returns:
            List[Dict]: Liste des documents météo triés par date croissante
        """
        try:
            # Calculer la date de début (maintenant - X heures)
            start_time = datetime.now() - timedelta(hours=hours)
            
            # Rechercher tous les documents correspondants
            # find() retourne un curseur (itérateur) de documents
            results = self.collection.find(
                {
                    "city": city,  # Filtre: cette ville
                    "timestamp": {"$gte": start_time}  # Timestamp >= date de début
                }
            ).sort("timestamp", 1)  # Trier par date croissante (1 = ascendant)
            
            # Convertir le curseur en liste
            return list(results)
            
        except Exception as e:
            print(f"[ERREUR] Erreur de récupération de l'historique: {e}")
            return []
    
    def get_all_cities(self) -> List[str]:
        """
        Récupère la liste de toutes les villes présentes dans la base de données.
        Utile pour remplir les menus déroulants de sélection.
        
        Returns:
            List[str]: Liste des noms de villes, triée alphabétiquement
        """
        try:
            # distinct() retourne toutes les valeurs uniques d'un champ
            cities = self.collection.distinct("city")
            
            # Trier la liste alphabétiquement
            return sorted(cities)
            
        except Exception as e:
            print(f"[ERREUR] Erreur de récupération des villes: {e}")
            return []
    
    def get_comparison_data(self, cities: List[str]) -> Dict[str, Dict]:
        """
        Récupère les données météo les plus récentes pour plusieurs villes.
        Utilisé pour le dashboard de comparaison multi-villes.
        
        Args:
            cities (List[str]): Liste des noms de villes à comparer
            
        Returns:
            Dict[str, Dict]: Dictionnaire mappant chaque ville à ses données météo
                            Exemple: {"Casablanca": {...}, "Rabat": {...}}
        """
        # Initialiser le dictionnaire de résultats
        result = {}
        
        # Pour chaque ville, récupérer les données les plus récentes
        for city in cities:
            data = self.get_latest_weather(city)
            
            # Ajouter au résultat seulement si des données existent
            if data:
                result[city] = data
                
        return result
    
    def close(self):
        """
        Ferme la connexion à MongoDB.
        Doit être appelé à la fin de l'utilisation pour libérer les ressources.
        """
        if self.client:
            self.client.close()
            print("[OK] Connexion MongoDB fermée")


# ============================================================================
# SINGLETON PATTERN
# ============================================================================
# Cette section implémente le pattern Singleton pour garantir qu'une seule
# instance de la base de données existe dans toute l'application.

# Variable globale pour stocker l'instance unique
_db_instance = None

def get_db() -> WeatherDB:
    """
    Récupère ou crée l'instance unique de la base de données.
    Pattern Singleton: garantit qu'une seule connexion MongoDB existe.
    
    Returns:
        WeatherDB: Instance unique de la base de données
    """
    global _db_instance  # Accéder à la variable globale
    
    # Si aucune instance n'existe, en créer une
    if _db_instance is None:
        _db_instance = WeatherDB()  # Créer l'instance
        _db_instance.connect()  # Établir la connexion
        
    # Retourner l'instance (nouvelle ou existante)
    return _db_instance
