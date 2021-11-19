from datetime import datetime
from kafka import KafkaConsumer
from json import loads
from typing import Dict

import db_ops
import logging

from models import Location
from schemas import (
    LocationSchema,
)

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("location-service")

TOPIC_NAME = 'locations'
KAFKA_SERVER = 'kafka-0.kafka-headless.default.svc.cluster.local:9093'

consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers=KAFKA_SERVER,
     auto_offset_reset='earliest',
     enable_auto_commit=True,
     group_id='test-group',
     value_deserializer=lambda x: loads(x.decode('utf-8')),
     api_version=(0,10,1))

location_map: Dict[str, Location] = []
for message in consumer: 
    location = message.value
    location_map = loads(location.replace("'",'"'))
    logger.info(location_map)
    break

for message in consumer:
    logger.info("Create location service")
    data = message.value
    logger.info(data)
    data_map = loads(location.replace("'",'"'))
    logger.info(data_map)
    logger.info(data[1])
    request_value = {
        "id": int(data['id']),
        "person_id": int(data['person_id']),
        "coordinate": data['coordinate'],
        "creation_time": datetime.strptime(data['creation_time'], "%Y-%m-%d")
    }
    logger.info(request_value)
    db_ops.save_location_data(request_value)
