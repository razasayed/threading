import random
import concurrent.futures
import time
import threading
import queue

#Producer Consumer pipeline refactored using Queue

class Pipeline(queue.Queue):
    def __init__(self):
        super().__init__(maxsize=20)

    def put_message(self, message):
        print(f'producing message: {message}')
        producer_pipeline.append(message)
        self.put(message)

    def get_message(self):
        message = self.get()
        print(f'consuming message: {message}')
        consumer_pipeline.append(message)
        return message


def producer(pipeline, event):
    while not event.is_set():
        message = random.randint(1, 100)
        pipeline.put_message(message)

def consumer(pipeline, event):
    while not pipeline.empty() or not event.is_set():
        print(f'queue size is {pipeline.qsize()}')
        message = pipeline.get_message()
        time.sleep(random.random())


producer_pipeline = []
consumer_pipeline = []

if __name__ == '__main__':
    pipeline = Pipeline()
    event = threading.Event()
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
        ex.submit(producer, pipeline, event)
        ex.submit(consumer, pipeline, event)
        time.sleep(0.5)
        event.set()
    print(f'producer pipeline: {producer_pipeline}')
    print(f'consumer pipeline: {consumer_pipeline}')