import grpc
from concurrent import futures
import time
import logging

import opinion_analyzer_pb2
import opinion_analyzer_pb2_grpc
from opinion_analyzer import OpinionAnalyzer

class OpinionAnalyzerServicer(opinion_analyzer_pb2_grpc.OpinionAnalyzerServiceServicer):
    def __init__(self, analyzer: OpinionAnalyzer):
        self.analyzer = analyzer

    def AnalyzeOpinion(self, request, context):
        topics = request.topics
        opinions = request.opinions
        logging.info(f"Received gRPC request: Topics='{topics}', Opinions='{opinions}'")
        result = self.analyzer.analyze_grpc(topics, opinions)
        return opinion_analyzer_pb2.AnalyzeResponse(analysis_result=result)

class GRPCServer:
    def __init__(self, host: str = '[::]:50051'):
        """
        Initializes the gRPC server.

        Parameters:
        - host: The address and port on which the server listens.
        """
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        self.host = host
        self.analyzer = OpinionAnalyzer()
        opinion_analyzer_pb2_grpc.add_OpinionAnalyzerServiceServicer_to_server(
            OpinionAnalyzerServicer(self.analyzer), self.server)

    def start(self):
        """
        Starts the gRPC server and keeps it running.
        """
        self.server.add_insecure_port(self.host)
        self.server.start()
        logging.info(f"gRPC server started on {self.host}")
        try:
            while True:
                time.sleep(86400)  # Sleep for a day to keep the server running
        except KeyboardInterrupt:
            self.server.stop(0)
            logging.info("gRPC server stopped.")