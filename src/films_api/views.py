from rest_framework import viewsets, permissions
from films.models import Film
from .serializers import FilmSerializer

class FilmViewSet(viewsets.ModelViewSet):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer
    permission_classes = [permissions.IsAuthenticated]
