from prompt_toolkit.validation import Validator, ValidationError

from app.cmd import cmd_list

class CmdValidator(Validator):

    def validate(self, document):
        text = document.text

        if text:
            cmd = text.split()[0]
            if cmd not in cmd_list:
                raise ValidationError(message=f'La commande {cmd} n’existe pas.')                                