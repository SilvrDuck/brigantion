from termcolor import colored

def cprint(
    text, 
    color=None, 
    on_color=None,
    attrs=None
):
    """
    Colorize text.

    Available text colors:
    red, green, yellow, blue, magenta, cyan, white.  

    Available text highlights:
    on_red, on_green, on_yellow, on_blue, on_magenta, on_cyan, on_white.  

    Available attributes:
    bold, dark, underline, blink, reverse, concealed.
    """
    print(colored(text, color, on_color, attrs))