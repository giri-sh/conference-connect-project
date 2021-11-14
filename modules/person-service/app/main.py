from datetime import datetime
from concurrent import futures

import grpc
import person_service_pb2
import person_service_pb2_grpc


class PersonServicer(person_service_pb2_grpc.PersonServiceServicer) {

    def Create(self, request, context):
        request_value = {
            "id": int(request.id),
            "first_name": request.first_name,
            "last_name": request.last_name,
            "company_name": request.company_name
        }
        print(request_value)
        return person_service_pb2.PersonMessage(**request_value)

    def Get(self, request, context):
        return person_service_pb2.PersonMessage(
            id = "1",
            first_name = "G",
            last_name = "S",
            company_name = "Glob"
        )

    def GetAll(self, request, context):
        order_1 = person_service_pb2.PersonMessage(
            id = "1",
            first_name = "G",
            last_name = "S",
            company_name = "Glob"
        )
        order_2 = person_service_pb2.PersonMessage(
            id = "2",
            first_name = "S",
            last_name = "G",
            company_name = "All"
        )
        result = person_service_pb2.PersonMessageList()
        result.person_list.extend([order_1, order_2])
        return result
}


# Initialize gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
item_pb2_grpc.add_ItemServiceServicer_to_server(ItemServicer(), server)
order_pb2_grpc.add_OrderServiceServicer_to_server(OrderServicer(), server)


print("Server starting on port 5001...")
server.add_insecure_port("[::]:5001")
server.start()
# Keep thread alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)



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

