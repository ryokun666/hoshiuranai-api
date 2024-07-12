import unittest
from app.utils import get_zodiac

class TestUtils(unittest.TestCase):

    def test_get_zodiac(self):
        zodiac = get_zodiac("20200401")
        self.assertEqual(zodiac['name'], '牡羊座')

if __name__ == '__main__':
    unittest.main()
