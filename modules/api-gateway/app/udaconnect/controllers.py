from datetime import datetime
import logging

from app.udaconnect.models import Connection, Location, Person
from app.udaconnect.schemas import (
    ConnectionSchema,
    LocationSchema,
    PersonSchema,
)
from app.udaconnect.services import ConnectionService, LocationService, PersonService
from flask import Flask, jsonify, request, g, Response
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource
from typing import Optional, List

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("udaconnect-api")

DATE_FORMAT = "%Y-%m-%d"

api = Namespace("UdaConnect", description="Connections via geolocation.")

@api.route("/persons")
class PersonsResource(Resource):
    @accepts(schema=PersonSchema)
    @responds(schema=PersonSchema)
    def post(self) -> Person:
        payload = request.get_json()
        new_person: Person = PersonService.create(payload)
        return new_person

    @responds(schema=PersonSchema, many=True)
    def get(self) -> List[Person]:
        persons: List[Person] = PersonService.retrieve_all()
        return persons


@api.route("/persons/<person_id>")
@api.param("person_id", "Unique ID for a given Person", _in="query")
class PersonResource(Resource):
    @responds(schema=PersonSchema)
    def get(self, person_id) -> Person:
        person: Person = PersonService.retrieve(person_id)
        return person


# @api.route("/locations")
# class LocationResourcePost(Resource):
#     @accepts(schema=LocationSchema)
#     @responds(schema=LocationSchema)
#     def post(self) -> Location:
#         logger.debug("Calling Location controller in debug mode")
#         logger.info("Calling Location controller")
#         logger.info(request)
#         json_data = request.get_json()
#         logger.info(json_data)
#         location: Location = LocationService.create(json_data)
#         return location


@api.route("/locations")
@api.route("/locations/<location_id>")
@api.param("location_id", "Unique ID for a given Location", _in="query")
class LocationResource(Resource):
    @accepts(schema=LocationSchema)
    @responds(schema=LocationSchema)
    def post(self) -> Location:
        logger.debug("Post Location controller in debug mode")
        logger.info("Post Location controller")
        logger.info(request)
        json_data = request.get_json()
        logger.info(json_data)
        location: Location = LocationService.create(json_data)
        return location

    @responds(schema=LocationSchema)
    def get(self, location_id) -> Location:
        logger.debug("Get Location controller in debug mode")
        logger.info("Get Location controller")
        location: Location = LocationService.retrieve(location_id)
        return location



@api.route("/persons/<person_id>/connection")
@api.param("start_date", "Lower bound of date range", _in="query")
@api.param("end_date", "Upper bound of date range", _in="query")
@api.param("distance", "Proximity to a given user in meters", _in="query")
class ConnectionDataResource(Resource):
    @responds(schema=ConnectionSchema, many=True)
    def get(self, person_id) -> ConnectionSchema:
        start_date: datetime = datetime.strptime(
            request.args["start_date"], DATE_FORMAT
        )
        end_date: datetime = datetime.strptime(request.args["end_date"], DATE_FORMAT)
        distance: Optional[int] = request.args.get("distance", 5)

        results = ConnectionService.find_contacts(
            person_id=person_id,
            start_date=start_date,
            end_date=end_date,
            meters=distance,
        )
        return results
