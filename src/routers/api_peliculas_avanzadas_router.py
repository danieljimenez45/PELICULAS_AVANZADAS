"""
Router que define los endpoints de la API REST para gestionar películas.
Todas las rutas tienen el prefijo /api/peliculas y devuelven respuestas JSON.
"""

from fastapi import APIRouter, HTTPException , Depends
from sqlmodel import Session
from data.db import get_session
from typing import Annotated
from data.PeliculasAvanzadasRepository import PeliculasAvanzadasRepository
from models.Pelicula import (
    PeliculaCreate,
    PeliculaUpdate,
    PeliculaResponse,
    map_create_to_pelicula,
    map_pelicula_to_response,
)

# Crea un router de FastAPI con prefijo y tags para organización
# prefix="/api/peliculas": todas las rutas empezarán con /api/peliculas
# tags=["peliculas"]: agrupa estas rutas en la documentación Swagger/OpenAPI
router = APIRouter(prefix="/api/peliculas", tags= ["peliculas"])

# Define un tipo anotado para la dependencia de sesión de base de datos
# SessionDep es un alias que indica que FastAPI debe inyectar una Session usando get_session
# Esto permite que cada request tenga su propia sesión de BD
SessionDep = Annotated[Session, Depends(get_session)]

# ============================================================================
# Endpoints de la API REST
# ============================================================================

@router.get("/", response_model=list[PeliculaResponse])
def lista_peliculas_avanzadas(session: SessionDep):
    """
    Endpoint GET que devuelve todas las películas disponibles.
    
    Ruta completa: GET /api/peliculas/
    
    Args:
        session: Sesión de base de datos inyectada automáticamente por FastAPI.
    
    Returns:
        Lista de objetos PeliculaResponse con todas las películas en formato JSON.
    
    Ejemplo de respuesta:
        [
            {
                "id": 1,
                "titulo": "Interestellar",
                "director": "Christopher Nolan",
                ...
            },
            ...
        ]
    """
    # Crea una instancia del repositorio con la sesión de BD
    repo = PeliculasAvanzadasRepository(session)
    # Obtiene todas las películas de la base de datos
    peliculas = repo.get_all_peliculas_avanzadas()
    # Convierte cada objeto Pelicula a PeliculaResponse usando list comprehension
    # Esto asegura que la respuesta tenga el formato correcto para la API
    return [map_pelicula_to_response(p) for p in peliculas]

@router.post("/", response_model=PeliculaResponse, status_code=201)
def nueva_pelicula_avanzada(pelicula_create: PeliculaCreate, session: SessionDep):
    """
    Endpoint POST que crea una nueva película.
    
    Ruta completa: POST /api/peliculas/
    
    Args:
        pelicula_create: Objeto PeliculaCreate con los datos de la nueva película.
                        FastAPI valida automáticamente el JSON del body del request.
        session: Sesión de base de datos inyectada automáticamente.
    
    Returns:
        Objeto PeliculaResponse con la película creada (incluyendo el ID asignado).
        Status code: 201 Created
    
    Ejemplo de request body:
        {
            "titulo": "Nueva Película",
            "sinopsis": "Descripción...",
            "director": "Director",
            "genero": "accion",
            "clasificacion": "PG-13",
            "duracion_min": 120,
            "presupuesto_millones": 50.0,
            "disponible": true,
            "fecha_estreno": "2024-01-01"
        }
    """
    # Crea el repositorio con la sesión
    repo = PeliculasAvanzadasRepository(session)
    # Convierte el DTO PeliculaCreate a modelo Pelicula
    pelicula = map_create_to_pelicula(pelicula_create)
    # Guarda la película en la base de datos
    pelicula_creada = repo.create_pelicula_avanzada(pelicula)
    # Convierte a PeliculaResponse para la respuesta JSON
    return map_pelicula_to_response(pelicula_creada)

@router.get("/{pelicula_id}", response_model=PeliculaResponse)
def pelicula_avanzada_por_id(pelicula_id: int, session: SessionDep):
    """
    Endpoint GET que obtiene una película específica por su ID.
    
    Ruta completa: GET /api/peliculas/{pelicula_id}
    
    Args:
        pelicula_id: ID de la película a buscar (extraído de la URL).
        session: Sesión de base de datos inyectada automáticamente.
    
    Returns:
        Objeto PeliculaResponse con los datos de la película encontrada.
    
    Raises:
        HTTPException: Si la película no existe (404 Not Found).
    
    Ejemplo de uso:
        GET /api/peliculas/1
    """
    repo = PeliculasAvanzadasRepository(session)
    # Busca la película por ID
    pelicula = repo.get_pelicula_avanzada(pelicula_id)
    # Si no existe, lanza una excepción HTTP 404
    if not pelicula:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    # Convierte y devuelve la película encontrada
    return map_pelicula_to_response(pelicula)

