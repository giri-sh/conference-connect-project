import logging
from datetime import datetime, timedelta
from typing import Dict, List
import json

from app import db
from app.udaconnect.models import Location, Person
from app.udaconnect.schemas import LocationSchema
from geoalchemy2.functions import ST_AsText, ST_Point
from sqlalchemy.sql import text
from flask import g
from kafka import TopicPartition, KafkaProducer, KafkaConsumer

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("loc-service-api")

DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"


class LocationService:
    @staticmethod
    def retrieve(location_id) -> Location:
        location, coord_text = (
            db.session.query(Location, Location.coordinate.ST_AsText())
            .filter(Location.id == location_id)
            .one()
        )

        # Rely on database to return text form of point to reduce overhead of conversion in app code
        location.wkt_shape = coord_text
        return location

    # @staticmethod
    # def create(location: Dict) -> Location:
    #     return location

