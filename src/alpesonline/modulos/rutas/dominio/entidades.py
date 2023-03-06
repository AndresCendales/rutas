"""Entidades del dominio de rutas

En este archivo usted encontrará las entidades del dominio de rutas

"""

from __future__ import annotations
from dataclasses import dataclass, field
import datetime

import alpesonline.modulos.rutas.dominio.objetos_valor as ov
from alpesonline.modulos.rutas.dominio.eventos import RutaProgramada
from alpesonline.seedwork.dominio.entidades import AgregacionRaiz, Entidad

@dataclass
class Orden(Entidad):
    tipo: str = field(default_factory="mercado")
    origen: ov.Ubicacion= field(default_factory=ov.Ubicacion)
    destino: ov.Ubicacion= field(default_factory=ov.Ubicacion)
    zona: ov.Zona= field(default_factory=ov.Zona)
    tiempo_estimado: int= field(default_factory=10)
    parada: int= field(default_factory=1)

@dataclass
class Ruta(AgregacionRaiz):
    ordenes: list[Orden] = field(default_factory=list[Orden])

    def programar_ruta(self, ruta: Ruta):
        self.ordenes = ruta.ordenes
        self.fecha_creacion = datetime.datetime.now()

        self.agregar_evento(RutaProgramada(id_ruta=self.id, ordenes=self.ordenes, fecha_creacion=self.fecha_creacion))
