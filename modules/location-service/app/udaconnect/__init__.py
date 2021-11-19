from app.udaconnect.models import Location, Person
from app.udaconnect.schemas import LocationSchema


def register_routes(api, app, root="api"):
    from app.udaconnect.controllers import api as loc_service_api

    api.add_namespace(loc_service_api, path=f"/{root}")
