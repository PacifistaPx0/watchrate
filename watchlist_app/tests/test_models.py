from django.test import TestCase
from watchlist_app.models import Watchlist

class MovieModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a movie object for use in all test methods
        Watchlist.objects.create(title="Inception",
                                 genre="Action", 
                                 description="A thief who steals corporate secrets through the use of dream-sharing technology.", 
                                 active=True)

    def test_movie_content(self):
        movie = Watchlist.objects.get(id=1)
        expected_object_name = f'{movie.title}'
        self.assertEqual(expected_object_name, 'Inception')
        self.assertTrue(movie.active)
