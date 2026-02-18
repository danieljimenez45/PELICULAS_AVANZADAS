"""
Módulo que define el modelo de datos Pelicula y sus DTOs (Data Transfer Objects).
Utiliza SQLModel para combinar la definición de modelo de Pydantic con SQLAlchemy.
"""

from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date, datetime
from .enums import GeneroEnum, ClasificacionEnum


class Pelicula(SQLModel, table=True):
    """
    Modelo principal que representa una película en la base de datos.
    
    Hereda de SQLModel con table=True, lo que significa que se creará una tabla
    en la base de datos con estos campos.
    
    Este modelo se usa tanto para la base de datos como para validación de datos.
    """
    
    # Campo ID: Clave primaria autoincremental
    id: Optional[int] = Field(default=None, primary_key=True)
    # primary_key=True indica que es la clave primaria de la tabla
    # default=None permite que la BD asigne automáticamente el ID

    # Campos de texto (Strings)
    titulo: str = Field(index=True, max_length=100)
    # index=True crea un índice en la BD para búsquedas más rápidas
    # max_length limita la longitud del texto
    
    sinopsis: str = Field(max_length=500)
    # Descripción breve de la película
    
    director: str = Field(index=True, max_length=80)
    # index=True permite búsquedas rápidas por director

    # Campos Enum: Valores restringidos a opciones predefinidas
    genero: GeneroEnum = Field(index=True)
    # index=True permite filtrar/buscar por género eficientemente
    
    clasificacion: ClasificacionEnum
    # Clasificación por edades (G, PG, PG-13, R, NC-17)

    # Campos numéricos con validaciones
    duracion_min: int = Field(gt=0, lt=600, description="Duración en minutos")
    # gt=0: debe ser mayor que 0 (no puede ser negativa)
    # lt=600: debe ser menor que 600 minutos (10 horas máximo)
    
    presupuesto_millones: float = Field(gt=0, description="Presupuesto en millones")
    # gt=0: debe ser mayor que 0 (presupuesto positivo)
    # Almacenado en millones de dólares/euros

    # Campo booleano
    disponible: bool = Field(default=True)
    # Indica si la película está disponible para visualización
    # Por defecto todas las películas están disponibles

    # Campos de fecha
    fecha_estreno: date
    # Fecha de estreno de la película en cines
    
    creado_en: datetime = Field(default_factory=datetime.utcnow)
    # Timestamp de cuándo se creó el registro en la base de datos
    # default_factory=datetime.utcnow asigna automáticamente la fecha/hora actual
    # cuando se crea una nueva película

    # Campo de puntuación (opcional)
    puntuacion: Optional[float] = Field(default=None, ge=0, le=10)
    # ge=0: debe ser mayor o igual que 0
    # le=10: debe ser menor o igual que 10
    # Optional permite que sea None si no hay puntuación aún

# ============================================================================
# DTOs (Data Transfer Objects)
# ============================================================================
# Los DTOs son modelos que se usan para transferir datos entre capas de la aplicación.
# Separar los DTOs del modelo de BD permite mayor flexibilidad y seguridad.

class PeliculaCreate(SQLModel):
    """
    DTO para crear una nueva película.
    
    Se usa cuando el cliente envía datos para crear una película.
    No incluye campos que se generan automáticamente (como id, creado_en).
    Todos los campos son requeridos excepto disponible y puntuacion.
    """
    titulo: str
    sinopsis: str
    director: str
    genero: GeneroEnum
    clasificacion: ClasificacionEnum
    duracion_min: int
    presupuesto_millones: float
    disponible: bool = True  # Por defecto está disponible
    fecha_estreno: date
    puntuacion: Optional[float] = None  # Opcional, puede no tener puntuación inicial

class PeliculaUpdate(SQLModel):
    """
    DTO para actualizar una película existente.
    
    Se usa en operaciones PATCH (actualización parcial).
    Todos los campos son opcionales porque solo se actualizan los campos enviados.
    Si un campo no se envía, no se modifica en la base de datos.
    """
    titulo: Optional[str] = None
    sinopsis: Optional[str] = None
    director: Optional[str] = None
    genero: Optional[GeneroEnum] = None
    clasificacion: Optional[ClasificacionEnum] = None
    duracion_min: Optional[int] = None
    presupuesto_millones: Optional[float] = None
    disponible: Optional[bool] = None
    fecha_estreno: Optional[date] = None
    puntuacion: Optional[float] = None

