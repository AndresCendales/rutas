"""Objetos valor del dominio de vuelos

En este archivo usted encontrará los objetos valor del dominio de vuelos

"""

from __future__ import annotations

from dataclasses import dataclass, field
from alpesonline.seedwork.dominio.objetos_valor import ObjetoValor
from datetime import datetime
from enum import Enum

@dataclass(frozen=True)
class Ubicacion(ObjetoValor):
    longitud: str
    latitud: str

class Zona(Enum):
    NORTE = "norte"
    SUR = "sur"
    ORIENTE = "oriente"
    OCCIDENTE = "occidente"
