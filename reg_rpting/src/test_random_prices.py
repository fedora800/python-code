import datetime
import random
import time

STREAM_NAME = "ExampleInputStream"


def get_data():
    return {
        'EVENT_TIME': datetime.datetime.now().isoformat(),
        'TICKER': random.choice(['AAPL', 'AMZN', 'MSFT', 'INTC', 'TBV']),
        'PRICE': round(random.random() * 100, 2)}


def generate_data():
    while True:
        data = get_data()
        print(data)
        time.sleep(2)


if __name__ == '__main__':
    generate_data()
