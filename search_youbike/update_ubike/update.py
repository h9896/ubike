"""This file is for updating db."""
import time
import requests
from django.db import models
from apscheduler.schedulers.background import BackgroundScheduler
from update_ubike.models import Ubike, UbikeDistance, get_distance

YOUBIKE_URL = "https://tcgbusfs.blob.core.windows.net/blobyoubike/YouBikeTP.json"
AVG_LAT = {'lat__avg':0}
AVG_LNG = {'lng__avg':0}
FIRST = True

def update_db_job():
    """This function is used to update ubike data."""
    print("Start update DB at {}".format(time.strftime("%Y-%m-%d %H:%M:%S",
                                        time.localtime(time.time()))))
    response = requests.get(YOUBIKE_URL)
    data = response.json()
    if data['retCode'] == 1:
        for _, value in data['retVal'].items():
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
            if Ubike.objects.filter(sno=value['sno']).exists():
                db_data = Ubike.objects.filter(sno=value['sno'])
                db_data.update(lng=longitude, lat=latitude, sbi=num_ubike,
                                sna=station, snaen=station_en,
                                bemp=num_vacancies, act=state)
            else:
                Ubike.objects.create(sno=value['sno'], lng=longitude,
                                    lat=latitude, sbi=num_ubike, sna=station,
                                    snaen=station_en, bemp=num_vacancies, act=state)
                if not FIRST:
                    new_dis = get_distance(latitude, longitude, \
                        AVG_LAT['lat__avg'], AVG_LNG['lng__avg'])
                    UbikeDistance.objects.create(sno=value['sno'],distance=new_dis)
        print("Finish update DB at {}".format(time.strftime('%Y-%m-%d %H:%M:%S',
                                            time.localtime(time.time()))))
        if FIRST:
            change_avg_lat()
            change_avg_lng()
            for ubike in Ubike.objects.all():
                dis = get_distance(ubike.lat, ubike.lng, AVG_LAT['lat__avg'], AVG_LNG['lng__avg'])
                if UbikeDistance.objects.filter(sno=ubike.sno).exists():
                    db_distance = UbikeDistance.objects.filter(sno=ubike.sno)
                    db_distance.update(distance=dis)
                else:
                    UbikeDistance.objects.create(sno=ubike.sno,distance=dis)
            change_first_flag()
            print("Finish update UbikeDistance at {}".format(time.strftime('%Y-%m-%d %H:%M:%S',
                                            time.localtime(time.time()))))

def change_avg_lat():
    '''change global value AVG_LAT'''
    global AVG_LAT
    AVG_LAT = Ubike.objects.aggregate(models.Avg('lat'))
def change_avg_lng():
    '''change global value AVG_LNG'''
    global AVG_LNG
    AVG_LNG = Ubike.objects.aggregate(models.Avg('lng'))
def change_first_flag():
    '''change global value FIRST'''
    global FIRST
    if FIRST:
        FIRST = False
    else:
        FIRST = True

def start():
    '''start scheduler'''
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_db_job, 'interval', \
        seconds=90, id='update_db_job', replace_existing=True)
    if not scheduler.running:
        scheduler.start()
