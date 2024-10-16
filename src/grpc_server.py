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
        topics = list(request.topics)
        opinions = list(request.opinions)
        logging.info(f"Received gRPC request: Topics='{topics}', Opinions='{opinions}'")

        opinions_result, topics_result = self.analyzer.analyze_grpc(topics, opinions)

        opinion_messages = [
            opinion_analyzer_pb2.Opinion(text=text, topic=topic, type=op_type)
            for text, topic, op_type in opinions_result
        ]

        topic_messages = [
            opinion_analyzer_pb2.Topic(topic_name=topic, summary=summary, effectiveness=effectiveness)
            for topic, summary, effectiveness in topics_result
        ]

        response = opinion_analyzer_pb2.AnalyzeResponse(opinions=opinion_messages, topics=topic_messages)

        return response

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