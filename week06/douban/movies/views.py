from django.shortcuts import render, get_object_or_404
from movies.models import Movie, Comment


def index(request):
    movies = Movie.objects.all()
    return render(request, "movies/index.html", {"movies": movies})


def movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    term = request.GET.get("term", None)
    comments = Comment.objects.filter(movie=movie, rating__gt=3).all()
    if term:
        comments = comments.filter(content__icontains=term)
    return render(request, "movies/detail.html", {"movie": movie, "comments": comments})
