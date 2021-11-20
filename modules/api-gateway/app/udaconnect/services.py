import logging
import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List
from json import dumps

import grpc
import app.udaconnect.grpc_services.person_service_pb2 as person_service_pb2
import app.udaconnect.grpc_services.person_service_pb2_grpc as person_service_pb2_grpc
from google.protobuf.json_format import MessageToDict

from app import db
from app.udaconnect.models import Connection, Location, Person
from app.udaconnect.schemas import ConnectionSchema, LocationSchema, PersonSchema
from geoalchemy2.functions import ST_AsText, ST_Point
from sqlalchemy.sql import text
from kafka import KafkaProducer

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("udaconnect-api")

ps_channel = grpc.insecure_channel("udaconnect-person-service:5001")
ps_stub = person_service_pb2_grpc.PersonServiceStub(ps_channel)

location_service_url = "http://udaconnect-location-service:5002/api/locations"

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
    def find_contacts(person_id: int, start_date: datetime, end_date: datetime, meters=5
    ) -> List[Connection]:
        """
        Finds all Person who have been within a given distance of a given Person within a date range.

        This will run rather quickly locally, but this is an expensive method and will take a bit of time to run on
        large datasets. This is by design: what are some ways or techniques to help make this data integrate more
        smoothly for a better user experience for API consumers?
        """
        locations: List = db.session.query(Location).filter(
            Location.person_id == person_id
        ).filter(Location.creation_time < end_date).filter(
            Location.creation_time >= start_date
        ).all()

        # Cache all users in memory for quick lookup
        person_map: Dict[str, Person] = {person.id: person for person in PersonService.retrieve_all()}

        # Prepare arguments for queries
        data = []
        for location in locations:
            data.append(
                {
                    "person_id": person_id,
                    "longitude": location.longitude,
                    "latitude": location.latitude,
                    "meters": meters,
                    "start_date": start_date.strftime("%Y-%m-%d"),
                    "end_date": (end_date + timedelta(days=1)).strftime("%Y-%m-%d"),
                }
            )

        query = text(
            """
        SELECT  person_id, id, ST_X(coordinate), ST_Y(coordinate), creation_time
        FROM    location
        WHERE   ST_DWithin(coordinate::geography,ST_SetSRID(ST_MakePoint(:latitude,:longitude),4326)::geography, :meters)
        AND     person_id != :person_id
        AND     TO_DATE(:start_date, 'YYYY-MM-DD') <= creation_time
        AND     TO_DATE(:end_date, 'YYYY-MM-DD') > creation_time;
        """
        )
        result: List[Connection] = []
        for line in tuple(data):
            for (
                exposed_person_id,
                location_id,
                exposed_lat,
                exposed_long,
                exposed_time,
            ) in db.engine.execute(query, **line):
                location = Location(
                    id=location_id,
                    person_id=exposed_person_id,
                    creation_time=exposed_time,
                )
                location.set_wkt_with_coords(exposed_lat, exposed_long)

                result.append(
                    Connection(
                        person=person_map[exposed_person_id], location=location,
                    )
                )

        return result
    

class LocationService:
    @staticmethod
    def retrieve(location_id) -> Location:
        if location_id:
            response = requests.get(f"{location_service_url}/{location_id}")
            logger.info(response)
            logger.info(response.json())
        else:
            response = requests.get(f"{location_service_url}")
            logger.info(response)
            logger.info(response.json())
        if(response.status_code == 200):
            location_data = json.loads(str(response.json()), object_hook=lambda d: Location(**d))
            logger.info(location_data)
            return location_data
        else:
            return {"error": response.status_code}

    @staticmethod
    def create(location: Dict) -> Location:
        logger.info(location)
        response = requests.post(f"{location_service_url}", json=location)
        logger.info(response.json())
        if(response.status_code == 200):
            new_location = response.json()
            return new_location 
        else:
            return {"error": response.status_code}
