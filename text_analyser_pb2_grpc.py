# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import text_analyser_pb2 as text__analyser__pb2


class TextAnalyserServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.AnalyseText = channel.unary_unary(
                '/TextAnalyserService/AnalyseText',
                request_serializer=text__analyser__pb2.AnalysisRequest.SerializeToString,
                response_deserializer=text__analyser__pb2.AnalysisResponse.FromString,
                )


class TextAnalyserServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def AnalyseText(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_TextAnalyserServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'AnalyseText': grpc.unary_unary_rpc_method_handler(
                    servicer.AnalyseText,
                    request_deserializer=text__analyser__pb2.AnalysisRequest.FromString,
                    response_serializer=text__analyser__pb2.AnalysisResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'TextAnalyserService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class TextAnalyserService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def AnalyseText(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/TextAnalyserService/AnalyseText',
            text__analyser__pb2.AnalysisRequest.SerializeToString,
            text__analyser__pb2.AnalysisResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)