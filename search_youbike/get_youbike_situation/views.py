"""This file."""
import json
from django.http import HttpResponse
from determine_boundary.boundary import BoundaryTaipei
from update_ubike.models import Ubike, UbikeDistance, get_distance
from update_ubike.update import AVG_LAT, AVG_LNG
# Create your views here.
boundary_tool = BoundaryTaipei()

def get_youbike_info(request) -> HttpResponse:
    """To find the location is in Taipei"""
    if request.method == "GET":
        lat = float(request.GET.get('lat', default='25.1055'))
        lng = float(request.GET.get('lng', default='121.5'))
        if boundary_tool.isPoiWithinPoly((lng, lat)):
            result = {}
            dis = get_distance(lat, lng, AVG_LAT['lat__avg'], AVG_LNG['lng__avg'])+2
            maybe = UbikeDistance.objects.filter(distance__lte=dis)
            for sno in maybe:
                data = Ubike.objects.get(sno=sno.sno)
                new_dis = get_distance(lat, lng, data.lat, data.lng)
                first = 3
                second = 3
                if new_dis <= 2:
                    if data.act == "1" and new_dis < second:
                        if new_dis < first:
                            first = new_dis
                            if "1" in result:
                                result["2"] = result["1"]
                                second = result["2"]["Distance (km)"]
                            result["1"] = {"No": data.sno, "Station": data.sna,\
                                    "Number can borrow": data.sbi, "Number can return": data.bemp,\
                                    "Longitude": data.lng, "Latitude": data.lat,\
                                    "Distance (km)": new_dis}
                        else:
                            second = new_dis
                            result["2"] = {"No": data.sno, "Station": data.sna,\
                                    "Number can borrow": data.sbi, "Number can return": data.bemp,\
                                    "Longitude": data.lng, "Latitude": data.lat,\
                                    "Distance (km)": new_dis}
            if result:
                http_result = {"code": "0", "data":[result["1"], result["2"]]}
                return HttpResponse(json.dumps(http_result, ensure_ascii=False), status=200)
            http_result = {"code": "1", \
                    "error_message": "There is no available station in 2 km."}
            return HttpResponse(json.dumps(http_result, ensure_ascii=False), status=200)
        http_result = {"code": "2", "error_message": "The location is not in Taipei city."}
        return HttpResponse(json.dumps(http_result, ensure_ascii=False), status=200)
    return HttpResponse("Should use the GET method.", status=405)
