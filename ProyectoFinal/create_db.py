from database import engine, Base
from models import Usuario, Tarea  # Importa las clases que has definido

Base.metadata.create_all(bind=engine)
