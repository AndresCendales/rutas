from alpesonline.seedwork.aplicacion.comandos import ComandoHandler
from alpesonline.modulos.rutas.infraestructura.fabricas import FabricaRepositorio
from alpesonline.modulos.rutas.dominio.fabricas import FabricaRutas

class ProgramarRutaBaseHandler(ComandoHandler):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_rutas: FabricaRutas = FabricaRutas()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio
    
    @property
    def fabrica_rutas(self):
        return self._fabrica_rutas    
    