class PeliculaResponse(Pelicula):
    """
    DTO para la respuesta al cliente.
    
    Hereda de Pelicula pero se usa específicamente para serializar
    los datos que se envían al cliente en las respuestas de la API.
    Incluye todos los campos incluyendo el ID y las fechas generadas automáticamente.
    """
    id: int  # ID es requerido en la respuesta (ya existe en la BD)
    titulo: str
    sinopsis: str       
    director: str
    genero: GeneroEnum
    clasificacion: ClasificacionEnum
    duracion_min: int
    presupuesto_millones: float
    disponible: bool
    fecha_estreno: date
    creado_en: datetime  # Incluye la fecha de creación
    puntuacion: Optional[float]

# ============================================================================
# Funciones Mapper (Convertidores entre DTOs y Modelos)
# ============================================================================
# Estas funciones convierten entre los diferentes tipos de objetos:
# - DTOs (Create, Update, Response) ↔ Modelo de BD (Pelicula)

def map_pelicula_to_response(pelicula: Pelicula) -> PeliculaResponse:
    """
    Convierte un objeto Pelicula (de la BD) a PeliculaResponse (para enviar al cliente).
    
    Args:
        pelicula: Objeto Pelicula obtenido de la base de datos.
    
    Returns:
        Objeto PeliculaResponse con todos los datos de la película.
    
    Esta función se usa cuando se devuelven películas en las respuestas de la API.
    """
    return PeliculaResponse(
        id=pelicula.id,
        titulo=pelicula.titulo,
        sinopsis=pelicula.sinopsis,
        director=pelicula.director,
        genero=pelicula.genero,
        clasificacion=pelicula.clasificacion,
        duracion_min=pelicula.duracion_min,
        presupuesto_millones=pelicula.presupuesto_millones,
        disponible=pelicula.disponible,
        fecha_estreno=pelicula.fecha_estreno,
        creado_en=pelicula.creado_en,
        puntuacion=pelicula.puntuacion
    )    

def map_create_to_pelicula(pelicula_create: PeliculaCreate) -> Pelicula:
    """
    Convierte un objeto PeliculaCreate (del cliente) a Pelicula (para guardar en BD).
    
    Args:
        pelicula_create: Objeto PeliculaCreate con los datos enviados por el cliente.
    
    Returns:
        Objeto Pelicula listo para ser insertado en la base de datos.
        El ID será None hasta que se guarde en la BD.
    
    Esta función se usa cuando se reciben datos para crear una nueva película.
    """
    return Pelicula(
        titulo=pelicula_create.titulo,
        sinopsis=pelicula_create.sinopsis,
        director=pelicula_create.director,
        genero=pelicula_create.genero,
        clasificacion=pelicula_create.clasificacion,
        duracion_min=pelicula_create.duracion_min,
        presupuesto_millones=pelicula_create.presupuesto_millones,
        disponible=pelicula_create.disponible,
        fecha_estreno=pelicula_create.fecha_estreno,
        puntuacion=pelicula_create.puntuacion
    )

def map_update_to_pelicula(pelicula: Pelicula, pelicula_update: PeliculaUpdate) -> Pelicula:
    """
    Actualiza un objeto Pelicula con los datos de PeliculaUpdate.
    
    Solo actualiza los campos que no son None en pelicula_update.
    Esto permite actualizaciones parciales (PATCH).
    
    Args:
        pelicula: Objeto Pelicula existente que se va a actualizar.
        pelicula_update: Objeto PeliculaUpdate con los nuevos valores.
    
    Returns:
        El mismo objeto Pelicula modificado con los nuevos valores.
    
    Esta función se usa cuando se actualizan películas existentes.
    """
    # Actualiza cada campo solo si tiene un valor (no es None)
    if pelicula_update.titulo is not None:
        pelicula.titulo = pelicula_update.titulo
    if pelicula_update.sinopsis is not None:
        pelicula.sinopsis = pelicula_update.sinopsis
    if pelicula_update.director is not None:
        pelicula.director = pelicula_update.director
    if pelicula_update.genero is not None:
        pelicula.genero = pelicula_update.genero
    if pelicula_update.clasificacion is not None:
        pelicula.clasificacion = pelicula_update.clasificacion
    if pelicula_update.duracion_min is not None:
        pelicula.duracion_min = pelicula_update.duracion_min
    if pelicula_update.presupuesto_millones is not None:
        pelicula.presupuesto_millones = pelicula_update.presupuesto_millones
    if pelicula_update.disponible is not None:
        pelicula.disponible = pelicula_update.disponible
    if pelicula_update.fecha_estreno is not None:
        pelicula.fecha_estreno = pelicula_update.fecha_estreno
    if pelicula_update.puntuacion is not None:
        pelicula.puntuacion = pelicula_update.puntuacion
    return pelicula