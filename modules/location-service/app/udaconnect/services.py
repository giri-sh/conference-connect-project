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

TOPIC_NAME = 'location_topics'
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


logger.info("Calling consumer to consume the message")
consumer = g.kafka_consumer
tp = TopicPartition(TOPIC_NAME, 0)
consumer.assign([tp])
lastOffset = consumer.position(tp)
consumer.seek_to_beginning(tp)

for message in consumer:
    new_location = Location()
    data = message.value
    logger.info(data)
    new_location.person_id = data["person_id"]
    new_location.creation_time = data["creation_time"]
    new_location.coordinate = ST_Point(data["latitude"], data["longitude"])
    db.session.add(new_location)
    db.session.commit()
    if message.offset == lastOffset - 1:
        break
