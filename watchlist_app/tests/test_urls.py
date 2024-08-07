from django.test import SimpleTestCase
from django.urls import reverse, resolve
from watchlist_app.api.views import MovieList, MovieDetail

class TestUrls(SimpleTestCase):

    def test_list_url_is_resolved(self):
        url = reverse('movie-list')
        self.assertEqual(resolve(url).func.view_class, MovieList)

    def test_detail_url_is_resolved(self):
        url = reverse('movie-detail', args=[1])
        self.assertEqual(resolve(url).func.view_class, MovieDetail)
