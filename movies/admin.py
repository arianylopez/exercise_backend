from django.contrib import admin
from .models import Genre, FilmWork, Person, GenreFilmWork, PersonFilmWork

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass

@admin.register(FilmWork)
class FilmWorkAdmin(admin.ModelAdmin):
    class GenreFilmWorkInline(admin.TabularInline):
        model = GenreFilmWork

    class PersonFilmWorkInline(admin.TabularInline):
        model = PersonFilmWork

    inlines = (GenreFilmWorkInline,)
    list_display = ('title', 'type', 'creation_date', 'rating', 'created', 'modified')
    list_filter = ('type',)
    search_fields = ('title', 'description', 'id')

@admin.register(Person)
class Person(admin.ModelAdmin):
    pass