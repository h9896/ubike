import requests
import time
import json
url = "http://127.0.0.1:8000/api/ubike"
youbike_api = 'http://data.taipei/youbike'
def load_data(url, youbike_api):
    response = requests.get(youbike_api)
    data = response.json()
    youbike={}
    if data['retCode'] == 1:
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
            youbike[int(value['sno'])] = {'lng' : longitude, 'lat' : latitude,
                                     'sbi' : num_ubike, 'sna' : station,
                                     'snaen' : station_en, 'bemp' : num_vacancies,
                                     'act' : state}
    if youbike:
        for key in youbike.keys():
            tmp_response = requests.get(url+"/{}/".format(key))
            if tmp_response.ok:
                tmp_data = {'sbi': youbike[key]['sbi'], 'bemp': youbike[key]['bemp'], 'act': youbike[key]['act']}
                requests.patch(url+"/{}/".format(key), data = tmp_data)
            else:
                tmp_data = youbike[key]
                tmp_data['id'] = key
                requests.post(url+'/', data = tmp_data)
    return True
if __name__ == "__main__":
    while True:
        load_data(url, youbike_api)
        print('OK!')
        time.sleep(10)