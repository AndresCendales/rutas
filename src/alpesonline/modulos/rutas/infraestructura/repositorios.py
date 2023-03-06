""" Repositorios para el manejo de persistencia de objetos de dominio en la capa de infrastructura del dominio de rutas

En este archivo usted encontrará las diferentes repositorios para
persistir objetos dominio (agregaciones) en la capa de infraestructura del dominio de rutas

"""

from alpesonline.config.db import db
from alpesonline.modulos.rutas.dominio.repositorios import RepositorioRutas, RepositorioEventosRutas
from alpesonline.modulos.rutas.dominio.entidades import Ruta
from alpesonline.modulos.rutas.dominio.fabricas import FabricaRutas
from .dto import Ruta as RutaDTO
from .dto import EventosRuta
from .mapeadores import MapeadorRuta, MapadeadorEventosRuta
from uuid import UUID
from pulsar.schema import *

class RepositorioRutasSQLAlchemy(RepositorioRutas):

    def __init__(self):
        self._fabrica_rutas: FabricaRutas = FabricaRutas()

    @property
    def fabrica_rutas(self):
        return self._fabrica_rutas

    def obtener_por_id(self, id: UUID) -> Ruta:
        ruta_dto = db.session.query(RutaDTO).filter_by(id=str(id)).one()
        return self.fabrica_rutas.crear_objeto(ruta_dto, MapeadorRuta())

    def obtener_todos(self) -> list[Ruta]:
        # TODO
        raise NotImplementedError

    def agregar(self, ruta: Ruta):
        ruta_dto = self.fabrica_rutas.crear_objeto(ruta, MapeadorRuta())

        db.session.add(ruta_dto)

    def actualizar(self, ruta: Ruta):
        # TODO
        raise NotImplementedError

    def eliminar(self, ruta_id: UUID):
        # TODO
        raise NotImplementedError

class RepositorioEventosRutaSQLAlchemy(RepositorioEventosRutas):

    def __init__(self):
        self._fabrica_rutas: FabricaRutas = FabricaRutas()

    @property
    def fabrica_rutas(self):
        return self._fabrica_rutas

    def obtener_por_id(self, id: UUID) -> Ruta:
        ruta_dto = db.session.query(RutaDTO).filter_by(id=str(id)).one()
        return self.fabrica_rutas.crear_objeto(ruta_dto, MapadeadorEventosRuta())

    def obtener_todos(self) -> list[Ruta]:
        raise NotImplementedError

    def agregar(self, evento):
        ruta_evento = self.fabrica_rutas.crear_objeto(evento, MapadeadorEventosRuta())

        parser_payload = JsonSchema(ruta_evento.data.__class__)
        json_str = parser_payload.encode(ruta_evento.data)

        evento_dto = EventosRuta()
        evento_dto.id = str(evento.id)
        evento_dto.id_entidad = str(evento.id_ruta)
        evento_dto.fecha_evento = evento.fecha_creacion
        evento_dto.version = str(ruta_evento.specversion)
        evento_dto.tipo_evento = evento.__class__.__name__
        evento_dto.formato_contenido = 'JSON'
        evento_dto.nombre_servicio = str(ruta_evento.service_name)
        evento_dto.contenido = json_str

        db.session.add(evento_dto)

    def actualizar(self, ruta: Ruta):
        raise NotImplementedError

    def eliminar(self, ruta_id: UUID):
        raise NotImplementedError
