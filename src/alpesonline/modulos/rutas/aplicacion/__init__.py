from pydispatch import dispatcher

from .handlers import HandlerRutaIntegracion

from alpesonline.modulos.rutas.dominio.eventos import RutaProgramada

dispatcher.connect(HandlerRutaIntegracion.handle_ruta_programada, signal=f'{RutaProgramada.__name__}Integracion')