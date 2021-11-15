import logging
import os
import psycopg2

from models import Person
from schemas import PersonSchema
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from geoalchemy2.functions import ST_AsText, ST_Point
from typing import Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("person-service-db-ops")

DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]
DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
engine = create_engine(f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
Session = sessionmaker(bind=engine)
session = Session()

def _db_connect():
    logger.info("Connecting to Database...")
    db_conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USERNAME,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    logger.info("Connnected to Database")
    return db_conn

def getPersonById(id: int):
    conn = _db_connect()
    cursor = conn.cursor()
    if(id):
        sql = f"SELECT * FROM person WHERE id={int(id)}"
    else:
        sql = f"SELECT * FROM person"
    cursor.execute(sql)
    data = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return data

# def save_to_db(location):

#     log("SAVING LOCATION:")

#     validation_results: Dict = LocationSchema().validate(location)
#     if validation_results:
#         log(f"Unexpected data format in payload: {validation_results}")
#         raise Exception(f"Invalid payload: {validation_results}")

#     new_location = Location()
#     new_location.person_id = location["person_id"]
#     new_location.creation_time = location["creation_time"]
#     new_location.coordinate = ST_Point(location["latitude"], location["longitude"])
#     session.add(new_location)
#     session.commit()

#     return new_location