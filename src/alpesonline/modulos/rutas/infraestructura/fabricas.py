""" Fábricas para la creación de objetos en la capa de infrastructura del dominio de rutas

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos en la capa de infraestructura del dominio de rutas

"""

from dataclasses import dataclass, field
from alpesonline.seedwork.dominio.fabricas import Fabrica
from alpesonline.seedwork.dominio.repositorios import Repositorio
from alpesonline.seedwork.infraestructura.vistas import Vista
from alpesonline.modulos.rutas.dominio.entidades import Ruta
from alpesonline.modulos.rutas.dominio.repositorios import RepositorioRutas, RepositorioEventosRutas
from .repositorios import RepositorioRutasSQLAlchemy, RepositorioEventosRutaSQLAlchemy
from .excepciones import ExcepcionFabrica

@dataclass
class FabricaRepositorio(Fabrica):
    def crear_objeto(self, obj: type, mapeador: any = None) -> Repositorio:
        if obj == RepositorioRutas:
            return RepositorioRutasSQLAlchemy()
        elif obj == RepositorioEventosRutas:
            return RepositorioEventosRutaSQLAlchemy()
        else:
            raise ExcepcionFabrica(f'No existe fábrica para el objeto {obj}')
