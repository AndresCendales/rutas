""" Mapeadores para la capa de infrastructura del dominio de rutas

En este archivo usted encontrará los diferentes mapeadores
encargados de la transformación entre formatos de dominio y DTOs

"""

from alpesonline.seedwork.dominio.repositorios import Mapeador
from alpesonline.seedwork.infraestructura.utils import unix_time_millis
from alpesonline.modulos.rutas.dominio.entidades import Ruta, Orden
from alpesonline.modulos.rutas.dominio.eventos import RutaProgramada, EventoRuta

from .dto import Ruta as RutaDTO
from .dto import Orden as OrdenDTO
from .excepciones import NoExisteImplementacionParaTipoFabricaExcepcion
from pulsar.schema import *

class MapadeadorEventosRuta(Mapeador):

    # Versiones aceptadas
    versions = ('v1',)

    LATEST_VERSION = versions[0]

    def __init__(self):
        self.router = {
            RutaProgramada: self._entidad_a_ruta_programada
        }

    def obtener_tipo(self) -> type:
        return EventoRuta.__class__

    def es_version_valida(self, version):
        for v in self.versions:
            if v == version:
                return True
        return False

    def _entidad_a_ruta_programada(self, entidad: RutaProgramada, version=LATEST_VERSION):
        def v1(evento):
            from .schema.v1.eventos import RutaProgramadaPayload, EventoRutaProgramada

            payload = RutaProgramadaPayload(
                id_ruta=str(evento.id_ruta),
                fecha_creacion=int(unix_time_millis(evento.fecha_creacion))
            )
            evento_integracion = EventoRutaProgramada(id=str(evento.id))
            evento_integracion.id = str(evento.id)
            evento_integracion.time = int(unix_time_millis(evento.fecha_creacion))
            evento_integracion.specversion = str(version)
            evento_integracion.type = 'RutaProgramada'
            evento_integracion.datacontenttype = 'AVRO'
            evento_integracion.service_name = 'alpesonline'
            evento_integracion.data = payload

            return evento_integracion
                    
        if not self.es_version_valida(version):
            raise Exception(f'No se sabe procesar la version {version}')

        if version == 'v1':
            return v1(entidad)

    def entidad_a_dto(self, entidad: EventoRuta, version=LATEST_VERSION) -> RutaDTO:
        if not entidad:
            raise NoExisteImplementacionParaTipoFabricaExcepcion
        func = self.router.get(entidad.__class__, None)

        if not func:
            raise NoExisteImplementacionParaTipoFabricaExcepcion

        return func(entidad, version=version)

    def dto_a_entidad(self, dto: RutaDTO, version=LATEST_VERSION) -> Ruta:
        raise NotImplementedError


class MapeadorRuta(Mapeador):
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'

    def _procesar_orden_dto(self, ordenes_dto: list) -> list[Orden]:
        ordenes = list()
        
        for orden_dto in ordenes_dto:
            orden = Orden()
            orden.id = orden_dto.id
            orden.tipo = orden_dto.tipo
            orden.origen.latitud = orden_dto.origen_latitud
            orden.origen.longitud = orden_dto.origen_longitud
            orden.destino.latitud = orden_dto.destino.latitud
            orden.destino.longitud = orden_dto.destino.longitud
            orden.zona = orden_dto.zona
            orden.tiempo_estimado = orden_dto.tiempo_estimado
            orden.parada = orden_dto.parada
            ordenes.append(orden)


        return [Orden(ordenes)]

    def _procesar_orden(self, orden: any) -> OrdenDTO:
        orden_dto = OrdenDTO()
        orden_dto.id = orden.id
        orden_dto.tipo = orden.tipo
        orden_dto.origen_latitud = orden.origen.latitud
        orden_dto.origen_longitud = orden.origen.longitud
        orden_dto.destino_latitud = orden.destino.latitud
        orden_dto.destino_longitud = orden.destino.longitud
        orden_dto.zona = orden.zona
        orden_dto.tiempo_estimado = orden.tiempo_estimado
        orden_dto.parada = orden.parada

        return orden_dto

    def obtener_tipo(self) -> type:
        return Ruta.__class__

    def entidad_a_dto(self, entidad: Ruta) -> RutaDTO:
        
        ruta_dto = RutaDTO()
        ruta_dto.fecha_creacion = entidad.fecha_creacion
        ruta_dto.fecha_actualizacion = entidad.fecha_actualizacion
        ruta_dto.id = str(entidad.id)

        ordenes_dto = list()
        
        for orden in entidad.ordenes:
            ordenes_dto.extend(self._procesar_orden(orden))

        ruta_dto.ordenes = ordenes_dto

        return ruta_dto

    def dto_a_entidad(self, dto: RutaDTO) -> Ruta:
        ruta = Ruta(dto.id, dto.fecha_creacion, dto.fecha_actualizacion)
        ruta.ordenes = list()

        ordenes_dto: list[OrdenDTO] = dto.ordenes

        ruta.ordenes.extend(self._procesar_orden_dto(ordenes_dto))
        
        return ruta