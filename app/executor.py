from app.documents import (
    create_doc,
    read_email,
    get_emails,
    read_doc,
    all_documents,
    print_t,
)
from datetime import datetime, timedelta
from random import randint
from app import config
from app.utils import cprint
import requests
from prompt_toolkit import prompt

def exec_cmd(cmd, args):       
    cmd_switch.get(cmd, default)(args)


def default(args):
    reseted = False
    if len(args) > 0:
        if args[0] == '8': # if pass was started
            reseted = reset_timer(args)

    if not reseted:
        cprint(f"Commande inconnue.", color='red')
        print(f'Commandes disponibles :')
        for cmd in sorted(cmd_switch.keys()):
            print(f'    {cmd}')


def lire(args):
    key = ' '.join(args).strip()

    if len(key) == 0:
        print('Choisissez un document ou un message à lire.')
        print('Examples: "lire 1037" ou "lire le livre rouge"')
        print('Tapez "messages" ou "documents" pour voir les fichiers disponibles.')
        return

    if all([d.isdigit() for d in key]): # email
        key = int(key)
        email = get_emails().get(key, None)
        if email is not None:
            read_email(email)
        else:
            print('Pas de message {}.'.format(key))

    else: # document
        doc = all_documents().get(key.lower(), None)
        if doc is not None:
            read_doc(doc)
        else:
            print('Le document {} n’existe pas.'.format(key))


def documents(args):
    cprint('Liste des documents disponibles', on_color='on_yellow', color='blue')
    [print(d.title) for d in all_documents().values() if not d.hidden]

def timer(args):
    json = requests.get(f'{config.ip_pj}/time_to_explosion').json()
    cprint(f"{json['min']} minutes et {json['sec']} restantes avant explosion.", color='red')
    
def reset_timer(args):
    if ' '.join(args) == '8 15 16 23 42':
        json = requests.get(f'{config.ip_pj}/time_to_explosion').json()
        delay = config.reset_delay
        if json['min'] < delay:
            resp = requests.get(f'{config.ip_pj}/reset_timer').json()
            cprint(f"Timer relancé, explosion dans {resp['min']} minutes et {resp['sec']} seconds.", color='green')
            return True
        else:
            cprint(f'Impossible de relancer le timer plus de {delay} minutes avant l’explosion.', color='red')
            cprint(f"Explosion dans {json['min']} minutes et {json['sec']} seconds.", color='red')
            return True

    return False


def envoyer(args):
    dest = prompt(message='destinataire : ')
    subject = prompt(message='sujet : ')
    text = prompt(
        message='Texte (Appuyiez sur Esc puis Enter pour envoyer) : ',
        multiline=True,
    )

    requests.post(
        f'{config.ip_pj}/email_to_pnj',
        json={
            'subject': subject,
            'dest': dest,
            'text': text,
        },
    )
    cprint('Message envoyé !', color='green')    

def messages(args):
    emails = get_emails()
    read = {k: v for k, v in emails.items() if v.is_read}
    unread = {k: v for k, v in emails.items() if not v.is_read}

    id_s = 'ID'
    so_s = 'Envoyeur'
    su_s = 'Sujet'
    da_s = 'Date'
    so_l = max([len(e.source) for e in emails.values()] + [len(so_s)]) + 2
    su_l = max([len(e.subject) for e in emails.values()] + [len(su_s)]) + 2
    da_l = 16 + 2 # len of date
    num_pad = 6

    header = f'{id_s:<{num_pad}} {da_s:<{da_l}} {so_s:<{so_l}} {su_s:<{su_l}}'
    print_m = lambda m: f'{m.id_:<{num_pad}} {print_t(m.date):<{da_l}} {m.source:<{so_l}} {m.subject:<{su_l}}'

    if len(unread) > 0:
        cprint(f'\n{len(unread)} messages non lus :', on_color='on_green', color='blue')
        cprint(header, color='blue', on_color='on_yellow')
        for m in sorted(unread.values(), key=lambda e: e.date, reverse=True):
            print(print_m(m))
    else:
        cprint('\nPas de messages non lus.', color='blue')

    if len(read) > 0:
        cprint(f'\n{len(read)} messages déjà ouverts :', on_color='on_green', color='blue')
        cprint(header, color='blue', on_color='on_yellow')
        for m in sorted(read.values(), key=lambda e: e.date, reverse=True):
            print(print_m(m))
    else:
        cprint('\nPas de messages déjà ouverts.', color='blue')

    print('\nTapez "lire [ID du message]" pour lire un message.')


cmd_switch = {
    'lire': lire,
    'documents': documents,
    'messages': messages,
    'timer': timer,
    'envoyer': envoyer,
} 