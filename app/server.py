from flask import Flask, request, jsonify
from app.documents import all_documents, get_emails
from app import config
import pyttsx3 
import random
import string
from datetime import datetime, timedelta
from random import randint

def rstr(stringLength=12):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return '___' + ''.join(random.choice(letters) for i in range(stringLength))

app = Flask(__name__)    


engine = pyttsx3.init() 
engine.setProperty('voice', config.voice_hkey) 


@app.route('/voice', methods=['POST'])
def voice():
    say_text(request.json['text'])
    return 'ok', 200
    

@app.route('/email', methods=['POST'])
def email():
    with open(f'{config.emails_path}/{rstr()}.txt', 'w', encoding='latin-1') as f:
        f.write(f"__SUBJECT__ {request.json['subject']}\n")
        f.write(f"__SOURCE__ {request.json['author']}\n")
        for l in request.json['text']:
            f.write(l)

    say_text(f"nouveau message reçu de {request.json['author']}")
    return 'ok', 200


@app.route('/email_to_pnj', methods=['POST'])
def email_to_pnj():
    now = datetime.utcnow().strftime('%H:%M')

    sentpath = config.sent_path
    with open(sentpath, 'r', encoding='latin-1') as f:
        all = f.readlines()

    with open(sentpath, 'w', encoding='latin-1') as f:
        for l in all:
            f.write(l)
        f.write('\n\n' + '#' * 40 + '\n\n')

        f.write(f'Heure : {now}\n')
        f.write(f"Destinataire : {request.json['dest']}\n")
        f.write(f"Sujet : {request.json['subject']}\n")
        for l in request.json['text']:
            f.write(l)
    return 'ok', 200

@app.route('/get_pj_email', methods=['GET'])
def get_pj_email():
    with open(config.sent_path, 'r', encoding='latin-1') as f:        
        return jsonify({'emails': f.readlines()})


@app.route('/document', methods=['POST'])
def document():
    with open(f'{config.documents_path}/{rstr()}.txt', 'w', encoding='latin-1') as f:
        f.write(f"__TITLE__ {request.json['title']}\n")
        if request.json['hidden']:
            f.write('__HIDDEN__\n')
        if request.json['pswd'] is not None:
            f.write(f"__PWD__ {request.json['pswd']}\n")

        for l in request.json['text']:
            f.write(l)
    return 'ok', 200

@app.route('/delete', methods=['POST'])
def delete():
    to_del = request.json['title'].lower()
    if all([d.isdigit() for d in to_del]): # email
        key = int(to_del)
        email = get_emails().get(key, None)
        if email is not None:
            with open(email.file, 'w', encoding='latin-1') as f:
                f.write('')
            return 'ok', 200
        else:
            return 'unkown mail', 500

    else: # document
        doc = all_documents().get(to_del, None)
        if doc is not None:
            with open(doc.file, 'w', encoding='latin-1') as f:
                f.write('')
            return 'ok', 200
        else:
            return 'unkown doc', 500

@app.route('/list_doc', methods=['GET'])
def list_doc():
    return jsonify({d.title: {
        'pass': d.pwd,
        'hidden': d.hidden,
        'text': f'{d.text[:40]}...',
    } for d in all_documents().values()})

@app.route('/list_email', methods=['GET'])
def list_email():
    return jsonify({e.id_: {
        'auteur': e.source,
        'sujet': e.subject,
        'text': f'{e.text[:40]}...',
    } for e in get_emails().values()})


@app.route('/logs', methods=['GET'])
def logs():
    with open(config.active_log_path, 'r', encoding='latin-1') as f:        
        return jsonify({'logs': f.readlines()})


@app.route('/time_to_explosion', methods=['GET'])
def time_to_explosion():
    return time_left()


def time_left():
    delta = config.next_boom - datetime.utcnow()
    min_left = round(delta.total_seconds() // 60)
    sec_left = round(delta.total_seconds() % 60)
    return jsonify({
        'min': min_left,
        'sec': sec_left,
    })

@app.route('/reset_timer', methods=['GET'])
def reset_timer():
    config.next_boom = datetime.utcnow() + \
    timedelta(minutes=randint(
        config.explosion_min, 
        config.explosion_max
    ))
    return time_left()

def say_text(text):
    engine.say(text) 
    engine.runAndWait() 
    engine.stop()




if __name__ == "__main__":
    app.run()