import logging
from datetime import datetime, timedelta
from typing import Dict, List
from json import dumps

from app import db
from app.udaconnect.models import Location, Person
from app.udaconnect.schemas import LocationSchema
from geoalchemy2.functions import ST_AsText, ST_Point
from sqlalchemy.sql import text
from flask import g
from kafka import TopicPartition, KafkaProducer, KafkaConsumer

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("loc-service-api")

TOPIC_NAME = 'locations'
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

    @staticmethod
    def create(location: Dict) -> Location:
        logger.info(location)
        validation_results: Dict = LocationSchema().validate(location)
        if validation_results:
            logger.warning(
                f"Unexpected data format in payload: {validation_results}")
            raise Exception(f"Invalid payload: {validation_results}")
        # Kafka Operationn
        producer = g.kafka_producer
        producer.send(TOPIC_NAME, location)
        producer.flush()

        consumer = g.kafka_consumer
        tp = TopicPartition(TOPIC_NAME,0)
        consumer.assign([tp])
        lastOffset = consumer.position(tp)
        consumer.seek_to_beginning(tp)

        for message in consumer:
            data = message.value
            new_location = Location()
            new_location.person_id = int(data["person_id"])
            new_location.creation_time = datetime.strptime(data['creation_time'], DATE_FORMAT)
            new_location.coordinate = ST_Point(data["latitude"], data["longitude"])
            db.session.add(new_location)
            db.session.commit()
            if message.offset == lastOffset - 1:
                break
        return location



