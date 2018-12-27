# IMPORT LIBRARIES

import os
import glob
import time
from datetime import date
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
import pytemperature
import nest
import sys

## GOOGLE DOCS

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('TemperatureSensing-dddd25843f51.json', scope)

gc = gspread.authorize(credentials)

wks = gc.open("temperature_sensor_data").sheet1

## WEATHER API

url = 'http://api.openweathermap.org/data/2.5/weather?appid=fa93b1d5eecaaa79b67d8fd82f371852&lat=51.536876&lon=-0.219663'

json_data = requests.get(url).json()

weather = json_data['weather'][0]['description']

outside_temp_Kelvin = json_data['main']['temp']
outside_temp = pytemperature.k2c(outside_temp_Kelvin)

## TIMESTAMP

day = str(date.today())
time = str(time.strftime("%H:%M:%S"))

## SENSOR

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines


def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()

    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

## NEST API

client_id = '568ff0a1-fb02-47f6-849b-28f4131c3399'
client_secret = 'tApMhBPwJvf89O8YVG2rloG9r'
access_token_cache_file = 'nest.json'

napi = nest.Nest(client_id=client_id, client_secret=client_secret, access_token_cache_file=access_token_cache_file)

if napi.authorization_required:
    if sys.version_info[0] < 3:
        pin = 'RWB8SNPC'
    else:
        pin = 'RWB8SNPC'

for structure in napi.structures:
    for device in structure.thermostats:
        nest_temp = device.temperature
        nest_target = device.target
        nest_humidity = device.humidity
        nest_eco = device.has_leaf
        nest_time2target = device.time_to_target

## OUTPUT

while True:
    wks.append_row([day, time, read_temp(), outside_temp, weather, nest_temp, n$
    break


