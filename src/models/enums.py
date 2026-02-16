from enum import Enum

class GeneroEnum(str, Enum):
    accion = "accion"
    drama = "drama"
    comedia = "comedia"
    terror = "terror"
    ciencia_ficcion = "ciencia_ficcion"
    romance = "romance"

class ClasificacionEnum(str, Enum):
    g = "G"
    pg = "PG"
    pg13 = "PG-13"
    r = "R"
    nc17 = "NC-17"
