from django.contrib import admin
from movies.models import Movie, Comment


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0


class MovieAdmin(admin.ModelAdmin):
    list_display = ["name"]
    inlines = [CommentInline]


admin.site.register(Movie, MovieAdmin)
