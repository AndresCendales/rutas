import alpesonline.seedwork.presentacion.api as api
import json
from alpesonline.seedwork.dominio.excepciones import ExcepcionDominio

from flask import request, session
from flask import Response
from alpesonline.modulos.rutas.aplicacion.mapeadores import MapeadorRutaDTOJson
from alpesonline.modulos.rutas.aplicacion.comandos.programar_ruta import ProgramarRuta
from alpesonline.seedwork.aplicacion.comandos import ejecutar_commando

bp = api.crear_blueprint('rutas', '/rutas')

@bp.route('/programa', methods=('POST',))
def programar_usando_comando():
    try:
        session['uow_metodo'] = 'pulsar'

        ruta_dict = request.json

        map_ruta = MapeadorRutaDTOJson()
        ruta_dto = map_ruta.externo_a_dto(ruta_dict)

        comando = ProgramarRuta(ruta_dto.fecha_creacion, ruta_dto.fecha_actualizacion, ruta_dto.id, ruta_dto.ordenes)
        
        ejecutar_commando(comando)
        
        return Response('{}', status=202, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')
