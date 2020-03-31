from queue import Queue
from threading import Thread
import random

from unittest.mock import patch

class MockException(Exception):
    pass

class Time:
    def sleep(self, n):
        raise MockException

time = Time()


url_queue = Queue()
scraped_queue = Queue()
cleaned_queue = Queue()
deduplicated_queue = Queue()

def scraper():
    while True:
        time.sleep(random.randrange(0,2))
        url = url_queue.get()
        print("Scraping {}".format(url))
        scraped_queue.put(url[3:])

def cleaner():
    while True:
        time.sleep(random.randrange(2,4))
        raw = scraped_queue.get()
        print("Cleaning {}".format(raw))
        cleaned_queue.put(raw.replace("-", ""))

def deduplicator():
     while True:
        time.sleep(random.randrange(4,6))
        cleaned = cleaned_queue.get()
        print("Deduplicating {}".format(cleaned))
        if cleaned not in seen:
            deduplicated_queue.put(cleaned)
            seen.add(cleaned)


def test_scraper():
    try:
        scraper()
    except Exception as e:
        assert type(e) == MockException

def test_cleaner():
    try:
        cleaner()
    except Exception as e:
        assert type(e) == MockException

def test_deduplicator():
    try:
        deduplicator()
    except Exception as e:
        assert type(e) == MockException




