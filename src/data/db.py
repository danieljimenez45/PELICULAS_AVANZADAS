"""
Módulo de configuración y gestión de la base de datos.
Maneja la conexión a PostgreSQL y la inicialización de las tablas.
"""

from models.Pelicula import Pelicula
from sqlmodel import SQLModel, Session, create_engine
import os
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env
# Esto permite configurar la conexión a la BD sin hardcodear valores
load_dotenv()

# ============================================================================
# Configuración de conexión a la base de datos
# ============================================================================

# Lee las credenciales y configuración de la BD desde variables de entorno
# os.getenv() obtiene el valor de la variable, o usa un valor por defecto si no existe
db_user: str = os.getenv("DB_USER")  
# Usuario de la base de datos PostgreSQL

db_password: str = os.getenv("DB_PASSWORD")
# Contraseña del usuario de la base de datos

db_server: str = os.getenv("DB_SERVER", "db-peliculas-avanzadas")
# Servidor/host de la BD (por defecto: nombre del contenedor Docker)

db_port: int = int(os.getenv("DB_PORT", 5432))  
# Puerto de PostgreSQL (por defecto: 5432, el estándar de PostgreSQL)

db_name: str = os.getenv("DB_NAME", "peliculasdb")  
# Nombre de la base de datos

# Construye la URL de conexión en formato SQLAlchemy/SQLModel
# Formato: postgresql+psycopg2://usuario:contraseña@servidor:puerto/nombre_bd
DATABASE_URL = f"postgresql+psycopg2://{db_user}:{db_password}@{db_server}:{db_port}/{db_name}"

# Crea el motor de SQLModel/SQLAlchemy que gestiona la conexión a la BD
# echo=True activa el logging de todas las consultas SQL (útil para debugging)
engine = create_engine(os.getenv("DB_URL", DATABASE_URL), echo=True)

def get_session():
    """
    Función generadora que proporciona una sesión de base de datos.
    
    Se usa como dependencia en FastAPI para inyectar la sesión en las rutas.
    Utiliza un context manager (with) para asegurar que la sesión se cierre correctamente.
    
    Yields:
        Session: Sesión de SQLModel lista para usar en operaciones de BD.
    
    Ejemplo de uso:
        @app.get("/ruta")
        def mi_ruta(session: Session = Depends(get_session)):
            # Usar session aquí
    """
    # with Session(engine) crea una sesión y la cierra automáticamente al salir
    # yield permite que FastAPI use esta función como generador para dependency injection
    with Session(engine) as session:
        yield session


def init_db():
    """
    Inicializa la base de datos: elimina tablas existentes, crea nuevas tablas
    e inserta datos iniciales (películas de ejemplo).
    
    Esta función se ejecuta al iniciar la aplicación (en el lifespan de FastAPI).
    ⚠️ ADVERTENCIA: drop_all() elimina TODAS las tablas existentes.
    """
    # Elimina todas las tablas existentes (¡CUIDADO en producción!)
    # Útil para desarrollo, pero peligroso en producción
    SQLModel.metadata.drop_all(engine)
    
    # Crea todas las tablas definidas en los modelos SQLModel
    # Lee los modelos con table=True y crea las tablas correspondientes
    SQLModel.metadata.create_all(engine)
    
    # Crea una sesión para insertar datos iniciales
    with Session(engine) as session:
        # ========================================================================
        # Película 1: Interestellar
        # ========================================================================
        session.add(Pelicula(
            id=1,
            titulo="Interestellar",
            sinopsis="Un grupo de exploradores viaja a través de un agujero de gusano en el espacio en un intento de asegurar la supervivencia de la humanidad.",
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
        
        # ========================================================================
        # Película 2: El Padrino
        # ========================================================================
        session.add(Pelicula(
            id=2,
            titulo="El Padrino",
            sinopsis="La historia de una familia de la mafia italiana en Nueva York y su patriarca, Don Vito Corleone.",
            director="Francis Ford Coppola",
            genero="drama",
            clasificacion="R",
            duracion_min=175,
            presupuesto_millones=6.0,
            disponible=True,
            fecha_estreno="1972-03-24",
            creado_en="1972-01-01T10:00:00",
            puntuacion=9.2
        ))
        
        # ========================================================================
        # Película 3: Matrix
        # ========================================================================
        session.add(Pelicula(
            id=3,
            titulo="Matrix",
            sinopsis="Un programador descubre que la realidad que conoce es una simulación creada por máquinas inteligentes.",
            director="Lana Wachowski, Lilly Wachowski",
            genero="ciencia_ficcion",
            clasificacion="R",
            duracion_min=136,
            presupuesto_millones=63.0,
            disponible=True,
            fecha_estreno="1999-03-31",
            creado_en="1999-01-15T14:30:00",
            puntuacion=8.7
        ))
        
        # ========================================================================
        # Película 4: Pulp Fiction
        # ========================================================================
        session.add(Pelicula(
            id=4,
            titulo="Pulp Fiction",
            sinopsis="Las historias entrelazadas de varios criminales en Los Ángeles, contadas de forma no lineal.",
            director="Quentin Tarantino",
            genero="accion",
            clasificacion="R",
            duracion_min=154,
            presupuesto_millones=8.0,
            disponible=True,
            fecha_estreno="1994-10-14",
            creado_en="1994-08-20T16:00:00",
            puntuacion=8.9
        ))
        
        # ========================================================================
        # Película 5: El Señor de los Anillos: La Comunidad del Anillo
        # ========================================================================
        session.add(Pelicula(
            id=5,
            titulo="El Señor de los Anillos: La Comunidad del Anillo",
            sinopsis="Un hobbit emprende un viaje épico para destruir un anillo mágico y salvar la Tierra Media.",
            director="Peter Jackson",
            genero="accion",
            clasificacion="PG-13",
            duracion_min=178,
            presupuesto_millones=93.0,
            disponible=True,
            fecha_estreno="2001-12-19",
            creado_en="2001-10-01T09:00:00",
            puntuacion=8.8
        ))
        
        # ========================================================================
        # Película 6: Inception
        # ========================================================================
        session.add(Pelicula(
            id=6,
            titulo="Inception",
            sinopsis="Un ladrón especializado en extraer secretos de los sueños de las personas es contratado para una misión imposible.",
            director="Christopher Nolan",
            genero="ciencia_ficcion",
            clasificacion="PG-13",
            duracion_min=148,
            presupuesto_millones=160.0,
            disponible=True,
            fecha_estreno="2010-07-16",
            creado_en="2010-05-15T11:00:00",
            puntuacion=8.8
        ))
        
        # ========================================================================
        # Película 7: Forrest Gump
        # ========================================================================
        session.add(Pelicula(
            id=7,
            titulo="Forrest Gump",
            sinopsis="La vida de un hombre con discapacidad intelectual que vive eventos históricos importantes de Estados Unidos.",
            director="Robert Zemeckis",
            genero="drama",
            clasificacion="PG-13",
            duracion_min=142,
            presupuesto_millones=55.0,
            disponible=True,
            fecha_estreno="1994-07-06",
            creado_en="1994-05-10T13:00:00",
            puntuacion=8.8
        ))
        
        # Confirma todas las inserciones en la base de datos
        # Sin commit(), los cambios no se guardarían permanentemente
        session.commit()