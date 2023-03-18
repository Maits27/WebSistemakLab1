import json as json

jsonKate= '{"id":2033571,"name":"Nire kanala","description":null,"latitude":"0.0","longitude":"0.0","created_at":"2023-02-14T19:33:17Z","elevation":null,"last_entry_id":null,"public_flag":false,"url":null,"ranking":30,"metadata":null,"license_id":0,"github_url":null,"tags":[],"api_keys":[{"api_key":"O5IPG5FW0B1IN6LO","write_flag":true},{"api_key":"1IQLFMJ7VOC07NEZ","write_flag":false}]}'

if __name__ == '__main__':
    banatua= json.loads(jsonKate)
    id=banatua['id']
    key=""
    for api in banatua['api_keys']:
        if api['write_flag']==True:
            key=api['api_key']
    print("ID-a: " + str(id))
    print("API key-a: " + key)

    with open('ApiKey.txt', 'w') as f:
        f.write(str(id)+"\n")
        f.write(key)