from pathlib import Path
from datetime import datetime, timedelta
from random import randint

documents_path = Path("app/data/documents")
emails_path = Path("app/data/emails")
sismo_path = Path("app/data/sismographe")
active_log_path = Path("app/data/logs/active.log")
sent_path = Path('app/data/logs/sent_emails.txt')

voice_hkey = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_frFR_HortenseM"

ip_pj='http://127.0.0.1:5000'

gn_year = 1963
gn_month = 2
gn_day = 21

explosion_min = 40 # minutes
explosion_max = 60 # minutes

reset_delay = 10

next_boom = datetime.utcnow() + \
    timedelta(minutes=randint(explosion_min, explosion_max))

pj_names = [
    'Anoush Ansari',
    'Svetlana Savitskaya',
    'Elena Kondakova',
    'Valentina Tereshkova',
    'Konstantin Feoktistov',
    'Vladimir Komarov',
    'Andriyan Nikolayev',
    'Pavel Popovich',
    'Valery Bykovsky',
    'Alexei Leonov',
    'Valeri Kubasov',
    'Gherman Titov',
]