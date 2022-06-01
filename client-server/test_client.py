import unittest

print('import umittest')
def somesum(a,b):
    return a+b

class TestFirstTest(unittest.TestCase):
    def testequal(self):
        self.assertEqual(somesum(2,5),7)

if __name__=='__main__':
    unittest.main()