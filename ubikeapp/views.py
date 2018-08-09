# Create your views here.
from ubikeapp.models import Ubike
from ubikeapp.serializers import UbikeSerializer

from rest_framework import viewsets


# Create your views here.
class UbikeViewSet(viewsets.ModelViewSet):
    queryset = Ubike.objects.all()
    serializer_class = UbikeSerializer