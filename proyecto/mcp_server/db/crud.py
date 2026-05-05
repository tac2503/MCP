from .session import SessionLocal
from ..models.usuario import Usuario

def create_user(db: SessionLocal, nombre: str, email: str):
    new_user = Usuario(nombre=nombre, email=email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user_email(db: SessionLocal, email: str):
    user = db.query(Usuario).filter(Usuario.email == email).first()
    if user:
        return user
    return None

def get_users(db: SessionLocal):
    users = db.query(Usuario).all()
    return users if users else None