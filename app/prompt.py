from prompt_toolkit.styles import Style
from prompt_toolkit import PromptSession
from app.documents import get_emails
from app.utils import cprint
import os

style = Style.from_dict(
    {
        "": "#ff0066",
        "emails": "#884444",
        "colon": "#0000aa",
        "pound": "#00aa00",
        "project": "ansicyan underline",
    }
)

def message():
    emails = [e for e in get_emails().values() if not e.is_read]

    ret = []
    if len(emails) > 0:
        ret.extend([
            ("class:emails", f"{len(emails)} messages non lus "),
            ("class:colon", ": "),
        ])

    ret.extend([
        ("class:project", "idunn"),
        ("class:pound", "# "),
    ])

    return ret


session = PromptSession(
    style=style,
    validate_while_typing=False,
)





def term_size():
    """
    Returns rows × columns
    """
    r, c = os.popen('stty size', 'r').read().split()
    return int(r), int(c)