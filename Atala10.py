import requests
import urllib.parse
USER_API_KEY = "NKS6F9SMZR4FI5Y7"
def create_channel():
     metodoa = 'POST'
     uria = "https://api.thingspeak.com/channels.json"
     goiburuak = {'Host': 'api.thingspeak.com',
          'Content-Type': 'application/x-www-form-urlencoded'}
     edukia = {'api_key': USER_API_KEY,
          'name': 'Nire kanala', 'field1': "%CPU", 'field2': "%RAM"}
     edukia_encoded = urllib.parse.urlencode(edukia)
     goiburuak['Content-Length'] = str(len(edukia_encoded))
     print("\n" + uria)
     print(edukia_encoded)
     erantzuna = requests.request(metodoa, uria, headers=goiburuak,
          data=edukia_encoded, allow_redirects=False)
     kodea = erantzuna.status_code
     deskribapena = erantzuna.reason
     print(str(kodea) + " " + deskribapena)
     edukia = erantzuna.content
     print(edukia)
if __name__ == "__main__":
     print("Creating channel...")
     create_channel()
     print("Channel created. Check on ThingSpeak")