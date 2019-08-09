from prompt_toolkit.shortcuts import yes_no_dialog

from app.prompt import session, message, cprint, term_size
from app.executor import exec_cmd
from app.sender import send_error
from datetime import datetime
from app import config
from app.documents import clean_emails

from colorama import init
init()

clean_emails()

## Consider launching 
# retro-term :
# python3 -m app.joueurs 2>&1 | tee app/data/logs/active.log
#
# powershell :
# python -m app.server
#
# powershell :
# python -m app.timer

# entrée de choix pour la redistribution

with open(config.active_log_path, 'w', encoding='latin-1') as f:
    f.write('')


if __name__ == "__main__":

    while True:
        try:
            """ ru = f"Это реальное время UTC, если когда-либо: 22.11.1963 {datetime.utcnow().strftime('%H:%M')}"
            cprint(
                f'\n+++ {ru}  ' + 
                '+' * (term_size()[1] - len(ru) - 6),
                on_color='on_blue'
            )
            print() """

            input_ = session.prompt(message=message()).split()
            
            if len(input_) > 0:
                cmd, *args = input_
                exec_cmd(cmd, args)

        except Exception as e:
            send_error(e)
