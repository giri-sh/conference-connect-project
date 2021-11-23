from datetime import datetime
from kafka import KafkaConsumer, TopicPartition
from typing import Dict
import json
import db_ops
import logging

from models import Location
from schemas import (
    LocationSchema,
)
from geoalchemy2.functions import ST_AsText, ST_Point

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("location-service")

TOPIC_NAME = 'location_topic'
KAFKA_SERVER = 'kafka-0.kafka-headless.default.svc.cluster.local:9093'

consumer = KafkaConsumer(bootstrap_servers=KAFKA_SERVER, group_id='test-group', auto_commit_interval_ms=2000,
                         value_deserializer=lambda m: json.loads(m.decode('utf-8')))

logger.info("Calling consumer to consume the message")
tp = TopicPartition(TOPIC_NAME, 0)
consumer.assign([tp])
lastOffset = consumer.position(tp)
consumer.seek_to_beginning(tp)

while True:
    for message in consumer:
        logger.info(message)
        if message.offset == 0:
            continue
        new_location = Location()
        data = message.value
        logger.info(data)
        new_location.person_id = data["person_id"]
        new_location.creation_time = data["creation_time"]
        new_location.coordinate = ST_Point(
            data["latitude"], data["longitude"])
        db_ops.save_location_data(new_location)
        if message.offset == lastOffset - 1:
            break


# TOPIC_NAME = 'location_topic'
# KAFKA_SERVER = 'kafka-0.kafka-headless.default.svc.cluster.local:9093'

# consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers=KAFKA_SERVER,
#                          auto_offset_reset='earliest',
#                          enable_auto_commit=True,
#                          group_id='test-group',
#                          value_deserializer=lambda x: loads(x.decode('utf-8')),
#                          api_version=(0, 10, 1))

# for message in consumer:
#     logger.info("Create location service")
#     data = message.value
#     request_value = {
#         "id": int(data['id']),
#         "person_id": int(data['person_id']),
#         "coordinate": data['coordinate'],
#         "creation_time": datetime.strptime(data['creation_time'], "%Y-%m-%d")
#     }
#     logger.info(request_value)
#     db_ops.save_location_data(request_value)
