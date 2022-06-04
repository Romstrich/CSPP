import unittest
from client import create_presence,process_ans
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR
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
        self.assertNotEqual(create_presence(), {ACTION: PRESENCE, TIME: time.time()
            , USER: {ACCOUNT_NAME: 'Guest', }})#разница во времени-FAILED

    def test_create_presence(self):
        s_msage=create_presence()
        time_now=s_msage[TIME]
        self.assertEqual(s_msage, {ACTION: PRESENCE, TIME:time_now , USER: {ACCOUNT_NAME: 'Guest', }})

    def test_answer200(self):
        self.assertEqual(process_ans({RESPONSE:200}),{RESPONSE:200})

    def test_answer400(self):
        self.assertEqual(process_ans( {RESPONSE:400,ERROR:'Request for lesson 3 is not correct'}),
                         {RESPONSE:400,ERROR:'Request for lesson 3 is not correct'})

if __name__ == '__main__':
    unittest.main()
