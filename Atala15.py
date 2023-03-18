import psutil
import requests
import urllib.parse
import json
import time

USER_API_KEY = "NKS6F9SMZR4FI5Y7"
CHANNEL_ID = 0
WRITE_API_KEY = ""


def create_channel():
    metodoa = 'GET'
    uria = "https://api.thingspeak.com/channels.json"
    goiburuak = {'Host': 'api.thingspeak.com'}
    edukia =''
    parametros={'api_key': USER_API_KEY}

    erantzuna = requests.request(metodoa, uria, headers=goiburuak, params=parametros,
                                 data=edukia, allow_redirects=False)

    with open('ApiKey.txt', 'r') as file:
        channelId = int(file.readline())

    # JSON PARSEATU
    badago = False
    banatua = json.loads(erantzuna.content)
    for i in range(banatua.__len__()):
        if banatua[i]['id']==int(channelId):
            badago=True

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

            with open('ApiKey.txt', 'w') as f:
                f.write(str(id) + "\n")
                f.write(key)

def update_channel():
    while True:
    #KODEA: psutil liburutegia erabiliz, %CPU eta %RAM atera
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory().percent
        #print("CPU: %" + str(cpu) + "\tRAM: %" + str(ram))

        metodoa = 'POST'
        uria = "https://api.thingspeak.com/update.json"
        goiburuak = {'Host': 'api.thingspeak.com',
                     'Content-Type': 'application/x-www-form-urlencoded'} # json o x-www-form-urlencoded??????????
        edukia = {'api_key': WRITE_API_KEY, 'name': 'Nire kanala',
                  "field1": cpu, "field2": ram}
        edukia_encoded = urllib.parse.urlencode(edukia)
        goiburuak['Content-Length'] = str(len(edukia_encoded))

        erantzuna = requests.request(metodoa, uria, headers=goiburuak,
                                     data=edukia_encoded, allow_redirects=False)
        print(erantzuna.status_code)
        print(erantzuna.reason)
        print(erantzuna.content)
        time.sleep(5)

if __name__ == "__main__":
    print("Using channel...")
    create_channel()
    with open('ApiKey.txt', 'r') as file:
        CHANNEL_ID = int(file.readline())
        WRITE_API_KEY = file.readline()
    update_channel()
