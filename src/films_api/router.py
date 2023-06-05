from rest_framework import routers

from .views import FilmViewSet

app_name = "films"

router = routers.DefaultRouter()
router.register("films", FilmViewSet)