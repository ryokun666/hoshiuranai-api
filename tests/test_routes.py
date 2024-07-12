import unittest
from app import app

class TestRoutes(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_horoscope(self):
        response = self.app.get('/?userid=test&date=20240101&birth=0401&resulttype=json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('announce', response.json)

if __name__ == '__main__':
    unittest.main()
