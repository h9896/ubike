# Create your views here.
from ubikeapp.models import Ubike
from ubikeapp.serializers import UbikeSerializer
import requests
from rest_framework import viewsets


# Create your views here.
class UbikeViewSet(viewsets.ModelViewSet):
    queryset = Ubike.objects.all()
    serializer_class = UbikeSerializer

def ub_load(request):
    youbike_api = 'http://data.taipei/youbike'
    response = requests.get(youbike_api)
    data = response.json()
    if data['retCode'] == 1:
        youbike={}
        for key, value in data['retVal'].items():
            #longitude
            longitude = value['lng']
            #latitude
            latitude = value['lat']
            #numbers of ubike can borrow
            num_ubike = value['sbi']
            #station name
            station = value['sna']
            #station name in English
            station_en = value['snaen']
            #number of ubike can retrun
            num_vacancies = value['bemp']
            #the station state
            state = value['act']
            # station id as key
            youbike[value['sno']] = {'lng' : longitude, 'lat' : latitude,
                                     'sbi' : num_ubike, 'sna' : station,
                                     'snaen' : station_en, 'bemp' : num_vacancies,
                                     'act' : state}
        for sno in youbike:
            tmp = Ubike(id=sno, lng = youbike[sno]['lng'], 
                    lat = youbike[sno]['lat'], 
                    sbi = youbike[sno]['sbi'], 
                    sna = youbike[sno]['sna'], 
                    snaen = youbike[sno]['snaen'], 
                    bemp = youbike[sno]['bemp'], 
                    act = youbike[sno]['act'])
            tmp.save()
            del tmp
        return True
    else:
        return False