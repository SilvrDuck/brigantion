from prompt_toolkit.shortcuts import yes_no_dialog

from app.prompt import session, message, cprint, term_size
from app.executor import exec_cmd
from app.sender import send_error
from datetime import datetime
from app.documents import clean_emails


from colorama import init
init()

clean_emails()

# explosion avec code et timer
# entrée de choix pour la redistribution
# lire des voix à distance


if __name__ == "__main__":

    while True:
        try:
            ru = f"Это реальное время UTC, если когда-либо: 22.11.1963 {datetime.utcnow().strftime('%H:%M')}"
            cprint(
                f'\n+++ {ru}  ' + 
                '+' * (term_size()[1] - len(ru) - 6),
                on_color='on_blue'
            )
            print()

            cmd, *args = session.prompt(message=message()).split()
            
            exec_cmd(cmd, args)

        except Exception as e:
            send_error(e)
