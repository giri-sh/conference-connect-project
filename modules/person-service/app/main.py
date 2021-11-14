from datetime import datetime
from concurrent import futures

import time
import grpc
import person_service_pb2
import person_service_pb2_grpc


class PersonServicer(person_service_pb2_grpc.PersonServiceServicer):

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


# Initialize gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
person_service_pb2_grpc.add_PersonServiceServicer_to_server(PersonServicer(), server)

print("Server starting on port 5001...")
server.add_insecure_port("[::]:5001")
server.start()
# Keep thread alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
