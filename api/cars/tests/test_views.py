from rest_framework.test import APITestCase
from rest_framework import status


def rate_car(client, url, car_id, rating):
    data = {
        'car_id': car_id,
        'rating': rating
    }

    response = client.post(url, data=data)
    return response


class CarViewTestCase(APITestCase):
    """Tests /cars endpoint
    """

    def setUp(self):
        self.url = '/cars/'
        self.data = {
            'make': 'Honda',
            'model': 'Civic',
        }

    def test_create_valid_car(self):
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_car(self):
        data = {
            'make': 'Honda',
            'model': 'NotCivic',
        }

        response = self.client.post(self.url, data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_car(self):
        response = self.client.post(self.url, data=self.data)
        car_id = response.data['id']

        response = self.client.delete(self.url + f'{car_id}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_avg_rating_key_exists(self):
        response = self.client.post(self.url, data=self.data)

        self.assertIn('avg_rating', response.data)

    def test_if_avg_rating_is_none_without_any_ratings(self):
        response = self.client.post(self.url, data=self.data)
        rating = response.data['avg_rating']

        self.assertIsNone(rating)


class CreateRatingViewTestCase(APITestCase):
    """Tests /rate endpoint
    """

    def setUp(self):
        self.rate_url = '/rate/'
        self.cars_url = '/cars/'
        self.car_data = {
            'make': 'Honda',
            'model': 'Civic',
        }

    def test_rate_a_car(self):
        response = self.client.post(self.cars_url, data=self.car_data)
        car_id = response.data['id']

        response = rate_car(self.client, self.rate_url, car_id, rating=4)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_avg_rating(self):
        response = self.client.post(self.cars_url, data=self.car_data)
        car_id = response.data['id']

        ratings = list(range(1, 6))

        for rate in ratings:
            rate_car(self.client, self.rate_url, car_id, rate)

        response = self.client.get(self.cars_url + f'{car_id}/')

        self.assertEqual(sum(ratings) / len(ratings), response.data['avg_rating'])

    def test_rate_above_5(self):
        response = self.client.post(self.cars_url, data=self.car_data)
        car_id = response.data['id']
        response = rate_car(self.client, self.rate_url, car_id, rating=6)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_rate_below_1(self):
        response = self.client.post(self.cars_url, data=self.car_data)
        car_id = response.data['id']
        response = rate_car(self.client, self.rate_url, car_id, rating=0)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_rate_for_non_existing_car(self):
        response = rate_car(self.client, self.rate_url, car_id=100, rating=4)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PopularViewTestCase(APITestCase):
    """Tests /popular endpoint
    """

    def setUp(self):
        self.rate_url = '/rate/'
        self.popular_url = '/popular/'
        self.cars_url = '/cars/'
        self.car_data = {
            'make': 'Honda',
            'model': 'Civic',
        }

    def test_response_have_rates_number_key(self):
        self.client.post(self.cars_url, data=self.car_data)
        response = self.client.get(self.popular_url)

        self.assertIn('rates_number', response.data[0])

    def test_popular_ordering(self):
        cars = [
            {
                'make': 'Ford',
                'model': 'Mustang',
            },
            {
                'make': 'Audi',
                'model': 'A4',
            },
            {
                'make': 'Honda',
                'model': 'Civic',
            },
        ]
        n_rates = [3, 5, 10]

        for item in zip(cars, n_rates):
            response = self.client.post(self.cars_url, data=item[0])
            car_id = response.data['id']
            for i in range(item[1]):
                rate_car(self.client, self.rate_url, car_id, rating=3)
            
        response = self.client.get(self.popular_url)
        results = response.data

        self.assertEqual([x['rates_number'] for x in results], list(reversed(n_rates)))
        self.assertEqual([x['model'] for x in results], list(reversed([x['model'] for x in cars])))
