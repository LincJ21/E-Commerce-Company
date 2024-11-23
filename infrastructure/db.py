from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Configurar la URL de la base de datos
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:SKLYjqmQgbHpHWWxGHIEukBxFpPLipLQ@junction.proxy.rlwy.net:22062/railway")

# Crear el motor de la base de datos
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()