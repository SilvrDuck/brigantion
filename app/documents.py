import re
from enum import Enum, auto
from collections import namedtuple
from prompt_toolkit.shortcuts import input_dialog
from app import config
from app.utils import cprint
import os
from datetime import datetime
from random import randint

find_tag = re.compile(r"(?:\_\_)([A-Z]+)(?:\_\_)(.*)")


def extract_tag(s, regex=find_tag):
    match = re.match(regex, s)
    if match is not None:
        return match.group(1), match.group(2).strip()
    else:
        return '', ''

# Docs

Document = namedtuple('Document', 'title pwd hidden text') # str str bool str

def create_doc(doc):
    title = None
    pwd = None
    hidden = False
    text = []

    for l in doc:
        tag, content = extract_tag(l)
        if tag == 'TITLE':
            title = content
        elif tag == 'PWD':
            pwd = content
        elif tag == 'HIDDEN':
            hidden = True
        else:
            text.append(l)

    if title is not None:
        return Document(
            title=title,
            pwd=pwd,
            hidden=hidden,
            text=''.join(text)
        )

def read_doc(doc):
    if doc.pwd is not None:
        in_title = 'Fichier protégé'
        in_text = 'Veuillez entrer le mot de passe du fichier «{}».'.format(doc.title)

        for __ in range(3):
            pwd = pwd_dialog(in_title, in_text)
            
            if pwd is None:
                return
            elif pwd == doc.pwd:
                break
            else:
                in_title = 'Mot de passe incorrect'
                in_text = 'Veuillez ré-essayer d’entrer le mot de pass du fichier «{}».'.format(doc.title)
        else:
            print('Trop de tentatives éronnées.')
            return
    
    print(doc.text)

all_documents = {}
for f in config.documents_path.iterdir():
    with open(f, "r") as d:
        doc = create_doc(d)
        if doc is not None:
            all_documents[doc.title.lower()] = doc

## Emails

Email = namedtuple('Email', 'id_ source subject text date is_read file')
global_id = 1336

def create_email(email, file):
    id_ = None
    source = None
    subject = 'Sans sujet'
    text = []
    is_read = False
    date = None

    for l in email:
        tag, content = extract_tag(l)
        if tag == 'ID':
            id_ = int(content)
        elif tag == 'SOURCE':
            source = content
        elif tag == 'SUBJECT':
            subject = content
        elif tag == 'READ':
            is_read = True
        elif tag == 'DATE':
            date = date_from_content(content)
        else:
            text.append(l)

    if date is None:
        date = date_from_file(file)

    if id_ is None:
        global global_id
        global_id += 1
        id_ = global_id
        update_email_id(file, id_)

    if all([
        id_ is not None,
        source is not None,
        subject is not None,
        text is not None,
        is_read is not None,
        date is not None,
    ]):
        return Email(
            id_=id_,
            source=source,
            subject=subject,
            is_read=is_read,
            text=''.join(text),
            date=date,
            file=file,
        )
    else:
        return None


def get_emails():
    ret = {}
    for f in config.emails_path.iterdir():
        with open(f, 'r') as e:
            email = create_email(e, f)
            if email is not None:
                ret[email.id_] = email
    return ret

def update_email(file, new_line):
    with open(file, 'r') as f:
        all = f.readlines()
    with open(file, 'w') as f:
        f.write(f'{new_line}\n')
        [f.write(l) for l in all]

def update_email_id(file, id_):
    update_email(file, f'__ID__ {id_}')

def update_email_read(file, bool):
    if bool:
        update_email(file, '__READ__')
    else:
        with open(file, 'r') as f:
            all = f.readlines()
        with open(file, 'w') as f:
            for l in all:
                tag, _ = extract_tag(l)
                if tag != 'READ':
                    f.write(l)

def read_email(email):
    if not email.is_read:
        update_email_read(email.file, True)

    cprint(f'\nMessage de : {email.source}', color='blue', on_color='on_yellow')
    cprint(f'Sujet : {email.subject}\n', color='blue', on_color='on_yellow')
    print(email.text)


def date_from_content(content):
    try:
        moment = content.split(' ')
        date = moment[0].split('.')
        hour = moment[1].split(':')
        return datetime(
            year=int(date[2]),
            month=int(date[1]),
            day=int(date[0]),
            hour=int(hour[0]),
            minute=int(hour[1]),
        )
    except:
        return rand_date()

def clean_emails(): # only at start
    for file in config.emails_path.iterdir():
        with open(file, 'r') as f:
            all = f.readlines()
        with open(file, 'w') as f:
            for l in all:
                tag, _ = extract_tag(l)
                if tag != 'ID':
                    f.write(l)

def date_from_file(file):
    created = os.stat(file).st_ctime
    date = datetime.fromtimestamp(created)
    date = date.replace(
        year=config.gn_year, 
        month=config.gn_month,
        day=config.gn_day,
        hour=(date.hour - 2) % 24,
    )
    return date

def rand_date():
    return datetime(
        year=config.gn_year,
        month=randint(1, config.gn_month),
        day=randint(1, config.gn_day-1),
        hour=randint(7, 19),
        minute=randint(1, 59),
    )

def print_t(t):
    return t.strftime('%d.%M.%Y %H:%M')


def pwd_dialog(title='', text=''):
    return input_dialog(
        title=title, 
        text=text, 
        password=True,
        ok_text='Ok',
        cancel_text='Annuler',
    )


