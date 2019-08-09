import time
from datetime import datetime, timedelta
import requests
from app import config



while True:
    try:
        with open('app/data/logs/received.txt', 'w', encoding='latin-1') as f:
            resp = requests.get(f'{config.ip_pj}/get_pj_email')
            f.write(''.join(resp.json()['emails']).encode().decode("latin-1"))
            print('update')
        time.sleep(5)

    except Exception as e:
        print(e)