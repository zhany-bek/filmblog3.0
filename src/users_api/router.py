from rest_framework import routers

from .views import UserViewSet

app_name = "users"

router = routers.DefaultRouter()
router.register("users", UserViewSet)