# version 1
def load_and_reformat(file: str) -> list[str]:
    with open(file, "r") as f:
        _result = sorted(f.read().upper().split());
    with open(file, "w") as f:
        f.write(" ".join(_result));
    return _result

NOUNS = load_and_reformat("nouns.txt");
ADJECTIVES = load_and_reformat("adjectives.txt");

SPECIAL = list("~`!@#$%^&*_-+=|\\:;\"\'<,>.?/");
ALPHA = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ");
NUM = list("0123456789");

REPLACEMENT = {
    "a": "4@",
    "b": "6>",
    "c": "<",
    "e": "3",
    "g": "6",
    "h": "%#",
    "i": "1!",
    "l": "1/",
    "n": "^",
    "o": "0*",
    "p": "?",
    "s": "5$",
    "x": "%",
    "z": "27",
};


from random import choice, randint, random;

def presuf() -> str:
    if 3*random() < 1:
        if 2*random() < 1: return str(randint(0,999));
        return "".join([choice(ALPHA + NUM + SPECIAL) for _ in range(randint(1,3))]);
    return "";

def pw() -> str:
    adj, noun, sep = choice(ADJECTIVES), choice(NOUNS), choice(SPECIAL) if 3*random() < 1 else "";
    pre, suf = presuf(), presuf();
    _ = pre + adj.title() + sep + noun.title() + suf;
    print(_);
    phrase = "";
    for char in _:
        if char.lower() in REPLACEMENT and 2*random() < 1:
            char = choice(REPLACEMENT[char.lower()]);
        phrase += char;
    return phrase;

def pw2() -> str:
    length = randint(8,18);
    s = "";
    while len(s) < length:
        if 8*random() < 5: # 5/8, 40/64
            s += choice(ALPHA);
        elif 8*random() < 5: # 15/64
            s += choice(NUM);
        else: # 9/64
            s += choice(SPECIAL);
    return s;



weston = 0x365ee6e6;
ryley = 0x365ef869;

print(weston, ryley);
print(weston-ryley);

#print(pw2());
    