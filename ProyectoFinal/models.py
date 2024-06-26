from sqlalchemy import Column, Integer, String, DateTime
from database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    fecha_registro = Column(DateTime)

class Tarea(Base):
    __tablename__ = "tareas"

    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String, index=True)
    estado = Column(String, index=True)
    usuario_id = Column(Integer)
