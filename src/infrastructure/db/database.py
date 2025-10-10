from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from contextlib import contextmanager
import os

# URL de la base de datos (puedes obtenerla de variables de entorno si lo deseas)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/ecommerce_chat.db")

# Motor de conexión a SQLite
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # Necesario para SQLite
)

# Factory de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base para modelos ORM
Base = declarative_base()

# Dependency para FastAPI (y otros usos): genera y cierra sesión correctamente
def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Inicializa BD y carga datos (crea las tablas si no existen)
def init_db():
    import src.infrastructure.db.models  # importa los modelos para que Base los conozca
    Base.metadata.create_all(bind=engine)