"""This file."""
import math
from django.db import models

# Create your models here.
class Ubike(models.Model):
    """This class is the struct of ubike data."""
    sno = models.IntegerField(primary_key=True)
    lng = models.FloatField()
    lat = models.FloatField()
    sbi = models.IntegerField()
    sna = models.TextField()
    snaen = models.TextField()
    bemp = models.IntegerField()
    act = models.TextField()
    created = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "ubike"

class UbikeDistance(models.Model):
    """This class is the struct of ubike distance."""
    sno = models.IntegerField(primary_key=True)
    distance = models.FloatField()

    class Meta:
        db_table = "ubikedistance"

def get_distance(lat, lng, lat2, lng2) -> float:
    """This get two point distance"""
    radius = 6371 # km

    dlat = math.radians(lat2-lat)
    dlon = math.radians(lng2-lng)
    a_val = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c_val = 2 * math.atan2(math.sqrt(a_val), math.sqrt(1-a_val))
    return radius * c_val
