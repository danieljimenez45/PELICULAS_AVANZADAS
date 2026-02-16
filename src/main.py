from typing import Annotated
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from sqlmodel import Session, select

from models.Pelicula import (
    Pelicula,
    PeliculaCreate,
    PeliculaUpdate,
    PeliculaResponse,
    map_create_to_pelicula,
    map_pelicula_to_response,
)
from data.db import init_db, get_session
from data.PeliculasAvanzadasRepository  import PeliculasAvanzadasRepository
from routers.api_peliculas_avanzadas_router import router as api_peliculas_avanzadas_router

import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

SessionDep = Annotated[Session, Depends(get_session)]
app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(api_peliculas_avanzadas_router)
#Ruta para la página prncipal
@app.get("/", response_class = HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/peliculas", response_class = HTMLResponse)
async def ver_peliculas(request: Request, session: SessionDep):
    repo = PeliculasAvanzadasRepository(session)
    peliculas = repo.get_all_peliculas_avanzadas()
    return templates.TemplateResponse("peliculas/peliculas.html", {"request": request, "peliculas": peliculas})

@app.get("/peliculas/new" , response_class= HTMLResponse)
async def nueva_pelicula_form(request: Request):
    """Formulario para añadir una pelicula nueva"""
    return templates.TemplateResponse("peliculas/pelicula_form.html",{
        "request": request,
        "pelicula": Pelicula()
    })

@app.post("/peliculas/new")
async def crear_pelicula(request: Request, session: SessionDep):
    form_data = await request.form()
    pelicula_create = PeliculaCreate(
        titulo=form_data.get("titulo"),
        sinopsis=form_data.get("sinopsis"),
        director=form_data.get("director"),
        genero=form_data.get("genero"),
        clasificacion=form_data.get("clasificacion"),
        duracion_min=int(form_data.get("duracion_min", 0)),
        presupuesto_millones=float(form_data.get("presupuesto_millones", 0)),
        disponible=form_data.get("disponible") == "on",
        fecha_estreno=form_data.get("fecha_estreno"),
    )
    repo = PeliculasAvanzadasRepository(session)
    pelicula = map_create_to_pelicula(pelicula_create)
    repo.create_pelicula_avanzada(pelicula)
    return RedirectResponse(url="/peliculas", status_code=303)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)