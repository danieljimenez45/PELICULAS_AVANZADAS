"""
Repositorio que encapsula todas las operaciones de acceso a datos para Películas.
Implementa el patrón Repository para separar la lógica de acceso a datos de la lógica de negocio.
"""

from sqlmodel import Session, select
from models.Pelicula import Pelicula


class PeliculasAvanzadasRepository:
    """
    Clase repositorio que gestiona todas las operaciones CRUD (Create, Read, Update, Delete)
    relacionadas con las películas en la base de datos.
    
    Utiliza SQLModel Session para interactuar con la base de datos PostgreSQL.
    """
    
    def __init__(self, session: Session):
        """
        Constructor del repositorio.
        
        Args:
            session: Sesión de SQLModel para realizar operaciones en la base de datos.
                     Esta sesión se inyecta desde fuera (patrón Dependency Injection).
        """
        self.session = session

    def get_all_peliculas_avanzadas(self) -> list[Pelicula]:
        """
        Obtiene todas las películas almacenadas en la base de datos.
        
        Returns:
            Lista de objetos Pelicula con todas las películas encontradas.
            Si no hay películas, retorna una lista vacía.
        """
        # Ejecuta una consulta SELECT * FROM pelicula
        peliculas = self.session.exec(select(Pelicula)).all()
        return peliculas
    
    def get_pelicula_avanzada(self, pelicula_id: int) -> Pelicula | None:
        """
        Obtiene una película específica por su ID.
        
        Args:
            pelicula_id: Identificador único de la película a buscar.
        
        Returns:
            Objeto Pelicula si se encuentra, None si no existe.
        """
        # Busca la película por su clave primaria (ID)
        pelicula = self.session.get(Pelicula, pelicula_id)
        return pelicula
    
    def create_pelicula_avanzada(self, pelicula: Pelicula) -> Pelicula:
        """
        Crea una nueva película en la base de datos.
        
        Args:
            pelicula: Objeto Pelicula con los datos a insertar.
        
        Returns:
            Objeto Pelicula con el ID asignado por la base de datos y datos actualizados.
        """
        # Añade la película a la sesión (prepara la inserción)
        self.session.add(pelicula)
        # Confirma la transacción (INSERT en la base de datos)
        self.session.commit()
        # Actualiza el objeto con los datos generados por la BD (como el ID autoincremental)
        self.session.refresh(pelicula)
        return pelicula
    
    def update_pelicula_avanzada(self, pelicula_id: int, pelicula_data: dict) -> Pelicula:
        """
        Actualiza los datos de una película existente.
        
        Args:
            pelicula_id: Identificador único de la película a actualizar.
            pelicula_data: Diccionario con los campos a actualizar y sus nuevos valores.
                          Solo se actualizan los campos presentes en el diccionario.
        
        Returns:
            Objeto Pelicula actualizado con los nuevos datos.
        """
        # Obtiene la película existente de la base de datos
        pelicula = self.get_pelicula_avanzada(pelicula_id)
        # Itera sobre cada campo en el diccionario y actualiza el atributo correspondiente
        # setattr(obj, 'atributo', valor) es equivalente a obj.atributo = valor
        for key, value in pelicula_data.items():
            setattr(pelicula, key, value)
        # Confirma la transacción (UPDATE en la base de datos)
        self.session.commit()
        # Actualiza el objeto con los datos finales de la BD
        self.session.refresh(pelicula)
        return pelicula
    
    def delete_pelicula_avanzada(self, pelicula_id: int) -> None:
        """
        Elimina una película de la base de datos.
        
        Args:
            pelicula_id: Identificador único de la película a eliminar.
        
        Returns:
            None
        """
        # Obtiene la película existente (necesaria para poder eliminarla)
        pelicula = self.get_pelicula_avanzada(pelicula_id)
        # Marca la película para eliminación
        self.session.delete(pelicula)
        # Confirma la transacción (DELETE en la base de datos)
        self.session.commit()
    
    def cambiar_disponibilidad_pelicula(self, pelicula_id: int, disponible: bool) -> Pelicula:
        """
        Cambia el estado de disponibilidad de una película.
        
        Args:
            pelicula_id: Identificador único de la película a modificar.
            disponible: Nuevo estado de disponibilidad (True o False).
        
        Returns:
            Objeto Pelicula actualizado con el nuevo estado de disponibilidad.
        
        Este método es más específico y eficiente que update_pelicula_avanzada
        cuando solo se necesita cambiar la disponibilidad.
        """
        # Obtiene la película existente de la base de datos
        pelicula = self.get_pelicula_avanzada(pelicula_id)
        # Actualiza solo el campo disponible
        pelicula.disponible = disponible
        # Confirma la transacción (UPDATE en la base de datos)
        self.session.commit()
        # Actualiza el objeto con los datos finales de la BD
        self.session.refresh(pelicula)
        return pelicula