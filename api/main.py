from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from passlib.context import CryptContext

# Importar modelos y base de datos locales
from models import (
    UserInput, UserDB, LoginRequest,
    PosteInput, PosteDB
)
from database import (
    users_collection, posts_collection
)

# Configuración de seguridad
pwd_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")

app = FastAPI(title="SmartCity Secure API", version="2.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === RUTA DE PING (KEEP-ALIVE) ===
@app.get("/ping")
def ping():
    """Ruta ligera para mantener el servidor despierto"""
    return {"status": "awake", "mensaje": "Pong!"}

# --- Funciones de ayuda ---
def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# --- RUTAS ---

@app.get("/")
def read_root():
    return {"Proyecto": "SmartCity Secure", "Status": "Database Updated 🟢"}

# === 1. USUARIOS (Actualizado: Rol Opcional) ===
@app.post("/usuarios/")
async def create_user(user: UserInput):
    # Validar si ya existe
    existing = users_collection.find_one({"correo": user.correo})
    if existing:
        raise HTTPException(status_code=400, detail="Correo ya registrado")

    hashed = pwd_context.hash(user.contrasena)

    nuevo = {
        "nombre": user.nombre,
        "correo": user.correo,
        "contrasena": hashed,
        "rol": user.rol
    }

    users_collection.insert_one(nuevo)

    return {"mensaje": "Usuario creado", "usuario": user.correo}


@app.get("/usuarios/", response_model=List[UserDB])
def get_users():
    users = []
    for u in users_collection.find():
        users.append(UserDB(
            id_usuario=str(u["_id"]),
            nombre=u["nombre"],
            rol=u.get("rol"),
            correo=u["correo"],
            contrasena=u["contrasena"]
        ))
    return users

# === RUTA DE LOGIN ===
@app.post("/login")
def login(credentials: LoginRequest):
    user = users_collection.find_one({"correo": credentials.correo})
    
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    if not verify_password(credentials.contrasena, user["contrasena"]):
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")
    
    return {
        "mensaje": "Login exitoso",
        "id_usuario": str(user["_id"]),
        "nombre": user["nombre"],
        "rol": user.get("rol"), # Puede ser None
        "status": "ok"
    }

# === 2. POSTES (Nueva colección unificada) ===
@app.post("/postes/", response_model=PosteDB)
def create_poste(poste: PosteInput):
    result = posts_collection.insert_one(poste.dict())
    created = posts_collection.find_one({"_id": result.inserted_id})
    created["_id"] = str(created["_id"])
    return created


@app.get("/postes/", response_model=List[PosteDB])
def get_postes():
    postes = []
    for p in posts_collection.find():
        p["_id"] = str(p["_id"])  # convertir ObjectId a string para que FastAPI no lo elimine
        postes.append(p)
    return postes
