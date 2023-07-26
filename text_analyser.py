# text_analyser.py
import grpc
from concurrent import futures
import string
import re
import text_analyser_pb2
import text_analyser_pb2_grpc

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
                print (word)
                if word in words_by_frequency:
                    words_by_frequency[word] += 1
                else:
                    words_by_frequency[word] = 1

    average_word_length = total_words_length / total_words
    average_sentence_length = total_words / total_sentences

    return words_by_frequency, average_word_length, average_sentence_length

class TextAnalyserServicer(text_analyser_pb2_grpc.TextAnalyserServiceServicer):
    def AnalyseText(self, request, context):
        text = request.text.splitlines()
        words_by_frequency, average_word_length, average_sentence_length = calculate_statistics(text)

        response = text_analyser_pb2.AnalysisResponse(
            words_by_frequency=words_by_frequency,
            average_word_length=average_word_length,
            average_sentence_length=average_sentence_length
        )

        return response

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    text_analyser_pb2_grpc.add_TextAnalyserServiceServicer_to_server(TextAnalyserServicer(), server)
    server.add_insecure_port('[::]:50001')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()