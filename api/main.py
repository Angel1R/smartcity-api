from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from bson import ObjectId
from typing import List
from passlib.context import CryptContext
import logging

# Importar modelos y base de datos locales
from models import (
    UserInput, UserDB, SensorInput, SensorDB,
    LuminaireInput, LuminaireDB, EnergyInput, EnergyDB,
    AlertInput, AlertDB
)
from database import (
    users_collection, sensors_collection, luminaires_collection,
    energy_collection, alerts_collection
)

# Configuración de seguridad para contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Inicializar App
app = FastAPI(title="SmartCity Secure API", version="1.0.0")

# CORS (Permitir acceso desde cualquier lado por ahora)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Funciones de ayuda ---
def hash_password(password: str):
    return pwd_context.hash(password)

def fix_id(doc):
    """Convierte el _id de Mongo a string para que Pydantic no falle"""
    doc["id"] = str(doc.pop("_id"))
    return doc

# --- RUTAS ---

@app.get("/")
def read_root():
    return {"Proyecto": "SmartCity Secure", "Status": "Online 🟢"}

# === 1. USUARIOS ===
@app.post("/usuarios/", response_model=UserDB)
def create_user(user: UserInput):
    user_dict = user.dict()
    user_dict["contrasena"] = hash_password(user.password) # Encriptar
    new_user = users_collection.insert_one(user_dict)
    created_user = users_collection.find_one({"_id": new_user.inserted_id})
    
    # Mapeo manual para ajustar al modelo de respuesta
    return UserDB(
        id_usuario=str(created_user["_id"]),
        nombre=created_user["nombre"],
        rol=created_user["rol"],
        correo=created_user["correo"],
        contrasena=created_user["contrasena"]
    )

@app.get("/usuarios/", response_model=List[UserDB])
def get_users():
    users = []
    for u in users_collection.find():
        users.append(UserDB(
            id_usuario=str(u["_id"]),
            nombre=u["nombre"],
            rol=u["rol"],
            correo=u["correo"],
            contrasena=u["contrasena"]
        ))
    return users

# === 2. SENSORES ===
@app.post("/sensores/", response_model=SensorDB)
def create_sensor(sensor: SensorInput):
    new_sensor = sensors_collection.insert_one(sensor.dict())
    created_sensor = sensors_collection.find_one({"_id": new_sensor.inserted_id})
    return SensorDB(id_sensor=str(created_sensor["_id"]), **sensor.dict())

@app.get("/sensores/", response_model=List[SensorDB])
def get_sensors():
    sensors = []
    for s in sensors_collection.find():
        sensors.append(SensorDB(id_sensor=str(s["_id"]), ubicacion=s["ubicacion"], estado=s["estado"], nivel_luz=s["nivel_luz"], fecha_registro=s["fecha_registro"]))
    return sensors

# === 3. LUMINARIAS ===
@app.post("/luminarias/", response_model=LuminaireDB)
def create_luminaire(lum: LuminaireInput):
    # Aquí podrías verificar si el sensor existe, pero lo dejaremos simple
    new_lum = luminaires_collection.insert_one(lum.dict())
    return LuminaireDB(id_luminaria=str(new_lum.inserted_id), **lum.dict())

@app.get("/luminarias/", response_model=List[LuminaireDB])
def get_luminaries():
    lums = []
    for l in luminaires_collection.find():
        lums.append(LuminaireDB(id_luminaria=str(l["_id"]), **{k:v for k,v in l.items() if k != "_id"}))
    return lums

# === 4. CONSUMO ===
@app.post("/consumo/", response_model=EnergyDB)
def create_energy_record(energy: EnergyInput):
    new_rec = energy_collection.insert_one(energy.dict())
    return EnergyDB(id_consumo=str(new_rec.inserted_id), **energy.dict())

@app.get("/consumo/", response_model=List[EnergyDB])
def get_energy_records():
    recs = []
    for r in energy_collection.find():
        recs.append(EnergyDB(id_consumo=str(r["_id"]), **{k:v for k,v in r.items() if k != "_id"}))
    return recs

# === 5. ALERTAS ===
@app.post("/alertas/", response_model=AlertDB)
def create_alert(alert: AlertInput):
    new_alert = alerts_collection.insert_one(alert.dict())
    return AlertDB(id_alerta=str(new_alert.inserted_id), **alert.dict())

@app.get("/alertas/", response_model=List[AlertDB])
def get_alerts():
    alerts = []
    for a in alerts_collection.find():
        alerts.append(AlertDB(id_alerta=str(a["_id"]), **{k:v for k,v in a.items() if k != "_id"}))
    return alerts