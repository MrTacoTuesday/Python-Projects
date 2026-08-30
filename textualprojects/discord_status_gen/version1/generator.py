# generator.py
# generates a Discord status randomly


with open("opening_phrase.txt") as file:
    OPENING_PHRASES = file.read().splitlines();
    
with open("actions.txt") as file:
    ACTIONS = file.read().splitlines();
with open("colors.txt") as file:
    COLORS = file.read().splitlines();
with open("subjects.txt") as file:
    SUBJECTS = file.read().splitlines();
with open("timing.txt") as file:
    TIMING = file.read().splitlines();
PERSONAL_POSSESSIVE = ["my","his","her","your","their"];

with open("structure.txt") as file:
    STRUCTURE = file.read().splitlines();


from random import choice;


def generate() -> str:
    opening_phrase = choice(OPENING_PHRASES);
    structure = choice(STRUCTURE);
    return " ".join([opening_phrase, parse_structure(structure)]);

def foobar(result: str, items: list[str], indicator: str) -> str:
    _result = result;
    for i in [choice(items) for _ in range(_result.count(indicator))]: 
        _result = _result.replace(indicator, i, 1);
    return _result;

def parse_structure(item: str) -> str:
    _result = foobar(item, ACTIONS, "{a}");
    _result = foobar(_result, COLORS, "{c}");
    _result = foobar(_result, SUBJECTS, "{s}");
    _result = foobar(_result, TIMING, "{t}"); # must come after subjects
    _result = foobar(_result, PERSONAL_POSSESSIVE, "{pp}"); # must come after subjects
    return _result;

i = 1;
_k = "";
while _k == "":
    print(f"#{i}: {generate()}",end="");
    _k = input();
    i += 1;