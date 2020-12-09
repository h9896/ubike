"""This file."""
import json
#from django.shortcuts import render
from django.http import HttpResponse
from determine_boundary.boundary import BoundaryTaipei

boundary_tool = BoundaryTaipei()
def is_in_boundary(request) -> HttpResponse:
    """To find the location is in Taipei"""
    if request.method == "GET":
        lat = float(request.GET.get('lat', default='25.105497'))
        lng = float(request.GET.get('lng', default='121.597366'))
        return HttpResponse(boundary_tool.isPoiWithinPoly((lng, lat)), status=200)
    elif request.method == "POST":
        req = json.loads(request.body)
        if "lat" in req and "lng" in req:
            lat = float(req["lat"])
            lng = float(req["lng"])
            return HttpResponse(boundary_tool.isPoiWithinPoly((lng, lat)), status=200)
        return HttpResponse("Can't find lat or lng in the request body", status=406)
    else:
        return HttpResponse("Should use the GET or POST method.", status=405)
