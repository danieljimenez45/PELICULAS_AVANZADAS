from fastapi import APIRouter, HTTPException , Depends
from sqlmodel import Session
from src.data.db import get_session
from typing import Annotated
from src.data.PeliculasAvanzadasRepository import PeliculasAvanzadasRepository
from src.models.Pelicula import (
    PeliculaCreate,
    PeliculaUpdate,
    PeliculaResponse,
    map_create_to_pelicula,
    map_pelicula_to_response,
)

router = APIRouter(prefix="/api/peliculas", tags= ["peliculas"])

SessionDep = Annotated[Session, Depends(get_session)]
#Rutas de la API para gestionar peliculas avanzadas

@router.get("/", response_model=list[PeliculaResponse])
def lista_peliculas_avanzadas(session: SessionDep):
    repo = PeliculasAvanzadasRepository(session)
    peliculas = repo.get_all_peliculas_avanzadas()
    return [map_pelicula_to_response(p) for p in peliculas]

@router.post("/", response_model=PeliculaResponse, status_code=201)
def nueva_pelicula_avanzada(pelicula_create: PeliculaCreate, session: SessionDep):
    repo = PeliculasAvanzadasRepository(session)
    pelicula = map_create_to_pelicula(pelicula_create)
    pelicula_creada = repo.create_pelicula_avanzada(pelicula)
    return map_pelicula_to_response(pelicula_creada)

@router.get("/{pelicula_id}", response_model=PeliculaResponse)
def pelicula_avanzada_por_id(pelicula_id: int, session: SessionDep):
    repo = PeliculasAvanzadasRepository(session)
    pelicula = repo.get_pelicula_avanzada(pelicula_id)
    if not pelicula:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    return map_pelicula_to_response(pelicula)

@router.delete("/{pelicula_id}", status_code=204)
def borrar_pelicula_avanzada(pelicula_id: int, session: SessionDep):
    repo = PeliculasAvanzadasRepository(session)
    pelicula = repo.get_pelicula_avanzada(pelicula_id)
    if not pelicula:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    repo.delete_pelicula_avanzada(pelicula_id)

@router.patch("/{pelicula_id}", response_model=PeliculaResponse)
def actualizar_parcial_pelicula_avanzada(
    pelicula_id: int,
    pelicula_update: PeliculaUpdate,
    session: SessionDep,
):
    repo = PeliculasAvanzadasRepository(session)
    pelicula_encontrada = repo.get_pelicula_avanzada(pelicula_id)
    if not pelicula_encontrada:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    pelicula_actualizada = repo.update_pelicula_avanzada(pelicula_id, pelicula_update.dict(exclude_unset=True))
    return map_pelicula_to_response(pelicula_actualizada)

@router.put("/{pelicula_id}", response_model=PeliculaResponse)
def actualizar_completo_pelicula_avanzada(  
    pelicula_id: int,
    pelicula_update: PeliculaUpdate,
    session: SessionDep,
):
    repo = PeliculasAvanzadasRepository(session)
    pelicula_encontrada = repo.get_pelicula_avanzada(pelicula_id)
    if not pelicula_encontrada:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    pelicula_actualizada = repo.update_pelicula_avanzada(pelicula_id, pelicula_update.dict())
    return map_pelicula_to_response(pelicula_actualizada)       