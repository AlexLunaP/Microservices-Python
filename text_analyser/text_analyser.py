# text_analyser.py
import grpc
from concurrent import futures
import string
import re
import text_analyser_pb2
import text_analyser_pb2_grpc
from prometheus_client import start_http_server, Counter, Summary

key_words = ["conduct", "contempt", "covid", "party", 
             "punishment", "gathering", "law", "responsibility"]

def calculate_statistics(text):
    words_by_frequency = {}
    total_words = 0
    total_words_length = 0
    total_sentences = 0

    enumeration_pattern = r'\b(?:[a-hj-zA-HJ-Z]|[ivxIVX]+)\)'
    additional_punctuation = '“”‘’–—…«»•'
    all_punctuation = string.punctuation + string.digits + additional_punctuation

    for line in text:
        line = line.strip().lower()
        cleaned_line = re.sub(enumeration_pattern, '', line)
        cleaned_line = cleaned_line.translate(str.maketrans('', '', all_punctuation))
        words = cleaned_line.lower().split()
        words = [word for word in words if word]

        total_words += len(words)
        total_words_length += sum(len(word) for word in words)
        total_sentences += len(re.findall(r'[.!?;:]', line))

        for word in words:
            total_words += 1
            total_words_length += len(word)

            if word in key_words:
                if word in words_by_frequency:
                    words_by_frequency[word] += 1
                else:
                    words_by_frequency[word] = 1

    average_word_length = total_words_length / total_words
    average_sentence_length = total_words / total_sentences

    return words_by_frequency, average_word_length, average_sentence_length

class TextAnalyserServicer(text_analyser_pb2_grpc.TextAnalyserServiceServicer):
    def AnalyseText(self, request, context):
        # Create a Prometheus counter to track the total number of requests
        REQUESTS = Counter('http_requests_total', 'Total number of HTTP requests')
        #Create a Prometheus summary to track the request processing time
        REQUEST_TIME = Summary('http_request_duration_seconds', 'HTTP request processing time')

        with REQUEST_TIME.time():
            REQUESTS.inc()
            text = request.text.splitlines()
            words_by_frequency, average_word_length, average_sentence_length = calculate_statistics(text)
            
            response = text_analyser_pb2.AnalysisResponse(
                words_by_frequency=words_by_frequency,
                average_word_length=average_word_length,
                average_sentence_length=average_sentence_length
            )

        # Create a channel to the Statistics Storage microservice
        with grpc.insecure_channel('statistics_storage:50002') as channel:
            # Create a stub for the Statistics Storage service
            stub = text_analyser_pb2_grpc.StatisticsStorageServiceStub(channel)

            # Create a request to send the calculated statistics to the Statistics Storage microservice
            storage_request = text_analyser_pb2.StorageRequest()
            storage_request.words_by_frequency.update(words_by_frequency)
            storage_request.average_word_length = average_word_length
            storage_request.average_sentence_length = average_sentence_length

            try:
                # Make the gRPC call to the Statistics Storage microservice
                storage_response = stub.StoreStatistics(storage_request)
                print("Sending statistics to Statistics Storage microservice.")
            except grpc.RpcError as e:
                # Handle the error response from the server
                if e.code() == grpc.StatusCode.INTERNAL:
                    print(f"Error storing statistics: {e.details()}")
                else:
                    # Handle other types of errors, if needed
                    print("An error occurred.")

        return response

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    text_analyser_pb2_grpc.add_TextAnalyserServiceServicer_to_server(TextAnalyserServicer(), server)
    server.add_insecure_port('[::]:50001')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    start_http_server(8000)
    serve()