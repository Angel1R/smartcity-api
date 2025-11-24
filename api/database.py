from pymongo import MongoClient
from dotenv import load_dotenv
import os
import certifi

# Cargar variables de entorno
load_dotenv()

# Usar la URI de la variable de entorno
MONGO_URI = os.getenv("MONGO_URI")

# Configuración de certificados SSL para Render/Atlas
ca = certifi.where()
client = MongoClient(MONGO_URI, tlsCAFile=ca)

# Base de datos
db = client["SmartCitySecure"]

# --- COLECCIONES ACTUALIZADAS SEGÚN TU IMAGEN ---
users_collection = db["Usuarios"]      # Nueva colección principal 'Usuarios'
posts_collection = db["Postes"]        # Nueva colección principal 'Postes'

# Colecciones anteriores (Dejadas por referencia, puedes borrarlas si ya no existen)
# energy_collection = db["consumo_energia"]
# alerts_collection = db["alertas_seguridad"]