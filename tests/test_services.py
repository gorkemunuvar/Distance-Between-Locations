import unittest
import services
from services.geocoding import get_coordinate
from services.point_polygon import in_polygon
from services.distance import calculate_distance, calculate_distance_gh

# RUNING TEST
# python -m unittest tests.test_services -v


class ServicesTestCase(unittest.TestCase):
    # Ensure that geocoding functionality works
    def test_get_coordinate(self):
        coordinate1 = get_coordinate('İstanbul')
        coordinate2 = get_coordinate('lsafdj')    # invalid input
        coordinate3 = get_coordinate('new york')
        coordinate4 = get_coordinate('12321312')  # invalid input
        coordinate5 = get_coordinate('')          # invalid input

        self.assertEqual(coordinate1, {'lat': 41.011218, 'lon': 28.978178})
        self.assertEqual(coordinate2, None)
        self.assertEqual(coordinate3, {'lat': 40.714606, 'lon': -74.0028})
        self.assertEqual(coordinate4, None)
        self.assertEqual(coordinate5, None)

    # Ensure that in_polygon func. works as expected
    def test_in_polygon(self):
        result1 = in_polygon(55.869046, 37.489491)  # Khovrino District
        result2 = in_polygon(55.804552, 37.670636)  # Sokolniki Park
        result3 = in_polygon(58.564392, 25.660798)  # Estonia
        result4 = in_polygon(-91.11111, 32.854049)  # Nowhere (Edge case)
        result5 = in_polygon(95.545858, -181.5444)  # Nowhere (Corner case)

        self.assertEqual(result1, True)
        self.assertEqual(result2, True)
        self.assertEqual(result3, False)
        self.assertEqual(result4, None)
        self.assertEqual(result5, None)

    # Ensure that OSRM API calculate distance func. works as we want
    def test_calculate_distance(self):
        slon = 37.3903193
        slat = 55.8142861

        distance1 = calculate_distance(slon, slat, 13.375142, 52.518621)
        distance2 = calculate_distance(slon, slat, 5.83843, 52.848781)
        distance3 = calculate_distance(slon, slat, 30.315877, 59.939099)

        self.assertEqual(distance1, 1817184.1)  # to Berlin
        self.assertEqual(distance2, 2410495.4)  # to Netherlands
        self.assertEqual(distance3, 697243.2)   # to St. Petersburg

    # Ensure that GRAPHHOPPER API calculate distance func. works as we want
    def test_calculate_distance_gh(self):
        slon = 37.3903193  # source longitude
        slat = 55.8142861  # source latitude

        distance1 = calculate_distance_gh(slon, slat, 13.375142, 52.518621)
        distance2 = calculate_distance_gh(slon, slat, 5.83843, 52.848781)
        distance3 = calculate_distance_gh(slon, slat, 30.315877, 59.939099)

        self.assertEqual(distance1, 1816858.066)  # to Berlin
        self.assertEqual(distance2, 2406151.711)  # to Netherlands
        self.assertEqual(distance3, 696927.77)    # to St. Petersburg


if __name__ == '__main__':
    unittest.main()
