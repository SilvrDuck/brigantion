from prompt_toolkit.shortcuts import yes_no_dialog

from app.prompt.session import session, message
from app.cmd import txt2cmd
from app.executor import exec_cmd
from app.sender import send_error

if __name__ == '__main__':

    while True:
        try:
            cmd, *args = session.prompt(message=message()).split()

            exec_cmd(txt2cmd[cmd], args)

        except Exception as e:
            send_error(e)