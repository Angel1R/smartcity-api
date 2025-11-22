from pymongo import MongoClient
from dotenv import load_dotenv
import os
import certifi

# Cargar variables de entorno
load_dotenv()

# Usar la URI de la variable de entorno (se configura en Render)
MONGO_URI = os.getenv("MONGO_URI")

# Cliente de Mongo
# Al cliente de Mongo le pasamos la ubicación de los certificados de confianza.
ca = certifi.where()
client = MongoClient(MONGO_URI, tlsCAFile=ca)

# Base de datos: SmartCitySecure
db = client["SmartCitySecure"]

# Colecciones basadas en tus diagramas
users_collection = db["usuarios"]           #
sensors_collection = db["sensores"]         #
luminaires_collection = db["luminarias"]    #
energy_collection = db["consumo_energia"]   #
alerts_collection = db["alertas_seguridad"] #