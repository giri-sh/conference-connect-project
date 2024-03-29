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
        db_ops.save_person_data(request_value)
        return person_service_pb2.PersonMessage(**request_value)

    def Get(self, request, context):
        logger.info("Get person service")
        db_data = db_ops.get_person_by_id(request.id)[0]
        person = person_service_pb2.PersonMessage(
            id = db_data[0],
            first_name = db_data[1],
            last_name = db_data[2],
            company_name = db_data[3]
        )
        return person

    def GetAll(self, request, context):
        logger.info("Get all person service")
        db_data_list = db_ops.get_all_person_list()
        person_data = []
        for db_data in db_data_list:
            person = person_service_pb2.PersonMessage(
                id = db_data[0],
                first_name = db_data[1],
                last_name = db_data[2],
                company_name = db_data[3]
            )
            person_data.append(person)
        result = person_service_pb2.PersonMessageList()
        result.person_list.extend(person_data)
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
