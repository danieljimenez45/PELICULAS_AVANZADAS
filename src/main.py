"""
Archivo principal de la aplicación FastAPI.
Define la aplicación web, configura rutas HTML y API, y gestiona el ciclo de vida de la app.
"""

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

# ============================================================================
# Gestión del ciclo de vida de la aplicación
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager que gestiona el ciclo de vida de la aplicación FastAPI.
    
    Se ejecuta al iniciar la aplicación (antes de yield) y al cerrarla (después de yield).
    Aquí se inicializa la base de datos con tablas y datos de ejemplo.
    
    Args:
        app: Instancia de la aplicación FastAPI.
    
    Yields:
        None: Controla el tiempo de vida de la aplicación.
    """
    # Código que se ejecuta AL INICIAR la aplicación
    # Inicializa la BD: elimina tablas viejas, crea nuevas y añade datos de ejemplo
    init_db()
    yield  # La aplicación está corriendo aquí
    # Código que se ejecuta AL CERRAR la aplicación (opcional)
    # Por ejemplo: cerrar conexiones, guardar logs, etc.

# ============================================================================
# Configuración de la aplicación FastAPI
# ============================================================================

# Define un tipo anotado para la dependencia de sesión de base de datos
# Permite inyectar automáticamente una sesión de BD en las rutas que lo necesiten
SessionDep = Annotated[Session, Depends(get_session)]

# Crea la instancia principal de la aplicación FastAPI
# lifespan=lifespan: usa el context manager definido arriba para gestionar el ciclo de vida
app = FastAPI(lifespan=lifespan)

# Monta el directorio de archivos estáticos (CSS, JS, imágenes, etc.)
# Los archivos en /static serán accesibles desde la URL /static
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configura Jinja2 para renderizar plantillas HTML
# Las plantillas están en el directorio "templates"
templates = Jinja2Templates(directory="templates")

# Incluye el router de la API REST
# Todas las rutas del router tendrán el prefijo /api/peliculas
app.include_router(api_peliculas_avanzadas_router)

# ============================================================================
# Rutas HTML (Interfaz Web)
# ============================================================================

@app.get("/", response_class = HTMLResponse)
async def root(request: Request):
    """
    Ruta raíz de la aplicación que muestra la página de inicio.
    
    Ruta: GET /
    
    Args:
        request: Objeto Request de FastAPI con información de la petición HTTP.
                Necesario para renderizar plantillas Jinja2.
    
    Returns:
        HTMLResponse: Página HTML renderizada desde la plantilla index.html.
    
    Esta ruta muestra la página principal con enlaces a otras secciones.
    """
    # Renderiza la plantilla index.html pasando el request como contexto
    # Jinja2 necesita el request para funciones como url_for()
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/peliculas", response_class = HTMLResponse)
async def ver_peliculas(request: Request, session: SessionDep):
    """
    Ruta GET que muestra el listado de todas las películas en formato HTML.
    
    Ruta: GET /peliculas
    
    Args:
        request: Objeto Request de FastAPI necesario para renderizar plantillas.
        session: Sesión de base de datos inyectada automáticamente.
    
    Returns:
        HTMLResponse: Página HTML con la lista de todas las películas.
    
    Esta ruta obtiene todas las películas de la BD y las muestra en una tabla HTML.
    """
    # Crea el repositorio para acceder a los datos
    repo = PeliculasAvanzadasRepository(session)
    # Obtiene todas las películas de la base de datos
    peliculas = repo.get_all_peliculas_avanzadas()
    # Renderiza la plantilla HTML pasando las películas como contexto
    return templates.TemplateResponse("peliculas/peliculas.html", {"request": request, "peliculas": peliculas})

@app.get("/peliculas/new" , response_class= HTMLResponse)
async def nueva_pelicula_form(request: Request):
    """
    Ruta GET que muestra el formulario HTML para crear una nueva película.
    
    Ruta: GET /peliculas/new
    
    Args:
        request: Objeto Request de FastAPI necesario para renderizar plantillas.
    
    Returns:
        HTMLResponse: Página HTML con el formulario de creación de película.
    
    Esta ruta muestra un formulario vacío para que el usuario introduzca los datos
    de una nueva película. Al enviar el formulario, se hace POST a la misma URL.
    """
    # Renderiza el formulario pasando una película vacía como contexto
    # La plantilla usa este objeto para inicializar los campos del formulario
    return templates.TemplateResponse("peliculas/pelicula_form.html",{
        "request": request,
        "pelicula": Pelicula()  # Película vacía para inicializar el formulario
    })

@app.post("/peliculas/new")
async def crear_pelicula(request: Request, session: SessionDep):
    """
    Ruta POST que procesa el formulario y crea una nueva película en la BD.
    
    Ruta: POST /peliculas/new
    
    Args:
        request: Objeto Request de FastAPI que contiene los datos del formulario.
        session: Sesión de base de datos inyectada automáticamente.
    
    Returns:
        RedirectResponse: Redirige a /peliculas después de crear la película.
        Status code: 303 See Other (redirección después de POST).
    
    Esta ruta recibe los datos del formulario HTML, los valida, crea la película
    en la BD y redirige al listado de películas.
    """
    # Obtiene los datos del formulario HTML (form-data)
    # await es necesario porque request.form() es una operación asíncrona
    form_data = await request.form()
    
    # Crea un objeto PeliculaCreate a partir de los datos del formulario
    # form_data.get() obtiene el valor de cada campo del formulario
    pelicula_create = PeliculaCreate(
        titulo=form_data.get("titulo"),
        sinopsis=form_data.get("sinopsis"),
        director=form_data.get("director"),
        genero=form_data.get("genero"),
        clasificacion=form_data.get("clasificacion"),
        # Convierte a int porque los formularios HTML envían strings
        duracion_min=int(form_data.get("duracion_min", 0)),
        # Convierte a float porque los formularios HTML envían strings
        presupuesto_millones=float(form_data.get("presupuesto_millones", 0)),
        # Los checkboxes envían "on" si están marcados, None si no
        disponible=form_data.get("disponible") == "on",
        fecha_estreno=form_data.get("fecha_estreno"),
    )
    
    # Crea el repositorio y guarda la película
    repo = PeliculasAvanzadasRepository(session)
    # Convierte el DTO a modelo de BD
    pelicula = map_create_to_pelicula(pelicula_create)
    # Guarda en la base de datos
    repo.create_pelicula_avanzada(pelicula)
    
    # Redirige al listado de películas después de crear
    # Status 303 es el estándar para redirección después de POST
    return RedirectResponse(url="/peliculas", status_code=303)

@app.get("/peliculas/{pelicula_id}", response_class = HTMLResponse)
async def pelicula_por_id_html(pelicula_id: int ,request: Request, session: SessionDep):
    """
    Ruta GET que muestra los detalles de una película específica en formato HTML.
    
    Ruta: GET /peliculas/{pelicula_id}
    
    Args:
        pelicula_id: ID de la película a mostrar (extraído de la URL).
        request: Objeto Request de FastAPI necesario para renderizar plantillas.
        session: Sesión de base de datos inyectada automáticamente.
    
    Returns:
        HTMLResponse: Página HTML con los detalles completos de la película.
    
    Raises:
        HTTPException: Si la película no existe (404 Not Found).
    
    Esta ruta muestra una página con toda la información de una película específica.
    """
    repo = PeliculasAvanzadasRepository(session)
    # Busca la película por ID
    pelicula_encontrada = repo.get_pelicula_avanzada(pelicula_id)
    # Si no existe, lanza error 404
    if not pelicula_encontrada:
        raise HTTPException(status_code=404, detail= "Pelicula no encontrada")
    # Convierte a DTO de respuesta
    pelicula_response = map_pelicula_to_response(pelicula_encontrada)
    # Renderiza la plantilla con los datos de la película
    return templates.TemplateResponse("peliculas/pelicula_detalle.html", {"request": request, "pelicula": pelicula_response })

# ============================================================================
# Punto de entrada de la aplicación
# ============================================================================

if __name__ == "__main__":
    """
    Bloque que se ejecuta solo cuando se ejecuta este archivo directamente
    (no cuando se importa como módulo).
    
    Inicia el servidor uvicorn para ejecutar la aplicación FastAPI.
    """
    # Ejecuta el servidor uvicorn con la aplicación FastAPI
    # "main:app": busca el objeto 'app' en el módulo 'main'
    # host="127.0.0.1": solo acepta conexiones locales (localhost)
    # port=8000: puerto donde escucha el servidor
    # reload=True: recarga automáticamente cuando cambias el código (solo desarrollo)
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)