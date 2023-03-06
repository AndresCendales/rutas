from alpesonline.modulos.rutas.dominio.eventos import RutaProgramada
from alpesonline.seedwork.aplicacion.handlers import Handler
from alpesonline.modulos.rutas.infraestructura.despachadores import Despachador

class HandlerRutaIntegracion(Handler):

    @staticmethod
    def handle_ruta_programada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-ruta')
