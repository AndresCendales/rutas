from alpesonline.seedwork.aplicacion.comandos import Comando
from alpesonline.modulos.rutas.aplicacion.dto import OrdenDTO, RutaDTO
from .base import ProgramarRutaBaseHandler
from dataclasses import dataclass
from alpesonline.seedwork.aplicacion.comandos import ejecutar_commando as comando

from alpesonline.modulos.rutas.dominio.entidades import Ruta
from alpesonline.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from alpesonline.modulos.rutas.aplicacion.mapeadores import MapeadorRuta
from alpesonline.modulos.rutas.infraestructura.repositorios import RepositorioRutas, RepositorioEventosRutas

@dataclass
class ProgramarRuta(Comando):
    fecha_creacion: str
    fecha_actualizacion: str
    id: str
    ordenes: list[OrdenDTO]

class ProgramarRutaHandler(ProgramarRutaBaseHandler):
    
    def handle(self, comando: ProgramarRuta):
        ruta_dto = RutaDTO(
                fecha_actualizacion=comando.fecha_actualizacion
            ,   fecha_creacion=comando.fecha_creacion
            ,   id=comando.id
            ,   ordenes=comando.ordenes)

        ruta: Ruta = self.fabrica_rutas.crear_objeto(ruta_dto, MapeadorRuta())
        ruta.programar_ruta(ruta)

        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioRutas)
        repositorio_eventos = self.fabrica_repositorio.crear_objeto(RepositorioEventosRutas)

        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, ruta, repositorio_eventos_func=repositorio_eventos.agregar)
        UnidadTrabajoPuerto.commit()


@comando.register(ProgramarRuta)
def ejecutar_comando_programar_ruta(comando: ProgramarRuta):
    handler = ProgramarRutaHandler()
    handler.handle(comando)
    