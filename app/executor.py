from app.cmd import Cmd
from app.documents import create_doc
from app import config


def exec_cmd(cmd, args):
    switch = {Cmd.lire: lire}
    switch = {Cmd.liste: liste}
    switch.get(cmd, default)(args)


def default(session, args):
    raise ValueError(f"Commande inconnue avec arguments {args}")


def lire(args):

    print(args)


def liste(args):
    path = config.data_path

    documents = []
    for f in path.iterdir():
        with open(f, "r") as d:
            documents.append(create_doc(d))
