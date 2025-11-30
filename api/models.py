from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Literal, List

# --- 1. USUARIOS ---
class UserInput(BaseModel):
    nombre: str
    # CAMBIO: El rol es totalmente opcional ahora
    rol: Optional[str] = 'Usuario' 
    correo: EmailStr
    contrasena: str = Field(..., min_length=8)

class UserDB(UserInput):
    id_usuario: str

class LoginRequest(BaseModel):
    correo: str
    contrasena: str

# --- 2. POSTES ---
class Coordenadas(BaseModel):
    lat: float
    lng: float

class PosteInput(BaseModel):
    lamp_id: str             # Ej: "3_lamp_001"
    zona: int                # Ej: 3
    tipo_lampara: str        # Ej: "Halógena"
    consumo_kwh: float       # Ej: 0
    voltaje: int             # Ej: 240
    corriente: float         # Ej: 0.625
    potencia_w: int          # Ej: 150
    horas_funcionamiento: int # Ej: 10
    estado_tecnico: str      # Ej: "Inoperativo"
    
    # Nota: En tu BD la fecha está guardada como STRING ("2024-01-11...").
    # Lo dejamos como str para evitar errores de validación.
    fecha: str               
    
    estado: str              # Ej: "encendido"
    
    coordenadas: Optional[Coordenadas] = None


class PosteDB(PosteInput):
    _id: str