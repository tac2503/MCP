from dotenv import load_dotenv
from sqlalchemy.exc import OperationalError

from .session import SessionLocal
from ..models.usuario import Usuario

load_dotenv()

USUARIO=[{
    "nombre": "Tomas Alvarez",
    "email":"tomas.alvarez@gmail.com"
}]

def create_usuario(db):
    for usuario in USUARIO:
        if db.query(Usuario).filter(Usuario.email == usuario["email"]).first():
            continue
        db.add(Usuario(nombre=usuario["nombre"], email=usuario["email"]))
    db.commit()
    
def main():
    try:
        db = SessionLocal()
        try:
            print("Creando Usuario...")
            create_usuario(db)
        finally:
            db.close()
    except OperationalError as e:
        print(f"Detalles del error: {e}")
        raise SystemExit(1) from e
    
if __name__ == "__main__":
    main()
    
        