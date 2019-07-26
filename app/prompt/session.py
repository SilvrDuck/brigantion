from prompt_toolkit.styles import Style
from prompt_toolkit import PromptSession

from app.prompt.validator import CmdValidator

style = Style.from_dict({
    # User input (default text).
    '':          '#ff0066',

    # Prompt.
    'username': '#884444',
    'at':       '#00aa00',
    'colon':    '#0000aa',
    'pound':    '#00aa00',
    'host':     '#00ffff bg:#444400',
    'path':     'ansicyan underline',
})


def message():
    return [
        ('class:username', 'john'),
        ('class:at',       '@'),
        ('class:host',     'localhost'),
        ('class:colon',    ':'),
        ('class:path',     '/user/john'),
        ('class:pound',    '# '),
    ]

session = PromptSession(
    style=style,
    #complete_while_typing=True,
    #validate_while_typing=True,
    #enable_history_search=True,
    #search_ignore_case=True,
    validator=CmdValidator(),
    validate_while_typing=False,
    #completer
    #auto_suggest
)