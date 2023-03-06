from alpesonline.seedwork.aplicacion.dto import Mapeador as AppMap
from alpesonline.seedwork.dominio.repositorios import Mapeador as RepMap
from alpesonline.modulos.rutas.dominio.entidades import Orden, Ruta
from alpesonline.modulos.rutas.dominio.objetos_valor import Zona
from .dto import RutaDTO, OrdenDTO

from datetime import datetime

class MapeadorRutaDTOJson(AppMap):
    def _procesar_orden(self, orden: dict) -> OrdenDTO:                
        return OrdenDTO(orden.get('id'), orden.get('tipo'), orden.get('origen'), orden.get('destino')) 
    
    def externo_a_dto(self, externo: dict) -> RutaDTO:
        ruta_dto = RutaDTO()
        for orden in externo.get('ordenes', list()):
            ruta_dto.ordenes.append(self._procesar_orden(orden))

        return ruta_dto

    def dto_a_externo(self, dto: RutaDTO) -> dict:
        return dto.__dict__

class MapeadorRuta(RepMap):
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'

    def _procesar_orden(self, orden_dto: OrdenDTO) -> Orden:
        return Orden(tipo=orden_dto.tipo, origen=orden_dto.origen, destino=orden_dto.destino, zona=Zona.NORTE, tiempo_estimado=10, parada=1)

    def obtener_tipo(self) -> type:
        return Ruta.__class__
    
    def entidad_a_dto(self, entidad: Ruta) -> RutaDTO:
        return RutaDTO("","","",[])

    def dto_a_entidad(self, dto: RutaDTO) -> Ruta:
        ruta = Ruta()
        ruta.ordenes = list()

        ordenes_dto: list[OrdenDTO] = dto.ordenes

        for orden_dto in ordenes_dto:
            ruta.ordenes.append(self._procesar_orden(orden_dto))
        
        return ruta
