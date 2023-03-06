"""DTOs para la capa de infrastructura del dominio de rutas

En este archivo usted encontrará los DTOs (modelos anémicos) de
la infraestructura del dominio de rutas

"""

from alpesonline.config.db import db
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, ForeignKey, Integer, Table

import uuid

Base = db.declarative_base()

# Tabla intermedia para tener la relación de muchos a muchos entre la tabla rutas y ordenes
rutas_ordenes = db.Table(
    "rutas_ordenes",
    db.Model.metadata,
    db.Column("ruta_id", db.String(40), db.ForeignKey("rutas.id")),
    db.Column("orden_id", db.String(40)),
    db.Column("tipo_orden", db.String(20)),
    db.Column("origen_latitud", db.String(10)),
    db.Column("origen_longitud", db.String(10)),
    db.Column("destino_latitud", db.String(10)),
    db.Column("destino_longitud", db.String(10)),
    db.Column("zona", db.String(10)),
    db.Column("tiempo_estimado", db.Integer),
    db.Column("parada", db.Integer),
    db.ForeignKeyConstraint(
        ["orden_id", "tipo_orden", "origen_latitud", "origen_longitud", "destino_latitud", "destino_longitud", "zona", "tiempo_estimado", "parada"],
        ["ordenes.id", "ordenes.tipo", "ordenes.origen_latitud", "ordenes.origen_longitud", "ordenes.destino_latitud", "ordenes.destino_longitud", "ordenes.zona", "ordenes.tiempo_estimado", "ordenes.parada"]
    )
)

class Orden(db.Model):
    __tablename__ = "ordenes"
    id = db.Column(db.String(40), primary_key=True)
    tipo = db.Column(db.String(20), primary_key=True, nullable=False)
    origen_latitud = db.Column(db.String(10), nullable=False, primary_key=True)
    origen_longitud = db.Column(db.String(10), nullable=False, primary_key=True)
    destino_latitud = db.Column(db.String(10), nullable=False, primary_key=True)
    destino_longitud = db.Column(db.String(10), nullable=False, primary_key=True)
    zona = db.Column(db.String(10), primary_key=True, nullable=False)
    tiempo_estimado = db.Column(db.Integer, primary_key=True, nullable=False)
    parada = db.Column(db.Integer, primary_key=True, nullable=False)

class Ruta(db.Model):
    __tablename__ = "rutas"
    id = db.Column(db.String(40), primary_key=True)
    fecha_creacion = db.Column(db.DateTime, nullable=False)
    fecha_actualizacion = db.Column(db.DateTime, nullable=False)
    ordenes = db.relationship('Orden', secondary=rutas_ordenes, backref='rutas')

class EventosRuta(db.Model):
    __tablename__ = "eventos_ruta"
    id = db.Column(db.String(40), primary_key=True)
    id_entidad = db.Column(db.String(40), nullable=False)
    fecha_evento = db.Column(db.DateTime, nullable=False)
    version = db.Column(db.String(10), nullable=False)
    tipo_evento = db.Column(db.String(100), nullable=False)
    formato_contenido = db.Column(db.String(10), nullable=False)
    nombre_servicio = db.Column(db.String(40), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
