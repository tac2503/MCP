from sqlalchemy import Column,Integer,String
from ..db.session import Base

class Usuario(Base):
    __tablename__='usuarios'
    
    id= Column(Integer,primary_key=True,autoincrement=True)
    nombre = Column(String,nullable=False)
    email = Column(String,nullable=False,unique=True)