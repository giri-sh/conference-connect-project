import logging
import os
import psycopg2

from models import Person
from schemas import PersonSchema
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

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
    db_conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USERNAME,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    logger.info("Connnected to Database")
    return db_conn

def get_person_by_id(id: int):
    conn = _db_connect()
    cursor = conn.cursor()
    sql = f"SELECT * FROM person WHERE id={int(id)}"
    cursor.execute(sql)
    data = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    logger.info("Retrieved data for get person by id")
    return data

def get_all_person_list():
    conn = _db_connect()
    cursor = conn.cursor()
    sql = f"SELECT * FROM person"
    cursor.execute(sql)
    data = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    logger.info("Retrieved data for get all person list")
    return data

def save_person_data(person):
    new_person = Person()
    new_person.id = person["id"]
    new_person.first_name = person["first_name"]
    new_person.last_name = person["last_name"]
    new_person.company_name = person["company_name"]
    session.add(new_person)
    session.commit()
