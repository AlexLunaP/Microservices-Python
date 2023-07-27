# web_display.py
import logging
from flask import Flask, jsonify, request, render_template
import grpc
import text_analyser_pb2
import text_analyser_pb2_grpc
import grpc
from google.protobuf import empty_pb2

def get_statistics():
    print("Fetching statistics from Statistics Storage microservice.")
    with grpc.insecure_channel('localhost:50002') as channel:
        print("Channel created. Making gRPC call.")
        stub = text_analyser_pb2_grpc.StatisticsStorageServiceStub(channel)
        try:
            # Create an empty gRPC request
            empty_request = empty_pb2.Empty()
            response = stub.GetStatistics(empty_request)
            print("Successfully fetched statistics from Statistics Storage microservice.")
            return response
        except grpc.RpcError as e:
            print(f"Error fetching statistics from Statistics Storage microservice: {e}")
            return None

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('home_template.html')

@app.route('/statistics', methods=['GET','POST'])
def display_statistics():
    statistics = get_statistics()

    # Check if the statistics is not None (i.e., no error occurred)
    if statistics is not None:
        # Extract the required data from the response
        words_by_frequency = dict(statistics.words_by_frequency)
        average_word_length = float(statistics.average_word_length)
        average_sentence_length = float(statistics.average_sentence_length)

         # Process the statistics as needed and format the response
        response_data = {
            'words_by_frequency': words_by_frequency,
            'average_word_length': average_word_length,
            'average_sentence_length': average_sentence_length
        }

        return render_template('statistics_template.html', statistics=response_data)
    else:
        # Return the error response to the client
        return jsonify({"error": "Error fetching statistics"}), 500
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=50003)
