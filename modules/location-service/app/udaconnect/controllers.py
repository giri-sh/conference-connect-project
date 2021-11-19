from datetime import datetime
import logging

from app.udaconnect.models import Location
from app.udaconnect.schemas import (
    LocationSchema,
)
from app.udaconnect.services import LocationService
from flask import request, g, Response
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource
from typing import Optional, List

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("loc-service-api")

api = Namespace("loc_service_api", description="Connections via geolocation.")

@api.route("/locations")
class LocationResourcePost(Resource):
    @accepts(schema=LocationSchema)
    @responds(schema=LocationSchema)
    def post(self) :
        logger.info("Calling Location controller")
        logger.info(request)
        json_data = request.get_json()
        logger.info(json_data)
        location: Location = LocationService.create(json_data)
        return Response(status="Success")

    @responds(schema=LocationSchema)
    def get(self) -> Location:
        logger.info("Get Location controller")
        location: Location = LocationService.retrieve()
        return location


@api.route("/locations/<location_id>")
@api.param("location_id", "Unique ID for a given Location", _in="query")
class LocationResource(Resource):
    @responds(schema=LocationSchema)
    def get(self, location_id) -> Location:
        logger.info("Get Location controller")
        location: Location = LocationService.retrieve(location_id)
        return location
