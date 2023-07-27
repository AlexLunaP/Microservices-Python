# text_reader.py
import grpc
import text_analyser_pb2
import text_analyser_pb2_grpc

def analyse_text(text):
    channel = grpc.insecure_channel('localhost:50001')
    stub = text_analyser_pb2_grpc.TextAnalyserServiceStub(channel)

    request = text_analyser_pb2.AnalysisRequest(text="".join(text))
    
    response = stub.AnalyseText(request)

    return response

def read_and_analyse_file(file_path):
    with open(file_path, "r") as file:
        text = file.readlines()
        response = analyse_text(text)

    print("Analysis Result:\n")
    print("Average word length:", response.average_word_length)
    print("Average sentence length:", response.average_sentence_length, "\n")
    print("Word Frequency:")
    for word, freq in response.words_by_frequency.items():
        print(f"Word: {word}, Frequency: {freq}")

if __name__ == '__main__':
    read_and_analyse_file('Boris.txt')