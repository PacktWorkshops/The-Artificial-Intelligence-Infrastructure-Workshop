from unittest import TestCase
from api import app


class TestAPI(TestCase):

    def test_api(self):
        app.run()
