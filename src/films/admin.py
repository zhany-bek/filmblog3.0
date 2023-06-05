from django.contrib import admin
from .models import Film

# Register your models here.
class FilmAdmin(admin.ModelAdmin):
    list_display = ('title_and_year', 'director_name', 'rating')

    def title_and_year(self, obj):
        return f"{obj.title}_{obj.release_year}"

admin.site.register(Film, FilmAdmin)