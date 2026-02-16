
from src.models.Pelicula import Pelicula
from sqlmodel import SQLModel, Session, create_engine
import os
from dotenv import load_dotenv

load_dotenv()

db_user: str = os.getenv("DB_USER")  
db_password: str = os.getenv("DB_PASSWORD")
db_server: str = os.getenv("DB_SERVER", "localhost")
db_port: int = int(os.getenv("DB_PORT", 5432))  
db_name: str = os.getenv("DB_NAME", "peliculasdb")  

DATABASE_URL = f"mysql+pymysql://{db_user}:{db_password}@{db_server}:{db_port}/{db_name}"
engine = create_engine(os.getenv("DB_URL", DATABASE_URL), echo=True)

def get_session():
    with Session(engine) as session:
        yield session


def init_db():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        session.add(Pelicula(
            id=1,
            titulo="Interestellar",
            sinopsis="Un grupo de exploradores viaja a través de un agujero de gusano...",
            director="Christopher Nolan",

            genero="ciencia_ficcion",
            clasificacion="PG-13",
            duracion_min=169,
            presupuesto_millones=165.0,
            disponible=True,
            fecha_estreno="2014-11-07",
            creado_en="2014-10-01T12:00:00",
            puntuacion=8.6
        ))
        session.commit()