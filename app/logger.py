import time
from app import config
import requests

while True:
    with open('app/data/logs/copy.log', 'w', encoding='latin-1') as f:
        logs = requests.get(f'{config.ip_pj}/logs')
        for l in logs.json()['logs']:
            f.write(l)

    time.sleep(3)