@router.delete("/{pelicula_id}", status_code=204)
def borrar_pelicula_avanzada(pelicula_id: int, session: SessionDep):
    """
    Endpoint DELETE que elimina una película por su ID.
    
    Ruta completa: DELETE /api/peliculas/{pelicula_id}
    
    Args:
        pelicula_id: ID de la película a eliminar (extraído de la URL).
        session: Sesión de base de datos inyectada automáticamente.
    
    Returns:
        Ninguno (status code 204 No Content).
    
    Raises:
        HTTPException: Si la película no existe (404 Not Found).
    
    Ejemplo de uso:
        DELETE /api/peliculas/1
    """
    repo = PeliculasAvanzadasRepository(session)
    # Verifica que la película existe antes de intentar eliminarla
    pelicula = repo.get_pelicula_avanzada(pelicula_id)
    if not pelicula:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    # Elimina la película de la base de datos
    repo.delete_pelicula_avanzada(pelicula_id)
    # No devuelve contenido (204 No Content)

@router.patch("/{pelicula_id}", response_model=PeliculaResponse)
def actualizar_parcial_pelicula_avanzada(
    pelicula_id: int,
    pelicula_update: PeliculaUpdate,
    session: SessionDep,
):
    """
    Endpoint PATCH que actualiza parcialmente una película.
    
    Ruta completa: PATCH /api/peliculas/{pelicula_id}
    
    Solo actualiza los campos que se envían en el request body.
    Los campos que no se envían permanecen sin cambios.
    
    Args:
        pelicula_id: ID de la película a actualizar (extraído de la URL).
        pelicula_update: Objeto PeliculaUpdate con los campos a actualizar.
                        Todos los campos son opcionales.
        session: Sesión de base de datos inyectada automáticamente.
    
    Returns:
        Objeto PeliculaResponse con la película actualizada.
    
    Raises:
        HTTPException: Si la película no existe (404 Not Found).
    
    Ejemplo de request body (solo actualiza título y director):
        {
            "titulo": "Nuevo Título",
            "director": "Nuevo Director"
        }
    """
    repo = PeliculasAvanzadasRepository(session)
    # Verifica que la película existe
    pelicula_encontrada = repo.get_pelicula_avanzada(pelicula_id)
    if not pelicula_encontrada:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    
    # Convierte el DTO a diccionario, excluyendo campos no establecidos (None)
    # exclude_unset=True solo incluye los campos que realmente se enviaron
    pelicula_data = pelicula_update.model_dump(exclude_unset=True)
    # Actualiza solo los campos enviados
    pelicula_actualizada = repo.update_pelicula_avanzada(pelicula_id, pelicula_data)
    return map_pelicula_to_response(pelicula_actualizada)

@router.put("/{pelicula_id}", response_model=PeliculaResponse)
def actualizar_completo_pelicula_avanzada(  
    pelicula_id: int,
    pelicula_update: PeliculaUpdate,
    session: SessionDep,
):
    """
    Endpoint PUT que actualiza completamente una película.
    
    Ruta completa: PUT /api/peliculas/{pelicula_id}
    
    A diferencia de PATCH, PUT reemplaza todos los campos.
    Los campos que no se envían se establecen como None (si son opcionales).
    
    Args:
        pelicula_id: ID de la película a actualizar (extraído de la URL).
        pelicula_update: Objeto PeliculaUpdate con todos los campos a actualizar.
        session: Sesión de base de datos inyectada automáticamente.
    
    Returns:
        Objeto PeliculaResponse con la película actualizada.
    
    Raises:
        HTTPException: Si la película no existe (404 Not Found).
    
    Nota: Aunque PeliculaUpdate tiene campos opcionales, en PUT se espera
          enviar todos los campos para una actualización completa.
    """
    repo = PeliculasAvanzadasRepository(session)
    # Verifica que la película existe
    pelicula_encontrada = repo.get_pelicula_avanzada(pelicula_id)
    if not pelicula_encontrada:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    
    # Convierte el DTO a diccionario incluyendo todos los campos
    # model_dump() sin exclude_unset incluye todos los campos (incluso None)
    pelicula_data = pelicula_update.model_dump()
    # Actualiza la película con todos los datos
    pelicula_actualizada = repo.update_pelicula_avanzada(pelicula_id, pelicula_data)
    return map_pelicula_to_response(pelicula_actualizada)