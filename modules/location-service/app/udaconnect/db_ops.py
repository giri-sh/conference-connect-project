import logging
import os
import psycopg2

from models import Location
from schemas import LocationSchema
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from typing import Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("location-service-db-ops")

DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]
DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
engine = create_engine(f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
Session = sessionmaker(bind=engine)
session = Session()

def save_location_data(location):
    new_location = Location()
    new_location.id = int(location["id"])
    new_location.person_id = int(location["person_id"])
    new_location.coordinate = location["coordinate"]
    new_location.creation_time = location["creation_time"]
    session.add(new_location)
    session.commit()
