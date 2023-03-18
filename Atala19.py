import json
import signal
import sys
import urllib.parse
import csv
import datetime
import requests
import urllib.parse


USER_API_KEY = "NKS6F9SMZR4FI5Y7"
CHANNEL_ID = 0
WRITE_API_KEY = ""

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
    with open('atala18.csv', 'w', newline='') as csvfile:
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
    with open('ApiKey.txt', 'r') as file:
        CHANNEL_ID = int(file.readline())
        WRITE_API_KEY = file.readline()
    # SIGINT jasotzen denean, "handler" metodoa exekutatuko da
    signal.signal(signal.SIGINT, handler)
    print('Running. Press CTRL-C to execute.')
    while True:
       pass # Ezer ez egin

