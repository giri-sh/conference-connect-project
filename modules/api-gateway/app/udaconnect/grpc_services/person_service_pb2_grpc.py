# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from app.udaconnect.grpc_services import person_service_pb2 as app_dot_udaconnect_dot_grpc__services_dot_person__service__pb2


class PersonServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Create = channel.unary_unary(
                '/PersonService/Create',
                request_serializer=app_dot_udaconnect_dot_grpc__services_dot_person__service__pb2.PersonMessage.SerializeToString,
                response_deserializer=app_dot_udaconnect_dot_grpc__services_dot_person__service__pb2.PersonMessage.FromString,
                )
        self.Get = channel.unary_unary(
                '/PersonService/Get',
                request_serializer=app_dot_udaconnect_dot_grpc__services_dot_person__service__pb2.UniquePersonMessage.SerializeToString,
                response_deserializer=app_dot_udaconnect_dot_grpc__services_dot_person__service__pb2.PersonMessage.FromString,
                )
        self.GetAll = channel.unary_unary(
                '/PersonService/GetAll',
                request_serializer=app_dot_udaconnect_dot_grpc__services_dot_person__service__pb2.Empty.SerializeToString,
                response_deserializer=app_dot_udaconnect_dot_grpc__services_dot_person__service__pb2.PersonMessageList.FromString,
                )


class PersonServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Create(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Get(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetAll(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_PersonServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Create': grpc.unary_unary_rpc_method_handler(
                    servicer.Create,
                    request_deserializer=app_dot_udaconnect_dot_grpc__services_dot_person__service__pb2.PersonMessage.FromString,
                    response_serializer=app_dot_udaconnect_dot_grpc__services_dot_person__service__pb2.PersonMessage.SerializeToString,
            ),
            'Get': grpc.unary_unary_rpc_method_handler(
                    servicer.Get,
                    request_deserializer=app_dot_udaconnect_dot_grpc__services_dot_person__service__pb2.UniquePersonMessage.FromString,
                    response_serializer=app_dot_udaconnect_dot_grpc__services_dot_person__service__pb2.PersonMessage.SerializeToString,
            ),
            'GetAll': grpc.unary_unary_rpc_method_handler(
                    servicer.GetAll,
                    request_deserializer=app_dot_udaconnect_dot_grpc__services_dot_person__service__pb2.Empty.FromString,
                    response_serializer=app_dot_udaconnect_dot_grpc__services_dot_person__service__pb2.PersonMessageList.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'PersonService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class PersonService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Create(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/PersonService/Create',
            app_dot_udaconnect_dot_grpc__services_dot_person__service__pb2.PersonMessage.SerializeToString,
            app_dot_udaconnect_dot_grpc__services_dot_person__service__pb2.PersonMessage.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Get(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/PersonService/Get',
            app_dot_udaconnect_dot_grpc__services_dot_person__service__pb2.UniquePersonMessage.SerializeToString,
            app_dot_udaconnect_dot_grpc__services_dot_person__service__pb2.PersonMessage.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetAll(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/PersonService/GetAll',
            app_dot_udaconnect_dot_grpc__services_dot_person__service__pb2.Empty.SerializeToString,
            app_dot_udaconnect_dot_grpc__services_dot_person__service__pb2.PersonMessageList.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
