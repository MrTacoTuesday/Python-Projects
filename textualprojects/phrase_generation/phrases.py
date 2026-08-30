import json;
from typing import Any, Callable;

def InputWordTypes(word: str) -> set[str]:
    l = {
        "1": ["Noun", "noun"],
        "2": ["Adjective", "adjv"],
        "3wo": ["Verb (without object)", "verb[wo]"],
        "3wi": ["Verb (with object)", "verb[wi]"],
        "4": ["Conjunction", "conj"],
        "5": ["Pronoun", "pron"],
        "6": ["Adverb", "advb"],
        "7": ["Preposition", "prep"],
        "8": ["Interjection", "intj"],
        "9i": ["Indefinite Article", "art[i]"],
        "9d": ["Definite Article", "art[d]"],
        "10s": ["Singular or First Person", "sfp"],
        "10p": ["Plural or Second Person", "psp"]
    };
    print(f"How would you classify this word: '{word}'?");
    _prompts = {k: f"{k}: {v[0]}" for k,v in l.items()};
    _result: set[str] = set();
    k = "";
    while k != "DONE":
        prompt = "\n".join(_prompts.values()) + "\nOr type 'DONE' to finish and exit\n\n>>> ";
        k = input(prompt);
        for _k in k.split(" "):
            if _k == "DONE":
                k = _k;
                break;
            if _k in _prompts:
                del _prompts[_k];
                _result.add(l[_k][1]);
    return _result;

class Dictionary(dict[str,set[str]]):
    @staticmethod
    def ImportJSON() -> "Dictionary":
        with open("dictionary.json", "r") as file:
            return json.load(file, cls=Dictionary.Decoder);
    def ExportJSON(self) -> None:
        with open("dictionary.json", "w") as file:
            json.dump(self, file, cls=Dictionary.Encoder);
    class Decoder(json.JSONDecoder):
        def decode(self, s: str) -> "Dictionary": # type: ignore
            obj = super().decode(s);
            assert isinstance(obj, dict);
            _result = Dictionary();
            for k,v in obj.items(): # type: ignore
                assert isinstance(k, str) and isinstance(v, list);
                _result[k] = set();
                for i in v: # type: ignore
                    assert isinstance(i, str);
                    _result[k].add(i);
            return _result;
    class Encoder(json.JSONEncoder):
        def default(self, o: "Dictionary") -> dict[str,list[str]]:
            try:
                assert isinstance(o, Dictionary);
                _result = {k: list(v) for k,v in o.items()};
            except TypeError:
                pass
            else:
                return _result;
            return super().default(o);

DICTIONARY = Dictionary.ImportJSON();

def word_generator(count: int = 10) -> Callable[[],str]:
    with open("words_dictionary.json") as file:
        _d = json.load(file); # type: ignore
    assert isinstance(_d, dict);
    _d = _d.__iter__(); # type: ignore
    c: int = 0;
    def __next__() -> str:
        nonlocal c;
        while c < count:
            s: Any = _d.__next__();
            assert isinstance(s, str);
            if s not in DICTIONARY:
                c += 1;
                return s;
        raise StopIteration;
    return __next__;
        

class WORD:
    class NOUN:
        ALL = {k for k in DICTIONARY.keys() if "noun" in DICTIONARY[k]};
        SINGULAR = {k for k in ALL if "sfp" in DICTIONARY[k]};
        PLURAL = {k for k in ALL if "psp" in DICTIONARY[k]};
    class ADJECTIVE:
        ALL = {k for k in DICTIONARY.keys() if "adjv" in DICTIONARY[k]};
        SINGULAR = {k for k in ALL if "sfp" in DICTIONARY[k]};
        PLURAL = {k for k in ALL if "psp" in DICTIONARY[k]};
    class VERB:
        class WITH_OBJECT:
            ALL = {k for k in DICTIONARY.keys() if "verb[wi]" in DICTIONARY[k]};
            FIRSTPERSON = {k for k in ALL if "sfp" in DICTIONARY[k]};
            SECONDPERSON = {k for k in ALL if "psp" in DICTIONARY[k]};
        class WITHOUT_OBJECT:
            ALL = {k for k in DICTIONARY.keys() if "verb[wo]" in DICTIONARY[k]};
            FIRSTPERSON = {k for k in ALL if "sfp" in DICTIONARY[k]};
            SECONDPERSON = {k for k in ALL if "psp" in DICTIONARY[k]};
        ALL = set[str].union(WITH_OBJECT.ALL, WITHOUT_OBJECT.ALL);
    class CONJUNCTION:
        ALL = {k for k in DICTIONARY.keys() if "conj" in DICTIONARY[k]};
        SINGULAR = {k for k in ALL if "sfp" in DICTIONARY[k]};
        PLURAL = {k for k in ALL if "psp" in DICTIONARY[k]};
    class PRONOUN:
        ALL = {k for k in DICTIONARY.keys() if "pron" in DICTIONARY[k]};
        SINGULAR = {k for k in ALL if "sfp" in DICTIONARY[k]};
        PLURAL = {k for k in ALL if "psp" in DICTIONARY[k]};
    class ADVERB:
        ALL = {k for k in DICTIONARY.keys() if "advb" in DICTIONARY[k]};
        SINGULAR = {k for k in ALL if "sfp" in DICTIONARY[k]};
        PLURAL = {k for k in ALL if "psp" in DICTIONARY[k]};
    class PREPOSITION: 
        ALL = {k for k in DICTIONARY.keys() if "prep" in DICTIONARY[k]};
        SINGULAR = {k for k in ALL if "sfp" in DICTIONARY[k]};
        PLURAL = {k for k in ALL if "psp" in DICTIONARY[k]};
    class INTERJECTION:
        ALL = {k for k in DICTIONARY.keys() if "intj" in DICTIONARY[k]};
        SINGULAR = {k for k in ALL if "sfp" in DICTIONARY[k]};
        PLURAL = {k for k in ALL if "psp" in DICTIONARY[k]};
    class ARTICLE:
        class DEFINITE:
            ALL = {k for k in DICTIONARY.keys() if "artl[d]" in DICTIONARY[k]};
            SINGULAR = {k for k in ALL if "sfp" in DICTIONARY[k]};
            PLURAL = {k for k in ALL if "psp" in DICTIONARY[k]};
        class INDEFINITE:
            ALL = {k for k in DICTIONARY.keys() if "artl[i]" in DICTIONARY[k]};
            SINGULAR = {k for k in ALL if "sfp" in DICTIONARY[k]};
            PLURAL = {k for k in ALL if "psp" in DICTIONARY[k]};
        ALL = set[str].union(DEFINITE.ALL, INDEFINITE.ALL);


if __name__ == "__main__":
    print(DICTIONARY);
    word_gen = word_generator(count = 5);
    try:
        while True:
            k = word_gen();
            v = InputWordTypes(k);
            DICTIONARY[k] = v;
            print(f"Added ({k}: {v}) to the dictionary");
    except StopIteration:
        pass
    print(DICTIONARY);
    j = input("Save to File (Y/N)?");
    if j == "Y":
        DICTIONARY.ExportJSON();
        print("File updated!");
    print("Exiting...");
