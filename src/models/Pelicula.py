from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date, datetime
from .enums import GeneroEnum, ClasificacionEnum


class Pelicula(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # Strings
    titulo: str = Field(index=True, max_length=100)
    sinopsis: str = Field(max_length=500)
    director: str = Field(index=True, max_length=80)

    # Enum
    genero: GeneroEnum = Field(index=True)
    clasificacion: ClasificacionEnum

    # Numéricos
    duracion_min: int = Field(gt=0, lt=600, description="Duración en minutos")
    presupuesto_millones: float = Field(gt=0, description="Presupuesto en millones")

    # Boolean
    disponible: bool = Field(default=True)

    # Fechas
    fecha_estreno: date
    creado_en: datetime = Field(default_factory=datetime.utcnow)

    # Ratings
    puntuacion: Optional[float] = Field(default=None, ge=0, le=10)

# DTOs
# DTO para creación
class PeliculaCreate(SQLModel):
    titulo: str
    sinopsis: str
    director: str
    genero: GeneroEnum
    clasificacion: ClasificacionEnum
    duracion_min: int
    presupuesto_millones: float
    disponible: bool = True
    fecha_estreno: date
    puntuacion: Optional[float] = None

# DTO para actualización (todos los campos opcionales)
class PeliculaUpdate(SQLModel):
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
# DTO para respuesta (todos los campos, incluyendo ID)    
class PeliculaResponse(Pelicula):
    id: int
    titulo: str
    sinopsis: str       
    director: str
    genero: GeneroEnum
    clasificacion: ClasificacionEnum
    duracion_min: int
    presupuesto_millones: float
    disponible: bool
    fecha_estreno: date
    creado_en: datetime
    puntuacion: Optional[float]

# Mappers
def map_pelicula_to_response(pelicula: Pelicula) -> PeliculaResponse:
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