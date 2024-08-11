from rest_framework.test import APITestCase
from rest_framework import status
from watchlist_app.models import Watchlist
from django.urls import reverse

class MovieAPITest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a movie for testing
        Watchlist.objects.create(title="Inception", 
                                 genre="Action",
                                 description="Dream-sharing technology.", 
                                 active=True)

    def test_get_all_movies(self):
        # Get API response
        response = self.client.get(reverse('movie-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_valid_single_movie(self):
        response = self.client.get(reverse('movie-detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Inception')

    def test_get_invalid_single_movie(self):
        response = self.client.get(reverse('movie-detail', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_valid_movie(self):
        data = {"title": "New Movie", "genre": "Action", "description": "About tests", "active": True}
        response = self.client.post(reverse('movie-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_put_valid_movie(self):
        data = {"title": "Inception Updated", "genre": "Action", "description": "Updated description", "active": False}
        response = self.client.put(reverse('movie-detail', kwargs={'pk': 1}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_movie(self):
        response = self.client.delete(reverse('movie-detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
