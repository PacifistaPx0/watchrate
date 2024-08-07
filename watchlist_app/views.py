# from django.shortcuts import get_object_or_404, render
# from watchlist_app.models import Movie
# from django.http import JsonResponse

# # Create your views here.
# def movie_list(request):
#     movies = Movie.objects.all()
#     data = {
#         'movies': list(movies.values())
#     }
#     return JsonResponse(data)

# def movie_detail(request, pk):
#     movie = get_object_or_404(Movie, pk=pk)
#     data = {
#         'id': movie.id,
#         'name': movie.name,
#         'description': movie.description,
#     }
#     return JsonResponse(data)