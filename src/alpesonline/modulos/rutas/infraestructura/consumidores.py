import pulsar,_pulsar  
from pulsar.schema import *
import uuid
import time
import logging
import traceback
import datetime

from alpesonline.modulos.rutas.infraestructura.schema.v1.eventos import EventoRutaProgramada
from alpesonline.modulos.rutas.infraestructura.schema.v1.comandos import ComandoProgramarRuta


from alpesonline.modulos.rutas.infraestructura.proyecciones import ProyeccionRutasLista
from alpesonline.seedwork.infraestructura.proyecciones import ejecutar_proyeccion
from alpesonline.seedwork.infraestructura import utils

def suscribirse_a_eventos(app=None):
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('eventos-ruta', consumer_type=_pulsar.ConsumerType.Shared,subscription_name='alpesonline-sub-eventos', schema=AvroSchema(EventoRutaProgramada))

        while True:
            mensaje = consumidor.receive()
            datos = mensaje.value().data
            print(f'Evento recibido: {datos}')

            ejecutar_proyeccion(ProyeccionRutasLista(datos.id_ruta), app=app)
            
            consumidor.acknowledge(mensaje)     

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos!')
        traceback.print_exc()
        if cliente:
            cliente.close()

def suscribirse_a_comandos(app=None):
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('comandos-ruta', consumer_type=_pulsar.ConsumerType.Shared, subscription_name='alpesonline-sub-comandos', schema=AvroSchema(ComandoProgramarRuta))

        while True:
            mensaje = consumidor.receive()
            print(f'Comando recibido: {mensaje.value().data}')

            consumidor.acknowledge(mensaje)     
            
        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de comandos!')
        traceback.print_exc()
        if cliente:
            cliente.close()