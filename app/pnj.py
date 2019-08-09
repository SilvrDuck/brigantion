from prompt_toolkit import prompt, PromptSession
from datetime import datetime
import requests
from app import config
from unidecode import unidecode
from pprint import pprint
import json
from colorama import init
init()


## Launch :
# Set proper IP in config (ipconfig in terminal)
#
# powershell :
# python -m app.logger
#
# powershell :
# python -m app.pnj
#
# powershell :
# python -m app.mailclient


def exec_pnj_cmd(cmd, args):
    if cmd == 'voice':
        resp = requests.post(
            f'{config.ip_pj}/voice', 
            json={'text': args},
        )
        print(resp.content)
    ################################
    elif cmd == 'email':
        subject = prompt(message='sujet : ')
        author = prompt(message='envoyeur : ')
        text = prompt(
            message='text (Esc+Enter pour envoyer): ',
            multiline=True,
        )

        cancel = prompt(message='Annuler ? (écrire "oui" sinon sera envoyé)')
        if 'oui' not in cancel:
            resp = requests.post(
                f'{config.ip_pj}/email',
                json={
                    'subject': subject,
                    'author': author,
                    'text': text,
                },
            )
            print(resp.content)
    ################################
    elif cmd == 'newdoc':
        print('attention, va créer un doc chez les PJ')
        title = prompt(message='titre (garder court) : ')
        title = unidecode(title).strip()
        hidden = prompt(message='cachés ? (oui si oui) : ')
        hidden = True if 'oui' in hidden.lower() else False
        pswd = prompt(message='mot de passe (rien = aucun) : ').strip()
        pswd = pswd if len(pswd) > 0 else None
        text = prompt(
            message='text (Esc+Enter pour envoyer) : ',
            multiline=True,
        )

        send = prompt(message='Envoyer ? (écrire "oui", sinon sera annulé)')
        if 'oui' in send:
            resp = requests.post(
                f'{config.ip_pj}/document',
                json={
                    'title': title,
                    'hidden': hidden,
                    'pswd': pswd,
                    'text': text,
                },
            )
            print(resp.content)
    ################################
    elif cmd == 'delete':
        print('Dangereux !!!')
        title = prompt(message='Nom du document (ou numéro pour email) : ')
        send = prompt(message='Effacer ? (écrire "oui", sinon sera annulé)')
        if 'oui' in send:
            resp = requests.post(
                f'{config.ip_pj}/delete',
                json={
                    'title': title,
                },
            )
            print(resp.content)
    ################################
    elif cmd == 'list_doc':
        resp = requests.get(f'{config.ip_pj}/list_doc')
        print(json.dumps(resp.json(), indent=4))
    ################################
    elif cmd == 'list_email':
        resp = requests.get(f'{config.ip_pj}/list_email')
        print(json.dumps(resp.json(), indent=4))
    ################################
    elif cmd == 'logs':
        resp = requests.get(f'{config.ip_pj}/logs')
        print(''.join(resp.json()['logs']).encode().decode("latin-1"))
    ################################
    else:
        print('Commande inconnue.')



if __name__ == "__main__":

    session = PromptSession()

    while True:
        try:
            input_ = session.prompt(message=f"{datetime.utcnow().strftime('%H:%M')}: ").split()
            
            if len(input_) > 0:
                cmd, *args = input_
                exec_pnj_cmd(cmd, args)

        except Exception as e:
            print(e)