# main.py

import logging

from opinion_analyzer import OpinionAnalyzer
from src.grpc_server import GRPCServer

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    analyzer = OpinionAnalyzer()

    user_input = input("Select an option:\n1 - Process CSV files\n2 - Start gRPC Server\nEnter 1 or 2: ").strip()

    if user_input == '1':
        topic_path = '../data/train/topics.csv'
        opinion_path = '../data/train/opinions.csv'
        analyzer.analyze_csv(topic_path, opinion_path)
    elif user_input == '2':
        grpc_server = GRPCServer()
        grpc_server.start()
    else:
        print("Invalid input. Please enter '1' or '2'.")