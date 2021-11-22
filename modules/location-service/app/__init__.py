from flask import Flask, jsonify, g
from flask_cors import CORS
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from kafka import KafkaProducer, KafkaConsumer, TopicPartition
import json
from app.udaconnect.models import Location
from geoalchemy2.functions import ST_AsText, ST_Point
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("loc-service-api")

db = SQLAlchemy()


def create_app(env=None):
    from app.config import config_by_name
    from app.routes import register_routes

    app = Flask(__name__)
    app.config.from_object(config_by_name[env or "test"])
    api = Api(app, title="Location Service API", version="0.0.1")

    CORS(app)  # Set CORS for development

    register_routes(api, app)
    db.init_app(app)
    app.app_context().push()

    KAFKA_SERVER = 'kafka-0.kafka-headless.default.svc.cluster.local:9093'
    # producer = KafkaProducer(bootstrap_servers = KAFKA_SERVER, value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    consumer = KafkaConsumer(bootstrap_servers=KAFKA_SERVER,
                             value_deserializer=lambda m: json.loads(m.decode('utf-8')))
    # g.kafka_producer = producer
    # g.kafka_consumer = consumer
    # consumer = g.kafka_consumer
    TOPIC_NAME = 'location_topic'
    logger.info("Calling consumer to consume the message")
    tp = TopicPartition(TOPIC_NAME, 0)
    consumer.assign([tp])
    lastOffset = consumer.position(tp)
    consumer.seek_to_beginning(tp)

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
        db.session.add(new_location)
        db.session.commit()
        if message.offset == lastOffset - 1:
            break

    # @app.before_request
    # def before_request():

    @app.route("/health")
    def health():
        return jsonify("healthy")

    return app
