
from app.cmd import Cmd

def exec_cmd(cmd, args):
    switch = {
        Cmd.lire: lire
    }
    switch.get(cmd, default)(args)

def default(session, args):
    raise ValueError(f'Commande inconnue avec arguments {args}')

def lire(session, args):
    
    print(args)