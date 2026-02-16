# 🐳 Guía Completa de Docker y Dockerfile

## 📚 Índice
1. [¿Qué es Docker?](#qué-es-docker)
2. [Conceptos Fundamentales](#conceptos-fundamentales)
3. [Instalación](#instalación)
4. [Dockerfile: Creación desde Cero](#dockerfile-creación-desde-cero)
5. [Comandos de Docker](#comandos-de-docker)
6. [Docker Compose](#docker-compose)
7. [Ejemplos Prácticos](#ejemplos-prácticos)
8. [Mejores Prácticas](#mejores-prácticas)

---

## ¿Qué es Docker?

**Docker** es una plataforma de contenedorización que permite empaquetar aplicaciones y sus dependencias en contenedores ligeros y portátiles. 

### ¿Por qué usar Docker?

- ✅ **Consistencia**: Tu aplicación funciona igual en desarrollo, pruebas y producción
- ✅ **Aislamiento**: Cada aplicación corre en su propio entorno
- ✅ **Portabilidad**: Funciona en cualquier sistema que tenga Docker instalado
- ✅ **Escalabilidad**: Fácil de escalar y gestionar múltiples instancias
- ✅ **Simplicidad**: No necesitas instalar dependencias directamente en tu máquina

### Analogía Simple
Imagina Docker como una **caja de transporte**:
- La caja (contenedor) contiene tu aplicación y todo lo que necesita
- Puedes mover la caja a cualquier lugar (servidor, otra computadora)
- La caja siempre funciona igual, sin importar dónde esté

---

## Conceptos Fundamentales

### 1. **Imagen (Image)**
Una imagen es una plantilla de solo lectura que contiene las instrucciones para crear un contenedor. Es como una "receta" o "molde".

**Ejemplo**: `python:3.13-slim` es una imagen que contiene Python 3.13

### 2. **Contenedor (Container)**
Un contenedor es una instancia ejecutable de una imagen. Es como una "casa construida con el molde".

**Ejemplo**: Cuando ejecutas `docker run python:3.13-slim`, creas un contenedor basado en esa imagen

### 3. **Dockerfile**
Un archivo de texto que contiene instrucciones para construir una imagen. Es como las instrucciones de un manual de construcción.

### 4. **Docker Compose**
Una herramienta para definir y ejecutar aplicaciones multi-contenedor usando un archivo YAML.

### 5. **Volumen (Volume)**
Almacenamiento persistente que sobrevive incluso si el contenedor se elimina.

### 6. **Red (Network)**
Permite que los contenedores se comuniquen entre sí.

---

## Instalación

### Windows
1. Descarga **Docker Desktop** desde: https://www.docker.com/products/docker-desktop
2. Instala y reinicia tu computadora
3. Verifica la instalación:
```bash
docker --version
docker-compose --version
```

### Linux (Ubuntu/Debian)
```bash
# Actualizar paquetes
sudo apt update

# Instalar Docker
sudo apt install docker.io docker-compose

# Agregar tu usuario al grupo docker (para no usar sudo)
sudo usermod -aG docker $USER

# Reiniciar sesión o ejecutar:
newgrp docker

# Verificar instalación
docker --version
```

---

## Dockerfile: Creación desde Cero

Un **Dockerfile** es un archivo de texto sin extensión que contiene instrucciones para construir una imagen Docker.

### Estructura Básica de un Dockerfile

```dockerfile
# Comentario: Las líneas que empiezan con # son comentarios

# 1. Imagen base (FROM)
FROM python:3.13-slim

# 2. Directorio de trabajo (WORKDIR)
WORKDIR /app

# 3. Copiar archivos (COPY)
COPY requirements.txt .

# 4. Ejecutar comandos (RUN)
RUN pip install -r requirements.txt

# 5. Copiar código de la aplicación
COPY ./src /app

# 6. Exponer puertos (EXPOSE)
EXPOSE 8000

# 7. Variables de entorno (ENV)
ENV PYTHONPATH=/app

# 8. Comando por defecto (CMD)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Instrucciones del Dockerfile Explicadas

#### **FROM**
Especifica la imagen base sobre la cual construirás tu imagen.

```dockerfile
FROM python:3.13-slim
# Usa la imagen oficial de Python 3.13 en versión slim (más ligera)
```

**Variantes comunes**:
- `python:3.13` - Imagen completa con muchas herramientas
- `python:3.13-slim` - Versión ligera, recomendada para producción
- `python:3.13-alpine` - Versión ultra-ligera basada en Alpine Linux

#### **WORKDIR**
Establece el directorio de trabajo para las siguientes instrucciones.

```dockerfile
WORKDIR /app
# Crea el directorio /app si no existe y lo establece como directorio actual
# Equivale a: mkdir -p /app && cd /app
```

#### **COPY**
Copia archivos o directorios desde el host al contenedor.

```dockerfile
COPY requirements.txt .
# Copia requirements.txt desde el directorio actual del host
# al directorio actual del contenedor (que es /app por el WORKDIR)

COPY ./src /app
# Copia todo el contenido de ./src al directorio /app del contenedor
```

**Sintaxis**: `COPY <origen> <destino>`

#### **RUN**
Ejecuta comandos durante la construcción de la imagen.

```dockerfile
RUN pip install -r requirements.txt
# Instala las dependencias de Python cuando se construye la imagen
```

**Importante**: Cada `RUN` crea una nueva capa. Combina comandos cuando sea posible:
```dockerfile
# ❌ Malo (crea 2 capas)
RUN apt-get update
RUN apt-get install -y git

# ✅ Bueno (crea 1 capa)
RUN apt-get update && apt-get install -y git
```

#### **ENV**
Define variables de entorno que estarán disponibles en el contenedor.

```dockerfile
ENV PYTHONPATH=/app
ENV NODE_ENV=production
# O múltiples en una línea:
ENV PYTHONPATH=/app NODE_ENV=production
```

#### **EXPOSE**
Documenta qué puertos expondrá el contenedor (no abre el puerto, solo documenta).

```dockerfile
EXPOSE 8000
# Indica que la aplicación usará el puerto 8000
```

#### **CMD**
Define el comando por defecto que se ejecutará cuando se inicie el contenedor.

```dockerfile
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
# Forma exec (recomendada): usa formato JSON array
```

**Formas de escribir CMD**:
```dockerfile
# Forma exec (recomendada)
CMD ["python", "app.py"]

# Forma shell
CMD python app.py
```

**Diferencia**: La forma exec evita problemas con señales y es más eficiente.

#### **ENTRYPOINT**
Similar a CMD, pero los argumentos pasados a `docker run` se añaden al comando.

```dockerfile
ENTRYPOINT ["python"]
# Si ejecutas: docker run mi-imagen app.py
# Se ejecutará: python app.py
```

#### **ARG**
Define variables que se pueden pasar durante el build.

```dockerfile
ARG VERSION=latest
# Se puede pasar con: docker build --build-arg VERSION=1.0 .
```

#### **.dockerignore**
Archivo (similar a .gitignore) que especifica qué archivos NO copiar al contenedor.

**Ejemplo de .dockerignore**:
```
__pycache__
*.pyc
.git
.env
node_modules
*.md
```

---

## Comandos de Docker

### Comandos Básicos

#### **docker --version**
Muestra la versión de Docker instalada.
```bash
docker --version
# Output: Docker version 24.0.0, build xxxxx
```

#### **docker info**
Muestra información detallada del sistema Docker.
```bash
docker info
# Muestra: versión, contenedores, imágenes, espacio usado, etc.
```

#### **docker help**
Muestra ayuda sobre comandos de Docker.
```bash
docker help
docker help run        # Ayuda específica del comando run
docker help build      # Ayuda específica del comando build
```

---

### Gestión de Imágenes

#### **docker images**
Lista todas las imágenes locales.
```bash
docker images
# Muestra: REPOSITORY, TAG, IMAGE ID, CREATED, SIZE

docker images -a        # Muestra todas las imágenes (incluyendo intermedias)
docker images --filter "dangling=true"  # Muestra imágenes huérfanas
```

#### **docker pull**
Descarga una imagen desde Docker Hub u otro registro.
```bash
docker pull python:3.13-slim
# Descarga la imagen oficial de Python 3.13 slim
```

#### **docker build**
Construye una imagen desde un Dockerfile.
```bash
docker build -t mi-app:latest .
# -t: etiqueta/nombre de la imagen (tag)
# . : contexto de construcción (directorio actual)

docker build -t mi-app:v1.0 -f Dockerfile.prod .
# -f: especifica un Dockerfile diferente
```

#### **docker rmi**
Elimina una o más imágenes.
```bash
docker rmi python:3.13-slim
# Elimina la imagen especificada

docker rmi $(docker images -q)
# Elimina todas las imágenes (¡cuidado!)

docker rmi $(docker images -f "dangling=true" -q)
# Elimina solo imágenes huérfanas
```

#### **docker image prune**
Limpia imágenes no utilizadas.
```bash
docker image prune              # Elimina imágenes huérfanas
docker image prune -a           # Elimina todas las imágenes no utilizadas
docker image prune -a --force   # Sin confirmación
```

---

### Gestión de Contenedores

#### **docker run**
Crea y ejecuta un contenedor desde una imagen.
```bash
docker run python:3.13-slim python --version
# Ejecuta un comando en un contenedor temporal

docker run -d python:3.13-slim python -m http.server 8000
# -d: ejecuta en segundo plano (detached mode)

docker run -p 8080:8000 mi-app
# -p: mapea puertos (host:contenedor)
# Accede desde el host en localhost:8080

docker run -e VAR=valor mi-app
# -e: define variables de entorno

docker run -v /ruta/host:/ruta/contenedor mi-app
# -v: monta un volumen (bind mount)

docker run --name mi-contenedor mi-app
# --name: asigna un nombre al contenedor

docker run --rm mi-app
# --rm: elimina el contenedor automáticamente al detenerse
```

#### **docker ps**
Lista contenedores en ejecución.
```bash
docker ps
# Muestra contenedores activos

docker ps -a
# Muestra todos los contenedores (incluyendo detenidos)

docker ps -q
# Solo muestra los IDs de los contenedores

docker ps --filter "status=exited"
# Filtra por estado
```

#### **docker start**
Inicia un contenedor detenido.
```bash
docker start mi-contenedor
# Inicia el contenedor con el nombre especificado

docker start -a mi-contenedor
# -a: muestra la salida (attach)
```

#### **docker stop**
Detiene un contenedor en ejecución.
```bash
docker stop mi-contenedor
# Detiene el contenedor (envía señal SIGTERM, luego SIGKILL si no responde)

docker stop $(docker ps -q)
# Detiene todos los contenedores en ejecución
```

#### **docker restart**
Reinicia un contenedor.
```bash
docker restart mi-contenedor
```

#### **docker rm**
Elimina uno o más contenedores.
```bash
docker rm mi-contenedor
# Elimina el contenedor (debe estar detenido)

docker rm -f mi-contenedor
# -f: fuerza la eliminación (detiene y elimina)

docker rm $(docker ps -a -q)
# Elimina todos los contenedores detenidos
```

#### **docker container prune**
Limpia contenedores detenidos.
```bash
docker container prune
# Elimina todos los contenedores detenidos
```

#### **docker exec**
Ejecuta un comando en un contenedor en ejecución.
```bash
docker exec mi-contenedor ls -la
# Ejecuta un comando en el contenedor

docker exec -it mi-contenedor bash
# -i: modo interactivo
# -t: asigna una terminal
# Abre una shell bash dentro del contenedor

docker exec -it mi-contenedor sh
# Abre shell sh (útil si bash no está disponible)
```

#### **docker logs**
Muestra los logs de un contenedor.
```bash
docker logs mi-contenedor
# Muestra todos los logs

docker logs -f mi-contenedor
# -f: sigue los logs en tiempo real (como tail -f)

docker logs --tail 100 mi-contenedor
# Muestra las últimas 100 líneas

docker logs --since 1h mi-contenedor
# Muestra logs de la última hora
```

#### **docker inspect**
Muestra información detallada de un contenedor o imagen.
```bash
docker inspect mi-contenedor
# Muestra información completa en JSON

docker inspect --format='{{.NetworkSettings.IPAddress}}' mi-contenedor
# Muestra solo la IP del contenedor
```

---

### Redes y Volúmenes

#### **docker network ls**
Lista todas las redes.
```bash
docker network ls
```

#### **docker network create**
Crea una nueva red.
```bash
docker network create mi-red
# Crea una red personalizada
```

#### **docker network connect**
Conecta un contenedor a una red.
```bash
docker network connect mi-red mi-contenedor
```

#### **docker volume ls**
Lista todos los volúmenes.
```bash
docker volume ls
```

#### **docker volume create**
Crea un volumen.
```bash
docker volume create mi-volumen
```

---

### Comandos Útiles para Desarrollo

#### **docker-compose up**
Construye e inicia los servicios definidos en docker-compose.yml.
```bash
docker-compose up
# Inicia los servicios en primer plano

docker-compose up -d
# -d: inicia en segundo plano (detached)

docker-compose up --build
# --build: reconstruye las imágenes antes de iniciar
```

#### **docker-compose down**
Detiene y elimina los contenedores, redes y volúmenes.
```bash
docker-compose down
# Detiene y elimina contenedores

docker-compose down -v
# -v: también elimina los volúmenes
```

#### **docker-compose ps**
Lista los servicios definidos en docker-compose.yml.
```bash
docker-compose ps
```

#### **docker-compose logs**
Muestra los logs de los servicios.
```bash
docker-compose logs
docker-compose logs -f          # Sigue los logs
docker-compose logs servicio1   # Logs de un servicio específico
```

#### **docker-compose exec**
Ejecuta un comando en un servicio en ejecución.
```bash
docker-compose exec fastapi-app bash
# Abre bash en el servicio fastapi-app
```

---

### Comandos de Limpieza

#### **docker system prune**
Limpia recursos no utilizados.
```bash
docker system prune
# Elimina contenedores detenidos, redes no utilizadas, imágenes huérfanas

docker system prune -a
# También elimina imágenes no utilizadas

docker system prune -a --volumes
# También elimina volúmenes no utilizados

docker system df
# Muestra el uso de disco de Docker
```

---

## Docker Compose

**Docker Compose** permite definir y ejecutar aplicaciones multi-contenedor usando un archivo YAML.

### Estructura de docker-compose.yml

```yaml
version: '3.8'  # Versión del formato (opcional en versiones recientes)

services:       # Define los servicios (contenedores)
  web:          # Nombre del servicio
    build:      # Construir desde Dockerfile
      context: .
      dockerfile: Dockerfile
    ports:      # Mapeo de puertos
      - "8080:8000"
    environment: # Variables de entorno
      - VAR=valor
    volumes:    # Volúmenes
      - ./src:/app
    depends_on: # Dependencias
      - db

  db:           # Segundo servicio
    image: postgres:16
    environment:
      POSTGRES_DB: mydb
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - db-data:/var/lib/postgresql/data

volumes:        # Volúmenes nombrados
  db-data:
```

### Ejemplo Real (Basado en tu Proyecto)

```yaml
name: fastapi-peliculas-avanzadas

services: 
  fastapi-app:  
    build:  
      context: .  
      dockerfile: Dockerfile  
    container_name: app-peliculas-avanzadas
    restart: always  
    ports:  
      - "8080:8000"  
    depends_on:  
      - fastapi-db
    environment:
      - DB_SERVER=fastapi-db
      
  fastapi-db:  
    image: postgres:16
    container_name: db-peliculas-avanzadas  
    environment:  
      POSTGRES_DB: ${DB_NAME}
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    ports:  
      - "5432:5432"
    volumes:
      - postgres-data:/var/lib/postgresql/data

volumes:
  postgres-data:
```

---

## Ejemplos Prácticos

### Ejemplo 1: Dockerfile Simple para Python

```dockerfile
# Imagen base
FROM python:3.13-slim

# Directorio de trabajo
WORKDIR /app

# Copiar requirements primero (para aprovechar cache de Docker)
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY ./src /app

# Variables de entorno
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Exponer puerto
EXPOSE 8000

# Comando por defecto
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Ejemplo 2: Dockerfile Multi-etapa (Optimizado)

```dockerfile
# Etapa 1: Construcción
FROM python:3.13-slim as builder

WORKDIR /app

# Instalar dependencias de compilación
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependencias
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Etapa 2: Imagen final (más ligera)
FROM python:3.13-slim

WORKDIR /app

# Copiar solo las dependencias instaladas desde la etapa anterior
COPY --from=builder /root/.local /root/.local
COPY ./src /app

ENV PATH=/root/.local/bin:$PATH
ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Ejemplo 3: Comandos Útiles para tu Proyecto

```bash
# Construir la imagen
docker build -t peliculas-app:latest .

# Ejecutar el contenedor
docker run -d -p 8080:8000 --name mi-app peliculas-app:latest

# Ver logs
docker logs -f mi-app

# Entrar al contenedor
docker exec -it mi-app bash

# Detener el contenedor
docker stop mi-app

# Eliminar el contenedor
docker rm mi-app

# Con Docker Compose
docker-compose up -d              # Iniciar en segundo plano
docker-compose logs -f            # Ver logs
docker-compose exec fastapi-app bash  # Entrar al contenedor
docker-compose down               # Detener y eliminar
```

---

## Mejores Prácticas

### 1. **Orden de Instrucciones**
Coloca las instrucciones que cambian menos frecuentemente primero para aprovechar el cache de Docker.

```dockerfile
# ✅ Bueno
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ./src /app

# ❌ Malo
COPY ./src /app
COPY requirements.txt .
RUN pip install -r requirements.txt
```

### 2. **Usa .dockerignore**
Crea un archivo `.dockerignore` para excluir archivos innecesarios:

```
__pycache__
*.pyc
.git
.env
node_modules
*.md
.DS_Store
```

### 3. **Usa Imágenes Oficiales**
Prefiere imágenes oficiales y versiones específicas:

```dockerfile
# ✅ Bueno
FROM python:3.13-slim

# ❌ Malo
FROM python:latest
```

### 4. **Minimiza el Número de Capas**
Combina comandos RUN cuando sea posible:

```dockerfile
# ✅ Bueno
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ❌ Malo
RUN apt-get update
RUN apt-get install -y git
RUN apt-get install -y curl
```

### 5. **No Ejecutes como Root**
Crea un usuario no privilegiado:

```dockerfile
RUN useradd -m -u 1000 appuser
USER appuser
```

### 6. **Usa Variables de Entorno para Configuración**
```dockerfile
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
```

### 7. **Etiqueta tus Imágenes**
```bash
docker build -t mi-app:v1.0.0 .
docker build -t mi-app:latest .
```

### 8. **Documenta tu Dockerfile**
Añade comentarios explicativos:

```dockerfile
# Instalar dependencias del sistema necesarias para compilar paquetes Python
RUN apt-get update && apt-get install -y gcc
```

---

## Solución de Problemas Comunes

### El contenedor se detiene inmediatamente
```bash
# Ver logs para entender qué pasó
docker logs nombre-contenedor

# Ejecutar en modo interactivo para debuggear
docker run -it mi-imagen bash
```

### Puerto ya en uso
```bash
# Cambiar el puerto en el mapeo
docker run -p 8081:8000 mi-app
```

### Permisos denegados
```bash
# En Linux, agregar usuario al grupo docker
sudo usermod -aG docker $USER
newgrp docker
```

### Limpiar todo Docker
```bash
# ⚠️ CUIDADO: Esto elimina TODO
docker system prune -a --volumes
```

---

## Recursos Adicionales

- **Documentación Oficial**: https://docs.docker.com/
- **Docker Hub**: https://hub.docker.com/
- **Dockerfile Best Practices**: https://docs.docker.com/develop/develop-images/dockerfile_best-practices/

---

## Glosario Rápido

- **Imagen**: Plantilla de solo lectura para crear contenedores
- **Contenedor**: Instancia ejecutable de una imagen
- **Dockerfile**: Archivo con instrucciones para construir una imagen
- **Docker Compose**: Herramienta para gestionar aplicaciones multi-contenedor
- **Volumen**: Almacenamiento persistente
- **Red**: Conexión entre contenedores
- **Tag**: Etiqueta/versión de una imagen
- **Registry**: Repositorio de imágenes (ej: Docker Hub)

---

¡Feliz contenedorización! 🐳
