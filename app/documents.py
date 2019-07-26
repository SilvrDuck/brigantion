import re
from enum import Enum, auto


class Prop(Enum):
    TITLE = auto()
    PASS = auto()
    HIDDEN = auto()


txt2prop = {p.name: p for p in Prop}

find_prop = re.compile(r"(?:\_\_)([A-Z]+)(?:\_\_)(.*)")


def extract_prop(s, regex=find_prop):
    match = re.match(regex, s).group(1)


def create_doc(doc):
    for l in doc:
        pass
