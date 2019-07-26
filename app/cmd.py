from enum import Enum, auto


class Cmd(Enum):
    lire = auto()
    liste = auto()
    envoyer = auto()
    destinataires = auto()
    sismographe = auto()


cmd2txt = {c: c.name for c in Cmd}
txt2cmd = {v: k for k, v in cmd2txt.items()}
cmd_list = [c.name for c in Cmd]
