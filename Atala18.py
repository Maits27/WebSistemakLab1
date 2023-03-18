import requests
import urllib.parse


USER_API_KEY = "NKS6F9SMZR4FI5Y7"
CHANNEL_ID = 0
WRITE_API_KEY = ""

with open('ApiKey.txt', 'r') as file:
    CHANNEL_ID = int(file.readline())
    WRITE_API_KEY = file.readline()

metodoa = 'DELETE'
uria = "https://api.thingspeak.com/channels/"+str(CHANNEL_ID)+"/feeds.json"
goiburuak = {'Host': 'api.thingspeak.com','Content-Type': 'application/x-www-form-urlencoded'}
parametro ={'api_key': USER_API_KEY}
edukia=''
edukia_encoded = urllib.parse.urlencode(edukia)
erantzuna = requests.request(metodoa, uria, headers=goiburuak, params=parametro,
                             data=edukia_encoded, allow_redirects=False)
print(str(erantzuna.status_code)+" "+erantzuna.reason)
print(erantzuna.content)