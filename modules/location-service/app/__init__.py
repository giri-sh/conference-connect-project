from flask import Flask, jsonify, g
from flask_cors import CORS
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from kafka import KafkaProducer, KafkaConsumer
import json

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

    @app.before_request
    def before_request():
        KAFKA_SERVER = 'kafka-0.kafka-headless.default.svc.cluster.local:9093'
        producer = KafkaProducer(bootstrap_servers = KAFKA_SERVER, value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        consumer = KafkaConsumer(bootstrap_servers = KAFKA_SERVER, value_deserializer=lambda m: json.loads(m.decode('utf-8')))
        g.kafka_producer = producer
        g.kafka_consumer = consumer

    @app.route("/health")
    def health():
        return jsonify("healthy")

    return app
