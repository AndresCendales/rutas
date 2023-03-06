import pulsar
from pulsar.schema import *

from alpesonline.modulos.rutas.infraestructura.schema.v1.eventos import EventoRutaProgramada
from alpesonline.modulos.rutas.infraestructura.schema.v1.comandos import ComandoProgramarRuta, ComandoProgramarRutaPayload
from alpesonline.seedwork.infraestructura import utils

from alpesonline.modulos.rutas.infraestructura.mapeadores import MapadeadorEventosRuta

class Despachador:
    def __init__(self):
        self.mapper = MapadeadorEventosRuta()

    def _publicar_mensaje(self, mensaje, topico, schema):
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        publicador = cliente.create_producer(topico, schema=AvroSchema(EventoRutaProgramada))
        publicador.send(mensaje)
        cliente.close()

    def publicar_evento(self, evento, topico):
        evento = self.mapper.entidad_a_dto(evento)
        self._publicar_mensaje(evento, topico, AvroSchema(evento.__class__))

    def publicar_comando(self, comando, topico):
        payload = ComandoProgramarRutaPayload(
            id_usuario=str(comando.id_usuario)
        )
        comando_integracion = ComandoProgramarRuta(data=payload)
        self._publicar_mensaje(comando_integracion, topico, AvroSchema(ComandoProgramarRuta))
