import grpc
import person_service_pb2
import person_service_pb2_grpc

channel = grpc.insecure_channel("localhost:5001")
stub = person_service_pb2_grpc.PersonServiceStub(channel)

response = stub.Get(person_service_pb2.Empty())
print(response)