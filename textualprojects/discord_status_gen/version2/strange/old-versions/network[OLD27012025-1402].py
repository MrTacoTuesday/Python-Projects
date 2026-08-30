"""
English Language:
{s} {v} {o}
{s} {v}
{v[command]}
"""

"""
How would I make a neural network for autocompletion?
A list of all punctuations used (P), indexed
A list of all words used (W), indexed
A text document tokenized into indices, [0,P.length)U[P.length, P.length + W.length)

NN input is indices of the last five items used
using context of last items words, suggest the 3 options for the next item index

Training data would be gathered from many text sources... orr I might could just use my own writings to make it similar to my style (?)
"""

"""
How would I train?
7 input tokens, 1 output token

"Hi how are you? I'm doing well!" -> ["Hi", " ", "how", " ", "are", " ", "you", "?", "I", "'", "m", " ", "doing", " ", "well", "!"]
    -> [1, 2, 3, 2, 4, 2, 5, 6, 7, 8, 9, 2, 10, 2, 11, 12]
Batch:
    Train [_, _, _, _, _, _, 1] -> 2;
    ...
    Train [_, _, _, 1, 2, 3, 2] -> 4
    ...
    Train [1, 2, 3, 2, 4, 2, 5] -> 6;
    Train [2, 3, 2, 4, 2, 5, 6] -> 7;
    Train [3, 2, 4, 2, 5, 6, 7] -> 8;
    Train [2, 4, 2, 5, 6, 7, 8] -> 9;
    ...
    Train [7, 8, 9, 2, 10, 2, 11] -> 12;
    Train [8, 9, 2, 10, 2, 11, 12] -> _;
    
"""

from base64 import b64encode;
from functools import reduce
from hashlib import sha256;
import json
import os
from typing import Callable, Generic, Literal, TypeVar

with open("known_characters.txt", encoding="utf-8") as f:
    KNOWN_CHARS = f.read();
with open("known_symbols.txt", encoding="utf-8") as f:
    KNOWN_SYMBOLS = f.read();
    
def update_known_characters(new_characters: str) -> None:
    global KNOWN_CHARS;
    KNOWN_CHARS += new_characters;
    with open("known_characters.txt", "w", encoding="utf-8") as f:
        f.write(KNOWN_CHARS);
def update_known_symbols(new_symbols: str) -> None:
    global KNOWN_SYMBOLS;
    KNOWN_SYMBOLS += new_symbols;
    with open("known_symbols.txt", "w", encoding="utf-8") as f:
        f.write(KNOWN_SYMBOLS);

def cipher_hash_b64(obj: object) -> bytes:
    return b64encode(sha256(str(obj).encode()).digest())

_K = TypeVar("_K");
_T = TypeVar("_T");        
class JSONData(Generic[_K, _T]):
    def __init__(self, data: dict[_K, _T], file: str) -> None:
        self.data = data;
        self.filename = file;
    def read(self) -> dict[_K, _T]:
        with open(self.filename, encoding="utf-8") as f:
            _dat = json.loads(f.read());
        assert isinstance(_dat, dict);
        self.data.update(_dat);
        return self.data;
    def write(self) -> None:
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.data, f, separators=(",",":"));
    def update(self, data: dict[_K, _T] = {}) -> None:
        self.data.update(data);
        self.write();

CHAR_VALIDATION: JSONData[str, str] = JSONData({}, "char_validation.json");
def add_char_validation(chars: str, key:Literal["letters", "symbols"]) -> None:
    global CHAR_VALIDATION;
    CHAR_VALIDATION.data.setdefault(key, "");
    for char in chars:
        if char not in CHAR_VALIDATION.data[key]:
            CHAR_VALIDATION.data[key] += char;
    CHAR_VALIDATION.write();

TOKENS: JSONData[str,int] = JSONData({}, "tokens.json");
def add_tokens(*tokens: str) -> None:
    global TOKENS;
    TOKENS.read();
    TOKENS.update({tokens[i]: len(TOKENS.data)+i for i in range(len(tokens)) if tokens[i] not in TOKENS.data});

TRAINING_DATA: JSONData[str,list[int]] = JSONData({}, "training_data.json");
def add_training_data(data: tuple[int,...]) -> None:
    global TRAINING_DATA;
    key = str(cipher_hash_b64(data), encoding="utf-8");
    if key not in TRAINING_DATA.data:
        TRAINING_DATA.update({key: list(data)});


class Tokenizer:
    def __init__(self, file: str) -> None:
        self.char = "\b0";
        self.tokens: list[str] = [];
        self.indices: tuple[int, ...] = tuple();
        self.document = open(file,encoding="utf-8");
        
    def next(self) -> None:
        if self.char == "":
            raise RuntimeError("Reached EOF");
        try:
            self.char = self.document.read(1);
        except Exception as e:
            print("Error Detected in parsing: ");
            raise e;
        #print("Char::", ascii(self.char), "Tell::", self.document.tell());
        
    def _issymbol(self, str: str) -> bool:
        #return str in KNOWN_SYMBOLS;
        return str in CHAR_VALIDATION.data.get("symbols","");
    
    def _ischar(self, str:str) -> bool:
        #return str in KNOWN_CHARS;
        return str in CHAR_VALIDATION.data.get("letters", "");
    
    def tokenize(self):
        self.next();
        while (self._make_token(self._ischar) or self._make_token(self._issymbol) or self._make_token(str.isdigit) or self._make_token(str.isspace)):
            if self.char == "":
                break;
        else:
            print("Unknown Character::", ascii(self.char), "/", self.char);
            I = input("Add to registry (Y/N) >>> ");
            if I == "Y":
                match input("Type:: [S]ymbol | [L]etter >>> "):
                    case "S": 
                        print("Updating...");
                        #update_known_symbols(self.char);
                        add_char_validation(self.char, "symbols");
                    case "L":
                        print("Updating...");
                        #update_known_characters(self.char);
                        add_char_validation(self.char, "letters");
                self.document.seek(0);
                self.tokens.clear();
                return self.tokenize();
            elif I == "N":
                raise RuntimeError("TOKENIZER/TOKENIZE:: Unknown Character:", ascii(self.char), "/", self.char);
        self.document.close();
        add_tokens(*self.tokens);
        self.indices = tuple([TOKENS.data[k] for k in self.tokens]);
        add_training_data(self.indices);
    
    def _make_token(self, condition: Callable[[str],bool]) -> bool:
        token = ""
        while (condition(self.char) and self.char != ""):
            token += self.char;
            self.next();
        if token != "":
            self.tokens.append(token);
            return True;
        return False;

dir = "./documents/";
for entry in os.scandir(dir):
    if entry.is_file() and entry.name.endswith(".txt"):
        Tokenizer(dir + entry.name).tokenize();

print(TRAINING_DATA.data);

