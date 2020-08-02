from django.db import models


class Movie(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Comment(models.Model):
    movie = models.ForeignKey(
        "Movie", related_name="comments", on_delete=models.CASCADE
    )
    content = models.TextField()
    rating = models.IntegerField()
    timestamp = models.DateTimeField()
    author = models.CharField(max_length=20)
