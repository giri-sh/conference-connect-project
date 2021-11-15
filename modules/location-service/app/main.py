from datetime import datetime
from kafka import KafkaConsumer, KafkaProducer

from app.udaconnect.models import Connection, Location, Person
from app.udaconnect.schemas import (
    ConnectionSchema,
    LocationSchema,
    PersonSchema,
)
from app.udaconnect.services import ConnectionService, LocationService, PersonService

TOPIC_NAME = 'items'
KAFKA_SERVER = 'kafka-0.kafka-headless.default.svc.cluster.local:9093'

producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER,
                        value_serializer=lambda x: dumps(x).encode('utf-8'),
                        api_version=(0,10,1))

consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers=KAFKA_SERVER,
     auto_offset_reset='earliest',
     enable_auto_commit=True,
     group_id='my-group',
     value_deserializer=lambda x: loads(x.decode('utf-8')),
     api_version=(0,10,1))

locations = [] 
for message in consumer:
    data = message.value
    tS = Timestamp()
    person_id = data['person_id']
    coordinate = data['coordinate']
    creation_time = datetime.strptime(data['creation_time'], FORMAT)
    connections = Connections.find_contacts(person_id, start_date, end_date)

#     log(connections)
#     data = {"foo---": f"{connections}" }
    producer.send('con', value=f"{connections}")


@api.route("/locations")
@api.route("/locations/<location_id>")
@api.param("location_id", "Unique ID for a given Location", _in="query")
class LocationResource(Resource):
    @accepts(schema=LocationSchema)
    @responds(schema=LocationSchema)
    def post(self) -> Location:
        request.get_json()
        location: Location = LocationService.create(request.get_json())
        return location

    @responds(schema=LocationSchema)
    def get(self, location_id) -> Location:
        location: Location = LocationService.retrieve(location_id)
        return location
