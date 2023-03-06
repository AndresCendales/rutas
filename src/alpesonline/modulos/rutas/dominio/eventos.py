from __future__ import annotations
from dataclasses import dataclass, field
from alpesonline.seedwork.dominio.eventos import (EventoDominio)
from datetime import datetime

class EventoRuta(EventoDominio):
    ...

@dataclass
class RutaProgramada(EventoRuta):
    id_ruta: uuid.UUID = None
    ordenes: list = None
    fecha_creacion: datetime = None
    