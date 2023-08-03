# statistics_storage.py
import grpc
from concurrent import futures
import redis
import logging
import text_analyser_pb2
import text_analyser_pb2_grpc

# Connect to the Redis server
redis_client = redis.StrictRedis(host='redis', port=6379, db=0)

def store_statistics_in_redis(statistics):
    try:
        # Convert all keys to lowercase before storing in Redis
        words_by_frequency_lowercase = {word.lower(): frequency for word, frequency in statistics['words_by_frequency'].items()}

        # Log the statistics data before storing
        print("Statistics to be stored in Redis:")
        print("Words by frequency:", words_by_frequency_lowercase)
        print("Average word length:", statistics['average_word_length'])
        print("Average sentence length:", statistics['average_sentence_length'])

        # Clear the Redis database
        redis_client.flushdb()

        # Store word frequencies in Redis using the word as the key and the frequency as the value
        for word, frequency in words_by_frequency_lowercase.items():
            redis_client.set(word, frequency)

        # Store average word length in Redis
        redis_client.set('average_word_length', float(statistics['average_word_length']))

        # Store average sentence length in Redis
        redis_client.set('average_sentence_length', float(statistics['average_sentence_length']))

        print("Data in Redis:")
        for key in redis_client.keys('*'):
            print(key, redis_client.get(key))

        print("Statistics stored in Redis successfully.")

    except redis.RedisError as e:
        logging.error(f"Error storing statistics in Redis: {e}")
        context = grpc.StatusCode.INTERNAL, "Error storing statistics in Redis."
        raise grpc.RpcError(grpc.StatusCode.INTERNAL, str(e), details=context.details)

    except Exception as ex:
        logging.error(f"Error in store_statistics_in_redis: {ex}")
        context = grpc.StatusCode.INTERNAL, "Error in store_statistics_in_redis."
        raise grpc.RpcError(grpc.StatusCode.INTERNAL, str(ex), details=context.details)


class StatisticsStorageServicer(text_analyser_pb2_grpc.StatisticsStorageServiceServicer):
    def StoreStatistics(self, request, context):
        statistics = {
            'words_by_frequency': dict(request.words_by_frequency),
            'average_word_length': request.average_word_length,
            'average_sentence_length': request.average_sentence_length,
        }
        store_statistics_in_redis(statistics)

        return text_analyser_pb2.StorageResponse(message="Statistics stored successfully.")
    
    def GetStatistics(self, request, context):
        try:
            # Fetch stored statistics from Redis
            words_by_frequency = {
                word.decode(): int(float(redis_client.get(word))) for word in redis_client.keys('*') if not word.startswith(b'average_')
            }

            # Convert the values for average_word_length and average_sentence_length to floats
            average_word_length = float(redis_client.get('average_word_length') or 0)  # Use 0 as default if not found
            average_sentence_length = float(redis_client.get('average_sentence_length') or 0)

            # Create and return the response
            response = text_analyser_pb2.GetStatisticsResponse(
                words_by_frequency=words_by_frequency,
                average_word_length=average_word_length,
                average_sentence_length=average_sentence_length)

            return response

        except redis.RedisError as e:
            logging.error(f"Error fetching statistics from Redis: {e}")
            context.set_details("Error fetching statistics from Redis.")
            context.set_code(grpc.StatusCode.INTERNAL)
            return text_analyser_pb2.GetStatisticsResponse()

        except Exception as ex:
            logging.exception("Error in GetStatistics:")
            context.set_details("Error in GetStatistics.")
            context.set_code(grpc.StatusCode.INTERNAL)
            return text_analyser_pb2.GetStatisticsResponse()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    text_analyser_pb2_grpc.add_StatisticsStorageServiceServicer_to_server(StatisticsStorageServicer(), server)
    server.add_insecure_port('[::]:50002')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()