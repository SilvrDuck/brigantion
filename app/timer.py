import time
from datetime import datetime, timedelta
import requests
from app import config



annonces = {
    1: 'explosion imminante ! Entrez immédiatement le mot de passe.',
    2: 'explosion dangeuresement proche, entrez le mot de passe',
    5: 'explosion prochaine, entrez le mot de passe au plus vite',
    10: 'explosion procheaine, entrez le mot de passe',
}

said = {k: False for k in annonces.keys()}

print('timer lancé')

while True:
    try:
        json = requests.get(f'{config.ip_pj}/time_to_explosion').json()
        print(f"time left {json['min']}.{json['sec']}")

        keys = [k for k in annonces.keys() if k > json['min']]
        key = max(keys) if len(keys) > 0 else None

        if key is not None and not said[key]:
            resp = requests.post(
                f'{config.ip_pj}/voice', 
                json={'text': annonces[key]},
            )
            print(resp.content)
            said[key] = True

        said[1] = False
        time.sleep(5)

    except Exception as e:
        print(e)