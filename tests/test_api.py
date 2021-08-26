import unittest
from app import app


class ApiTestCase(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.tester = app.test_client(self)

    # Ensure that Flask was set up correctly.
    def test_index(self):
        response = self.tester.get('/', content_type='html/text')

        self.assertEqual(response.status_code, 200)

    # Ensure that the home page loads correctly.
    def test_home_page_loading(self):
        response = self.tester.get('/', content_type='html/text')

        self.assertTrue(b'Welcome to Distance Calculator' in response.data)

    # Ensure that addres parameter is missing.
    def test_missing_address_parameter(self):
        response = self.tester.get('/distance/', follow_redirects=True)

        self.assertIn(b'<address> parameter is missing.', response.data)

    # Ensure that we get a messsage when the address is incorrect.
    def test_incorrect_addres_info(self):
        response1 = self.tester.get('/distance/?address=')
        response2 = self.tester.get('/distance/?address=fjasdlfja')
        response3 = self.tester.get('/distance/?address=123213')

        msg = 'Make sure that address information is correct.'

        self.assertIn(bytes(msg, encoding='utf-8'), response1.data)
        self.assertIn(bytes(msg, encoding='utf-8'), response2.data)
        self.assertIn(bytes(msg, encoding='utf-8'), response3.data)

    # Ensure that no need to calc. distance for addressin already in Moscow Ring Road.
    def test_no_need_to_calculate(self):
        response1 = self.tester.get('/distance/?address=Sokolniki Park')
        response2 = self.tester.get('/distance/?address=Khovrino District')

        self.assertIn(b'No need to calculate.', response1.data)
        self.assertIn(b'No need to calculate.', response2.data)

    # Ensure that distance is calculated correctly.
    def test_distance_result(self):
        response1 = self.tester.get('/distance/?address=St. Petersburg')
        response2 = self.tester.get('/distance/?address=Ankara')

        self.assertIn(b'distance', response1.data)
        self.assertIn(b'distance', response2.data)


if __name__ == '__main__':
    unittest.main()
