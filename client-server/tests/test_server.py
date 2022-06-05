import sys
sys.path.append('..')

import unittest

from client import *
from server import *


TEST_MESSAGE_200=create_presence()
TEST_MESSAGE_400={'some_message':'some_message'}


class TestServer(unittest.TestCase):
    def test_200(self):
        self.assertEqual(process_client_message(TEST_MESSAGE_200),{RESPONSE:200})

class TestServer(unittest.TestCase):
    def test_200(self):
        self.assertEqual(process_client_message(TEST_MESSAGE_400),{RESPONSE:400,ERROR:'Request for lesson 3 is not correct'})