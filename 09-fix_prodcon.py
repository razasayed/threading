import random
import concurrent.futures
import time
import threading

#Producer Consumer pipeline fixed using locks

FINISH = 'THE END'

class Pipeline:
    def __init__(self, capacity):
        self.capacity = capacity
        self.message = None #Shared data
        self.producer_lock = threading.Lock()
        self.consumer_lock = threading.Lock()
        self.consumer_lock.acquire()

    def put_message(self, message):
        print(f'producing message: {message}')
        producer_pipeline.append(message)
        self.producer_lock.acquire()
        self.message = message
        self.consumer_lock.release()

    def get_message(self):
        print(f'consuming message: {self.message}')
        self.consumer_lock.acquire()
        message = self.message
        self.producer_lock.release()
        consumer_pipeline.append(message)
        return message


def producer(pipeline):
    for _ in range(pipeline.capacity):
        message = random.randint(1, 100)
        pipeline.put_message(message)
    pipeline.put_message(FINISH)

def consumer(pipeline):
    message = None
    while message is not FINISH:
        message = pipeline.get_message()
        if message is not FINISH:
            time.sleep(random.random())


producer_pipeline = []
consumer_pipeline = []

if __name__ == '__main__':
    pipeline = Pipeline(10)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
        ex.submit(producer, pipeline)
        ex.submit(consumer, pipeline)
    print(f'producer pipeline: {producer_pipeline}')
    print(f'consumer pipeline: {consumer_pipeline}')