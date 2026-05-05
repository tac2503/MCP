from ..db.session import SessionLocal
from ..db.crud import create_user, get_user_email, get_users

def get_user_by_email(email: str):
    user = get_user_email(SessionLocal(), email)
    if user:
        return {"nombre": user.nombre, "email": user.email}
    return None

def create_new_user(nombre: str, email: str):
    if not nombre or not email:
        return {"error": "Faltan datos obligatorios: nombre y email."}

    existing_user = get_user_email(SessionLocal(), email)
    if existing_user:
        return {"error": "El usuario con este email ya existe."}
    
    new_user = create_user(SessionLocal(), nombre, email)
    return {"nombre": new_user.nombre, "email": new_user.email}

def get_all_users():
    users = get_users(SessionLocal())

    if users:   
        return {
            "usuarios":[
                {"nombre": user.nombre, "email": user.email} for user in users
            ]
        }
    return None

