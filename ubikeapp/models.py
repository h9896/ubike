from django.db import models

# Create your models here.
class Ubike(models.Model):
    lng = models.FloatField()
    lat = models.FloatField()
    sbi = models.IntegerField()
    sna = models.TextField()
    snaen = models.TextField()
    bemp = models.IntegerField()
    act = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "ubike"