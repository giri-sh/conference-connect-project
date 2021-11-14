# Conference Connect Project


### Command to generate gRPC files
python -m grpc_tools.protoc -I./ --python_out=./ --grpc_python_out=./ person-service.proto
