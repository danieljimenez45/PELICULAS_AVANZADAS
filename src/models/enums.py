"""
Módulo que define los enumerados (enums) utilizados en el modelo de Película.
Los enums restringen los valores posibles que pueden tomar ciertos campos.
"""

from enum import Enum

class GeneroEnum(str, Enum):
    """
    Enum que define los géneros cinematográficos disponibles para las películas.
    Hereda de str y Enum para poder usarse como string en la base de datos.
    """
    accion = "accion"
    drama = "drama"
    comedia = "comedia"
    terror = "terror"
    ciencia_ficcion = "ciencia_ficcion"
    romance = "romance"

class ClasificacionEnum(str, Enum):
    """
    Enum que define las clasificaciones por edades según el sistema de rating MPAA.
    Hereda de str y Enum para poder usarse como string en la base de datos.
    
    Valores:
    - G: Todos los públicos
    - PG: Se recomienda la guía de los padres
    - PG-13: Se recomienda la guía de los padres para menores de 13 años
    - R: Restringido, menores de 17 años requieren acompañante adulto
    - NC-17: Solo mayores de 17 años
    """
    g = "G"
    pg = "PG"
    pg13 = "PG-13"
    r = "R"
    nc17 = "NC-17"
