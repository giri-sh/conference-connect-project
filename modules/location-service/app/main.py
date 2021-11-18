from datetime import datetime
from kafka import KafkaConsumer

import db_ops

from models import Location
from schemas import (
    LocationSchema,
)

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

TOPIC_NAME = 'location'
KAFKA_SERVER = 'kafka-0.kafka-headless.default.svc.cluster.local:9093'

consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers=KAFKA_SERVER,
     auto_offset_reset='earliest',
     enable_auto_commit=True,
     group_id='test-group',
     value_deserializer=lambda x: loads(x.decode('utf-8')),
     api_version=(0,10,1))

locations = [] 
for message in consumer:
    data = message.value
    request_value = {
        "id": data['id'],
        "person_id": data['person_id'],
        "coordinate": data['coordinate'],
        "creation_time": datetime.strptime(data['creation_time'], "%Y-%m-%d")
    }
    db_ops.save_location_data(request_value)
