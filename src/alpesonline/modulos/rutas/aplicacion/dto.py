from dataclasses import dataclass, field
from alpesonline.seedwork.aplicacion.dto import DTO

@dataclass(frozen=True)
class UbicacionDTO(DTO):
    longitud: str
    latitud: str

@dataclass(frozen=True)
class OrdenDTO(DTO):
    id: str
    tipo: str
    origen: UbicacionDTO
    destino: UbicacionDTO

@dataclass(frozen=True)
class RutaDTO(DTO):
    fecha_creacion: str = field(default_factory=str)
    fecha_actualizacion: str = field(default_factory=str)
    id: str = field(default_factory=str)
    ordenes: list[OrdenDTO] = field(default_factory=list)