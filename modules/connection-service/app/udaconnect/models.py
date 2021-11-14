from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from app import db  # noqa
from geoalchemy2 import Geometry
from geoalchemy2.shape import to_shape
from shapely.geometry.point import Point
from sqlalchemy import BigInteger, Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.ext.hybrid import hybrid_property

@dataclass
class Connection:
    location: Location
    person: Person