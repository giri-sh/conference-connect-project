import logging
from datetime import datetime, timedelta
from typing import Dict, List
from json import dumps

from app import db
from app.udaconnect.models import Location, Person
from app.udaconnect.schemas import LocationSchema
import db_ops
from geoalchemy2.functions import ST_AsText, ST_Point
from sqlalchemy.sql import text
from flask import g

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("loc-service-api")

TOPIC_NAME = 'locations'

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

    @staticmethod
    def create(location: Dict) -> Location:
        logger.info(location)
        validation_results: Dict = LocationSchema().validate(location)
        if validation_results:
            logger.warning(f"Unexpected data format in payload: {validation_results}")
            raise Exception(f"Invalid payload: {validation_results}")
        # Kafka Operationn
        producer = g.kafka_producer
        producer.send(TOPIC_NAME, location)
        consumer = g.kafka_consumer
        
        for message in consumer:
            data = message.value
            new_location = Location()
            new_location.id = data["id"]
            new_location.person_id = data["person_id"]
            new_location.creation_time = data["creation_time"]
            new_location.coordinate = ST_Point(data["latitude"], location["longitude"])
            db_ops.save_location_data(new_location)
        return new_location

