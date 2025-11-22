from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Literal
from datetime import datetime

# --- 1. Usuarios ---
class UserInput(BaseModel):
    nombre: str
    rol: Literal["Administrador", "Tecnico"] # Ejemplo de roles
    correo: EmailStr
    contrasena: str = Field(..., min_length=6)

class UserDB(UserInput):
    id_usuario: str # Representará el ObjectId de Mongo convertido a string
    
class LoginRequest(BaseModel):
    correo: str
    contrasena: str

# --- 2. Sensores ---
class SensorInput(BaseModel):
    ubicacion: str
    estado: Literal["Activo", "Inactivo"]
    nivel_luz: float
    fecha_registro: datetime = Field(default_factory=datetime.utcnow)

class SensorDB(SensorInput):
    id_sensor: str

# --- 3. Luminarias ---
class LuminaireInput(BaseModel):
    id_sensor: str # Referencia al sensor (FK simulada)
    estado: Literal["Encendida", "Apagada", "Falla"]
    consumo_actual: float
    ultima_actualizacion: datetime = Field(default_factory=datetime.utcnow)

class LuminaireDB(LuminaireInput):
    id_luminaria: str

# --- 4. Consumo de Energía ---
class EnergyInput(BaseModel):
    id_luminaria: str # Referencia a la luminaria (FK simulada)
    energia_consumida: float
    fecha_medicion: datetime = Field(default_factory=datetime.utcnow)
    alerta: Literal["Si", "No"]

class EnergyDB(EnergyInput):
    id_consumo: str

# --- 5. Alertas de Seguridad ---
class AlertInput(BaseModel):
    tipo_alerta: str # Ej: "Ciberataque", "Falla técnica"
    descripcion: str
    fecha_alerta: datetime = Field(default_factory=datetime.utcnow)
    estado: Literal["Pendiente", "Resuelto"]

class AlertDB(AlertInput):
    id_alerta: str