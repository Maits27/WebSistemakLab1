import signal
import sys
import urllib.parse
import csv
import urllib.parse
import psutil
import requests
import urllib.parse
import json
import time
from pathlib import Path
USER_API_KEY = "NKS6F9SMZR4FI5Y7"
CHANNEL_ID = 0
WRITE_API_KEY = ""

# DOKUMENTAZIOA: https://es.mathworks.com/help/thingspeak/rest-api.html
# Egilea: Maitane Urruela
# Data: 27/02/2023
# Irakasgaia: Web Sistemak (3. maila)

def create_channel():
    metodoa = 'GET'
    uria = "https://api.thingspeak.com/channels.json"
    goiburuak = {'Host': 'api.thingspeak.com'}
    edukia =''
    parametros={'api_key': USER_API_KEY}

    erantzuna = requests.request(metodoa, uria, headers=goiburuak, params=parametros,
                                 data=edukia, allow_redirects=False)

    # JSON PARSEATU
    badago = False

    apikey_file = Path('ApiKey.txt')
    if apikey_file.is_file():
        with open(apikey_file, 'r', encoding='utf8') as file:
            channelId = int(file.readline())

        banatua = json.loads(erantzuna.content)
        for i in range(banatua.__len__()):
            if banatua[i]['id'] == int(channelId):
                badago = True


    if(badago):
        print("Jada existitzen da kanala")
    else:
        print(erantzuna.status_code)
        print(erantzuna.content)
        metodoa = 'POST'
        uria = "https://api.thingspeak.com/channels.json"
        goiburuak = {'Host': 'api.thingspeak.com',
                     'Content-Type': 'application/x-www-form-urlencoded'}
        edukia = {'api_key': USER_API_KEY,
                  'name': 'Nire kanala', 'field1': "%CPU", 'field2': "%RAM"}
        edukia_encoded = urllib.parse.urlencode(edukia)
        goiburuak['Content-Length'] = str(len(edukia_encoded))

        erantzuna = requests.request(metodoa, uria, headers=goiburuak,
                                     data=edukia_encoded, allow_redirects=False)
        kodea = erantzuna.status_code
        deskribapena = erantzuna.reason
        print(str(kodea) + " " + deskribapena)
        edukia = erantzuna.content
        print(edukia)
        if kodea == 402 :
            print("Kanal kopuru maximoa gainditu egin duzu. Ordaintzea beharrezkoa da gehiago sortu nahi izatekotan")
        else:
            # JSON PARSEATU
            banatua = json.loads(edukia)
            id = banatua['id']
            key = ""
            for api in banatua['api_keys']:
                if api['write_flag'] == True:
                    key = api['api_key']

            with open('ApiKey.txt', 'w', encoding='utf8') as f:
                f.write(str(id) + "\n")
                f.write(key)

def update_channel():
    time.sleep(2)
    print("ADI!!!!!!!!!!!!!!!!!!!!!!")
    print("CTRL-C sakatu eguneraketa eteteko eta datuak gordetzeko.")
    time.sleep(2)
    while True:
        #KODEA: psutil liburutegia erabiliz, %CPU eta %RAM atera
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory().percent

        metodoa = 'POST'
        uria = "https://api.thingspeak.com/update.json"
        goiburuak = {'Host': 'api.thingspeak.com',
                     'Content-Type': 'application/x-www-form-urlencoded'}
        edukia = {'api_key': WRITE_API_KEY, 'name': 'Nire kanala',
                  "field1": cpu, "field2": ram}
        edukia_encoded = urllib.parse.urlencode(edukia)
        goiburuak['Content-Length'] = str(len(edukia_encoded))

        erantzuna = requests.request(metodoa, uria, headers=goiburuak,
                                     data=edukia_encoded, allow_redirects=False)
        print("Aktualizazioa burutzean: "+str(erantzuna.status_code)+" "+str(erantzuna.reason))
        time.sleep(15)

def ezabatuEdukia():
    metodoa = 'DELETE'
    uria = "https://api.thingspeak.com/channels/"+str(CHANNEL_ID)+"/feeds.json"
    goiburuak = {'Host': 'api.thingspeak.com','Content-Type': 'application/x-www-form-urlencoded'}
    parametro ={'api_key': USER_API_KEY}
    edukia=''
    edukia_encoded = urllib.parse.urlencode(edukia)
    erantzuna = requests.request(metodoa, uria, headers=goiburuak, params=parametro,
                                 data=edukia_encoded, allow_redirects=False)
    print("Edukia ezabatzean: "+str(erantzuna.status_code)+" "+erantzuna.reason)

def sortuCVS(hiztegia):
    with open('100lagina.csv', 'w', newline='', encoding='utf8') as csvfile:
        fitxategi = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        feedsParam=[]
        if hiztegia['feeds'].__len__()==0:
            print("Ez dago daturik")
        else:
            for param in hiztegia['feeds'][0]:
                if not param.__eq__('entry_id'):
                    feedsParam.append(param)
            fitxategi.writerow(feedsParam)

            for param in hiztegia['feeds']:
                timestamp = param[feedsParam[0]]
                cpu=param[feedsParam[1]]
                ram=param[feedsParam[2]]
                fitxategi.writerow([str(timestamp), str(cpu), str(ram)])

def lortu100Lagin():
    metodoa = 'GET'
    uria = "https://api.thingspeak.com/channels/"+str(CHANNEL_ID)+"/feeds.json"
    goiburuak = {'Host': 'api.thingspeak.com','Content-Type': 'application/x-www-form-urlencoded'}
    edukia ={'api_key': WRITE_API_KEY, 'results':100}
    edukia_encoded = urllib.parse.urlencode(edukia)
    erantzuna = requests.request(metodoa, uria, headers=goiburuak,
                                 data=edukia_encoded, allow_redirects=False)
    print("Edukia lortzean: "+str(erantzuna.status_code)+" "+erantzuna.reason)
    return erantzuna.content

def handler(sig_num, frame):
     # Gertaera kudeatu
     print('\nSignal handler called with signal ' + str(sig_num))
     hiztegia = json.loads(lortu100Lagin())
     sortuCVS(hiztegia)
     ezabatuEdukia()
     sys.exit(0)

if __name__ == "__main__":
    # SIGINT jasotzen denean, "handler" metodoa exekutatuko da
    signal.signal(signal.SIGINT, handler)
    apikey_file = Path('UserApiKey.txt')
    if apikey_file.is_file():
        with open(apikey_file, 'r', encoding='utf8') as file:
            USER_API_KEY = file.readline()
    else:
        print("Zure erabiltzailearen ID-arekin sortu UserApiKey.txt fitxategia. Bestela defektuz dagoena erabiliko da.")
    create_channel()
    time.sleep(2)
    print("Kanala 15 segunduro eguneratzen hasiko da")
    with open('ApiKey.txt', 'r', encoding='utf8') as file:
        CHANNEL_ID = int(file.readline())
        WRITE_API_KEY = file.readline()
    update_channel()

