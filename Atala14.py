import requests
import urllib.parse
import psutil
import time

USER_API_KEY = "NKS6F9SMZR4FI5Y7"
CHANNEL_ID = 0
WRITE_API_KEY = ""

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
     print("Updating channel...")
     with open('ApiKey.txt', 'r') as file:
         cid=int(file.readline())
         wak=file.readline()
         CHANNEL_ID=cid
         WRITE_API_KEY=wak
     update_channel()


