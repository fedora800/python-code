import alpaca.config as config
import json
import requests


API_KEY = "CKQGTOEKCROULTOHKJS9"
API_SECRET_KEY = "vQ8w3DC7m9GvDipwWF2Ra5WhDvGblBLS8Isg8xS7"

API_KEY = config.API_KEY
API_SECRET_KEY = config.API_SECRET_KEY
BASE_URL = "https://broker-api.sandbox.alpaca.markets"
ACCOUNT_URL = '{}/v2/account'.format(BASE_URL)
HEADERS = {"APCA-API-KEY-ID": API_KEY, "APCA-API-SECRET-KEY": API_SECRET_KEY}

def get_account():
    r = requests.get(ACCOUNT_URL, headers=HEADERS)
    return json.loads(r.content)



test = get_account()
print(test)