from django.db import models


# Create your models here.
class Comment(models.Model):
    id = models.BigAutoField(primary_key=True)
    rating = models.IntegerField()
    content = models.CharField(max_length=400)
    date = models.DateField()

    def __str__(self):
        return self.content
