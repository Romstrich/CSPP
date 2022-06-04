import unittest
from client import create_presence
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME
import  time

print('import unittest')


def somesum(a, b):
    return a + b


class TestFirstTest(unittest.TestCase):
    def test_Equal(self):
        self.assertEqual(somesum(2, 5), 7)

    def test_NoEqual(self):
        self.assertNotEqual(somesum(2, 5), 6)

    def test_create_presence1(self):
        self.assertEqual(create_presence(), {ACTION: PRESENCE, TIME: time.time()
            , USER: {ACCOUNT_NAME: 'Guest', }})#разница во времени-FAILED

    def test_create_presence(self):
        s_msage=create_presence()
        time_now=s_msage[TIME]
        self.assertEqual(s_msage, {ACTION: PRESENCE, TIME:time_now , USER: {ACCOUNT_NAME: 'Guest', }})

    
if __name__ == '__main__':
    unittest.main()
