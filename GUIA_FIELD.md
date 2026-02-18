# 📚 Guía Completa de Field() en SQLModel/Pydantic

Este documento explica todas las opciones disponibles para usar en `Field()` cuando defines campos en modelos SQLModel/Pydantic.

---

## 📋 Índice

1. [Parámetros Básicos](#parámetros-básicos)
2. [Validación de Tipos](#validación-de-tipos)
3. [Validación Numérica](#validación-numérica)
4. [Validación de Strings](#validación-de-strings)
5. [Validación de Fechas](#validación-de-fechas)
6. [Configuración de Base de Datos](#configuración-de-base-de-datos)
6. [Valores por Defecto](#valores-por-defecto)
7. [Documentación y Metadata](#documentación-y-metadata)
8. [Ejemplos Prácticos](#ejemplos-prácticos)

---

## Parámetros Básicos

### `default`
Valor por defecto del campo si no se proporciona.

```python
from sqlmodel import Field

# Campo con valor por defecto
disponible: bool = Field(default=True)

# Campo opcional con None por defecto
puntuacion: Optional[float] = Field(default=None)
```

### `default_factory`
Función que genera el valor por defecto (se ejecuta cada vez que se crea una instancia).

```python
from datetime import datetime

# Fecha/hora actual al crear el registro
creado_en: datetime = Field(default_factory=datetime.utcnow)

# ID único generado automáticamente
import uuid
id_unico: str = Field(default_factory=lambda: str(uuid.uuid4()))
```

### `alias`
Nombre alternativo para el campo en la serialización/deserialización.

```python
# En el código Python se usa "fecha_estreno"
# En JSON se serializa como "release_date"
fecha_estreno: date = Field(alias="release_date")
```

### `title`
Título descriptivo del campo (útil para documentación).

```python
titulo: str = Field(title="Título de la Película")
```

### `description`
Descripción del campo (aparece en la documentación OpenAPI/Swagger).

```python
duracion_min: int = Field(
    description="Duración de la película en minutos",
    gt=0,
    lt=600
)
```

---

## Validación de Tipos

### `ge` (Greater or Equal)
Valor debe ser mayor o igual que el especificado.

```python
# Número positivo o cero
edad: int = Field(ge=0)

# Duración mínima de 1 minuto
duracion_min: int = Field(ge=1)
```

### `gt` (Greater Than)
Valor debe ser mayor que el especificado.

```python
# Número estrictamente positivo
presupuesto: float = Field(gt=0)

# ID debe ser mayor que 0
id: int = Field(gt=0)
```

### `le` (Less or Equal)
Valor debe ser menor o igual que el especificado.

```python
# Puntuación máxima de 10
puntuacion: float = Field(le=10)

# Porcentaje máximo de 100
porcentaje: int = Field(le=100)
```

### `lt` (Less Than)
Valor debe ser menor que el especificado.

```python
# Duración máxima de 600 minutos (10 horas)
duracion_min: int = Field(lt=600)

# Edad máxima de 120 años
edad: int = Field(lt=120)
```

### `multiple_of`
Valor debe ser múltiplo del número especificado.

```python
# Solo números pares
numero_par: int = Field(multiple_of=2)

# Solo múltiplos de 5
precio: float = Field(multiple_of=5.0)
```

---

## Validación Numérica

### Combinación de validaciones numéricas

```python
# Puntuación entre 0 y 10
puntuacion: float = Field(ge=0, le=10)

# Duración entre 1 y 600 minutos
duracion_min: int = Field(gt=0, lt=600)

# Presupuesto positivo
presupuesto_millones: float = Field(gt=0, description="Presupuesto en millones")
```

---

## Validación de Strings

### `min_length`
Longitud mínima del string.

```python
# Título debe tener al menos 3 caracteres
titulo: str = Field(min_length=3)

# Código debe tener al menos 5 caracteres
codigo: str = Field(min_length=5)
```

### `max_length`
Longitud máxima del string.

```python
# Título máximo de 100 caracteres
titulo: str = Field(max_length=100)

# Email máximo de 255 caracteres
email: str = Field(max_length=255)
```

### `pattern` (Regex)
El string debe coincidir con el patrón regex especificado.

```python
import re

# Email válido
email: str = Field(pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

# Código postal español (5 dígitos)
codigo_postal: str = Field(pattern=r'^\d{5}$')

# Teléfono español (9 dígitos)
telefono: str = Field(pattern=r'^\d{9}$')
```

### Combinación de validaciones de strings

```python
# Título entre 3 y 100 caracteres
titulo: str = Field(
    min_length=3,
    max_length=100,
    description="Título de la película"
)

# Sinopsis entre 10 y 500 caracteres
sinopsis: str = Field(
    min_length=10,
    max_length=500,
    description="Descripción breve de la película"
)
```

---

## Validación de Fechas

### `ge`, `gt`, `le`, `lt` con fechas

```python
from datetime import date, datetime

# Fecha de estreno no puede ser anterior a 1900
fecha_estreno: date = Field(ge=date(1900, 1, 1))

# Fecha de nacimiento no puede ser futura
fecha_nacimiento: date = Field(le=date.today())

# Fecha de creación debe ser actual o pasada
creado_en: datetime = Field(default_factory=datetime.utcnow, le=datetime.utcnow())
```

---

## Configuración de Base de Datos

### `primary_key`
Indica que el campo es la clave primaria de la tabla.

```python
# ID como clave primaria
id: Optional[int] = Field(default=None, primary_key=True)
```

### `index`
Crea un índice en la base de datos para búsquedas más rápidas.

```python
# Índice simple
titulo: str = Field(index=True, max_length=100)

# Múltiples campos con índice
director: str = Field(index=True, max_length=80)
genero: str = Field(index=True)
```

### `unique`
El campo debe tener valores únicos en la tabla.

```python
# Email único
email: str = Field(unique=True, max_length=255)

# Código único
codigo: str = Field(unique=True, max_length=20)
```

### `nullable`
Indica si el campo puede ser NULL en la base de datos (por defecto es True si es Optional).

```python
# Campo que puede ser NULL
puntuacion: Optional[float] = Field(default=None, nullable=True)

# Campo que NO puede ser NULL
titulo: str = Field(nullable=False, max_length=100)
```

### `sa_column`
Permite especificar directamente una columna de SQLAlchemy con configuración avanzada.

```python
from sqlalchemy import Column, String, Text

# Columna personalizada con tipo TEXT en lugar de VARCHAR
sinopsis: str = Field(
    sa_column=Column(Text),
    max_length=500
)

# Columna con longitud específica
codigo: str = Field(
    sa_column=Column(String(20), unique=True),
    max_length=20
)
```

---

## Valores por Defecto

### Valores simples

```python
# Booleano por defecto
disponible: bool = Field(default=True)

# Entero por defecto
contador: int = Field(default=0)

# String por defecto
estado: str = Field(default="pendiente")
```

### Valores None (campos opcionales)

```python
from typing import Optional

# Campo opcional con None por defecto
puntuacion: Optional[float] = Field(default=None)

# Campo opcional con valor por defecto si no se proporciona
categoria: Optional[str] = Field(default="general")
```

### Funciones generadoras

```python
from datetime import datetime
import uuid

# Fecha/hora actual
creado_en: datetime = Field(default_factory=datetime.utcnow)

# ID único
id_unico: str = Field(default_factory=lambda: str(uuid.uuid4()))

# Contador incremental (requiere lógica adicional)
contador: int = Field(default_factory=lambda: get_next_counter())
```

---

## Documentación y Metadata

### `title`
Título del campo para documentación.

```python
titulo: str = Field(title="Título de la Película")
```

### `description`
Descripción detallada del campo.

```python
duracion_min: int = Field(
    description="Duración de la película en minutos. Debe estar entre 1 y 600 minutos.",
    gt=0,
    lt=600
)
```

### `example`
Ejemplo de valor para la documentación.

```python
email: str = Field(
    example="usuario@ejemplo.com",
    pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
)
```

### `deprecated`
Marca el campo como deprecado.

```python
# Campo antiguo que ya no se debe usar
campo_antiguo: str = Field(deprecated=True, description="Usar campo_nuevo en su lugar")
```

---

## Validaciones Avanzadas

### `const`
El campo debe tener exactamente este valor (constante).

```python
# Campo que siempre debe ser "activo"
estado: str = Field(const="activo")

# Versión fija
version: str = Field(const="1.0.0")
```

### `regex` (alias de `pattern`)
Validación mediante expresión regular.

```python
# Código alfanumérico de 6 caracteres
codigo: str = Field(regex=r'^[A-Z0-9]{6}$', max_length=6)
```

---

## Ejemplos Prácticos

### Ejemplo 1: Modelo de Película Completo

```python
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date, datetime

class Pelicula(SQLModel, table=True):
    # Clave primaria
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Strings con validación de longitud
    titulo: str = Field(
        index=True,
        max_length=100,
        min_length=1,
        description="Título de la película"
    )
    
    sinopsis: str = Field(
        max_length=500,
        min_length=10,
        description="Descripción breve de la película"
    )
    
    director: str = Field(
        index=True,
        max_length=80,
        description="Nombre del director"
    )
    
    # Números con validación de rango
    duracion_min: int = Field(
        gt=0,
        lt=600,
        description="Duración en minutos (entre 1 y 600)"
    )
    
    presupuesto_millones: float = Field(
        gt=0,
        description="Presupuesto en millones de dólares"
    )
    
    # Booleano con valor por defecto
    disponible: bool = Field(default=True)
    
    # Fechas
    fecha_estreno: date = Field(
        ge=date(1900, 1, 1),
        description="Fecha de estreno en cines"
    )
    
    creado_en: datetime = Field(
        default_factory=datetime.utcnow,
        description="Fecha y hora de creación del registro"
    )
    
    # Campo opcional con validación
    puntuacion: Optional[float] = Field(
        default=None,
        ge=0,
        le=10,
        description="Puntuación de 0 a 10"
    )
```

### Ejemplo 2: Modelo de Usuario con Validaciones

```python
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date

class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Email único con validación regex
    email: str = Field(
        unique=True,
        max_length=255,
        pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
        description="Dirección de correo electrónico"
    )
    
    # Nombre con validación de longitud
    nombre: str = Field(
        min_length=2,
        max_length=50,
        description="Nombre del usuario"
    )
    
    # Edad con validación de rango
    edad: int = Field(
        ge=0,
        le=120,
        description="Edad del usuario"
    )
    
    # Teléfono con validación regex
    telefono: Optional[str] = Field(
        default=None,
        pattern=r'^\d{9}$',
        description="Teléfono de 9 dígitos"
    )
    
    # Fecha de nacimiento
    fecha_nacimiento: date = Field(
        le=date.today(),
        description="Fecha de nacimiento"
    )
```

### Ejemplo 3: Modelo de Producto

```python
from sqlmodel import SQLModel, Field
from typing import Optional
from decimal import Decimal

class Producto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Código único
    codigo: str = Field(
        unique=True,
        max_length=20,
        pattern=r'^[A-Z0-9-]+$',
        description="Código único del producto"
    )
    
    # Nombre indexado
    nombre: str = Field(
        index=True,
        max_length=200,
        description="Nombre del producto"
    )
    
    # Precio con validación
    precio: float = Field(
        gt=0,
        multiple_of=0.01,  # Centavos
        description="Precio en euros"
    )
    
    # Stock mínimo
    stock: int = Field(
        ge=0,
        default=0,
        description="Cantidad en stock"
    )
    
    # Descuento opcional
    descuento: Optional[float] = Field(
        default=None,
        ge=0,
        le=100,
        description="Porcentaje de descuento (0-100)"
    )
```

---

## Resumen de Parámetros Comunes

| Parámetro | Tipo | Descripción | Ejemplo |
|-----------|------|-------------|---------|
| `default` | Cualquiera | Valor por defecto | `Field(default=True)` |
| `default_factory` | Callable | Función que genera el valor | `Field(default_factory=datetime.utcnow)` |
| `primary_key` | bool | Clave primaria | `Field(primary_key=True)` |
| `index` | bool | Crear índice en BD | `Field(index=True)` |
| `unique` | bool | Valores únicos | `Field(unique=True)` |
| `nullable` | bool | Permite NULL | `Field(nullable=True)` |
| `max_length` | int | Longitud máxima (strings) | `Field(max_length=100)` |
| `min_length` | int | Longitud mínima (strings) | `Field(min_length=3)` |
| `ge` | Number | Mayor o igual que | `Field(ge=0)` |
| `gt` | Number | Mayor que | `Field(gt=0)` |
| `le` | Number | Menor o igual que | `Field(le=100)` |
| `lt` | Number | Menor que | `Field(lt=100)` |
| `multiple_of` | Number | Múltiplo de | `Field(multiple_of=5)` |
| `pattern` / `regex` | str | Expresión regular | `Field(pattern=r'^\d+$')` |
| `title` | str | Título del campo | `Field(title="Nombre")` |
| `description` | str | Descripción del campo | `Field(description="...")` |
| `example` | Cualquiera | Ejemplo de valor | `Field(example="ejemplo")` |
| `alias` | str | Nombre alternativo | `Field(alias="nombre_alt")` |
| `deprecated` | bool | Campo deprecado | `Field(deprecated=True)` |
| `const` | Cualquiera | Valor constante | `Field(const="valor")` |
| `sa_column` | Column | Columna SQLAlchemy | `Field(sa_column=Column(...))` |

---

## Consejos y Mejores Prácticas

### 1. **Usa índices en campos de búsqueda frecuente**
```python
titulo: str = Field(index=True, max_length=100)
director: str = Field(index=True, max_length=80)
```

### 2. **Combina validaciones para mayor seguridad**
```python
puntuacion: float = Field(ge=0, le=10, description="Puntuación de 0 a 10")
```

### 3. **Usa `default_factory` para valores dinámicos**
```python
creado_en: datetime = Field(default_factory=datetime.utcnow)
```

### 4. **Documenta tus campos con `description`**
```python
duracion_min: int = Field(
    gt=0,
    lt=600,
    description="Duración en minutos. Debe estar entre 1 y 600."
)
```

### 5. **Valida emails y códigos con regex**
```python
email: str = Field(pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
```

### 6. **Usa `unique=True` para campos que deben ser únicos**
```python
email: str = Field(unique=True, max_length=255)
codigo: str = Field(unique=True, max_length=20)
```

---

## Referencias

- **Documentación oficial de Pydantic**: https://docs.pydantic.dev/latest/concepts/fields/
- **Documentación oficial de SQLModel**: https://sqlmodel.tiangolo.com/
- **Validadores personalizados**: https://docs.pydantic.dev/latest/concepts/validators/

---

¡Feliz modelado! 🎉
