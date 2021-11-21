import logging
import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List
from json import dumps

import grpc
import app.udaconnect.grpc_services.person_service_pb2 as person_service_pb2
import app.udaconnect.grpc_services.person_service_pb2_grpc as person_service_pb2_grpc
from google.protobuf.timestamp_pb2 import Timestamp
from google.protobuf.json_format import MessageToDict

from app import db
from app.udaconnect.models import Connection, Location, Person
from app.udaconnect.schemas import ConnectionSchema, LocationSchema, PersonSchema
from geoalchemy2.functions import ST_AsText, ST_Point
from sqlalchemy.sql import text
from kafka import KafkaProducer

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("udaconnect-api")

tS = Timestamp()
DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"

ps_channel = grpc.insecure_channel("udaconnect-person-service:5001")
ps_stub = person_service_pb2_grpc.PersonServiceStub(ps_channel)

location_service_url = "http://udaconnect-location-service:5002/api/locations"
connection_service_url = "http://udaconnect-connection-service:5003/api/persons"

class PersonService:
    @staticmethod
    def create(person: Dict) -> Person:
        logger.info("Creating details for person %s", person.get("id"))
        person_message = person_service_pb2.PersonMessage(
            id = person.get("id"),
            first_name = person.get("first_name"),
            last_name = person.get("last_name"),
            company_name = person.get("company_name")
        )
        response = ps_stub.Create(person_message)
        data = MessageToDict(message=response, preserving_proto_field_name=True)
        logger.info(data)
        return data

    @staticmethod
    def retrieve(person_id: int) -> Person:
        logger.info("Getting details for person %d", int(person_id))
        person_id_data = person_service_pb2.UniquePersonMessage(
            id = int(person_id)
        )
        response = ps_stub.Get(person_id_data)
        logger.info(response)
        data = MessageToDict(message=response, preserving_proto_field_name=True)
        logger.info(data)
        return data

    @staticmethod
    def retrieve_all() -> List[Person]:
        logger.info("Getting all person details")
        response = ps_stub.GetAll(person_service_pb2.Empty())
        logger.info(response)
        data = MessageToDict(message=response, preserving_proto_field_name=True).get('person_list')
        logger.info(data)
        return data


class ConnectionService:
    @staticmethod
    def find_contacts(person_id: int, start_date: str, end_date: str, meters=5
    ) -> List[Connection]:
        payload = {'start_date': start_date, 'end_date': end_date, 'distance': meters}
        response = requests.get(url=f"{connection_service_url}/{person_id}/connection", params=payload)
        logger.info(response.json())
        return response
    

class LocationService:
    @staticmethod
    def retrieve(location_id) -> Location:
        if location_id:
            response = requests.get(f"{location_service_url}/{location_id}")
            logger.info(response.json())
        else:
            response = requests.get(f"{location_service_url}")
            logger.info(response.json())
        if(response.status_code == 200):
            location_data = response.json()
            logger.info("Sending response")
            logger.info(location_data)
            new_location = Location()
            new_location.id = location_data['id']
            new_location.person_id = location_data['person_id']
            new_location.creation_time = datetime.strptime(location_data['creation_time'], DATE_FORMAT)
            new_location.set_wkt_with_coords(location_data['latitude'], location_data['longitude'])
            logger.info(new_location)
            return new_location
        else:
            return {"error": response.status_code}

    @staticmethod
    def create(location: Dict) -> Location:
        logger.info(location)
        response = requests.post(f"{location_service_url}", json=location)
        logger.info(response.json())
        if(response.status_code == 200):
            return location
        else:
            return {"error": response.status_code}
