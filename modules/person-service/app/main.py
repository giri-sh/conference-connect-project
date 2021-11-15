from datetime import datetime
from concurrent import futures

import time
import grpc
import person_service_pb2
import person_service_pb2_grpc
import db_ops
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("person-service")


class PersonServicer(person_service_pb2_grpc.PersonServiceServicer):

    def Create(self, request, context):
        logger.info("Create person service")
        request_value = {
            "id": int(request.id),
            "first_name": request.first_name,
            "last_name": request.last_name,
            "company_name": request.company_name
        }
        logger.info(request_value)
        return person_service_pb2.PersonMessage(**request_value)

    def Get(self, request, context):
        logger.info("Get person service")
        response = person_service_pb2.PersonMessage(
            id = 1,
            first_name = "G",
            last_name = "S",
            company_name = "Glob"
        )
        logger.info(response)
        db_data = db_ops.getPersonById(request.id)
        logger.info(db_data)
        logger.info(db_data[0])
        return response

    def GetAll(self, request, context):
        logger.info("Get all person service")
        order_1 = person_service_pb2.PersonMessage(
            id = 1,
            first_name = "G",
            last_name = "S",
            company_name = "Glob"
        )
        order_2 = person_service_pb2.PersonMessage(
            id = 2,
            first_name = "S",
            last_name = "G",
            company_name = "All"
        )
        result = person_service_pb2.PersonMessageList()
        result.person_list.extend([order_1, order_2])
        logger.info(result)
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
