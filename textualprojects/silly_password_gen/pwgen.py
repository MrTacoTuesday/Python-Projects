# version 2
from functools import reduce
from random import random, choice, shuffle

WORDS: list[str] = []
with open('./data/google-10000-english-usa-no-swears.txt') as file:
    WORDS = file.read().splitlines()

SHARED_SYMBOLS = {'c': {'<'}, 'e': {'3', '='}, 'f': {'7'}, 'h': {'#'}, 'i': {'1', ':', '!'}, 'j': {';', '7'}, 'k': {'{'}, 'l': {'1', '|', '!'}, 'm': {'3'}, 'n': {'2'}, 'o': {'0'}, 'p': {'?', '7'}, 'q': {'9'}, 'r': {'7'}, 's': {'5', '$'}, 't': {'+', '7'}, 'u': {'<', '^', '>'}, 'v': {'<', '^', '>'}, 'w': {'3'}, 'x': {'%', '*'}, 'y': {'/', '7'}, 'z': {'%', '7'}}
UNIQUE_SYMBOLS = {'a': {'@'}, 'A': {'4'}, 'b': {'?', '>', '6'}, 'B': {'8'}, 'C': {'[', '('}, 'd': {'?', '<', '6'}, 'D': {'>', ')', ']', '7'}, 'e': {'9'}, 'E': {'{'}, 'f': {'&'}, 'g': {'9', '8', '&'}, 'G': {'6'}, 'h': {'2'}, 'i': {';', '.'}, 'I': {'|'}, 'j': {'/'}, 'n': {'^'}, 'Q': {'?'}}

def P(probability: float = 0.5) -> bool:
    return random() < probability
    
def generate_charmap() -> dict[str, str]:
    symbol_set = set()
    char_map = {}
    chars = list('abcdefghijklmnopqrstuvwxyz')
    shuffle(chars)
    for char in chars:
        
        lower_symbols = SHARED_SYMBOLS.get(char, set()).union(UNIQUE_SYMBOLS.get(char, set())).difference(symbol_set)
        upper_symbols = SHARED_SYMBOLS.get(char, set()).union(UNIQUE_SYMBOLS.get(char.upper(), set())).difference(symbol_set)
        #print("--  chrmap gen: chr:", char)
        #print("--  chrmap gen: lower_symbols:", lower_symbols)
        #print("--  chrmap gen: upper_symbols:", upper_symbols)
        
        
        if len(lower_symbols):
            symbol = choice(list(lower_symbols))
            symbol_set.add(symbol)
            char_map[char] = symbol
        else:
            char_map[char] = char
            
        if len(upper_symbols):
            symbol = choice(list(upper_symbols))
            symbol_set.add(symbol)
            char_map[char.upper()] = symbol
        else:
            char_map[char.upper()] = char.upper()
            
    return char_map

def charswap(char: str, map: dict[str,str]) -> str:
    if P(0.5):
        return map.get(char, char)
    return char
    

class Word:
    def __init__(self, word: str):
        self.word = word.capitalize()
        
    @property
    def charlength(self) -> int:
        return len(self.word)
    
    def randomized(self, map: dict[str,str] = {}) -> str:
        return reduce(lambda a,b: a + charswap(b, map), self.word)
    
class WordSet(list[Word]):
    
    def __init__(self, character_map: dict[str,str] | None = None) -> None:
        self.map = character_map or generate_charmap()
        self.generation: str = ""
        
    @property
    def charlength(self) -> int:
        return reduce(lambda a,b: a + b.charlength, self, 0)
    
    @property
    def words(self) -> int:
        return len(self)
        
    def __repr__(self) -> str:
        result = ""
        for modifier in self:
            result += modifier.__repr__()
        return result

    def new_charmap(self) -> None:
        self.map = generate_charmap()
    
    def randomize(self, new_mapping: bool = False) -> str:
        if new_mapping:
            self.map = generate_charmap()
        self.generation = ""
        for modifier in self:
            self.generation += modifier.randomized(self.map)
        return self.generation
    
    def __str__(self) -> str:
        return self.generation if len(self.generation) else self.randomize()
        
    @staticmethod
    def Generate(min_words: int = 1, word_size: range = range(8,21)) -> "WordSet":
        ws = WordSet()
        while ws.charlength <= word_size.start or ws.words < min_words:
            
            word = choice(WORDS)
            while ws.charlength + len(word) > word_size.stop:
                word = choice(WORDS)
            if ws.charlength  + len(word) > word_size.stop and ws.words + 1 < min_words:
                del ws[0]
            ws.append(Word(word))
        return ws
    
ws = WordSet.Generate(1, range(8, 21))
print("Original:",ws.__repr__())
print("Gen 1:",ws.randomize())
print("Gen 2:",ws.randomize())
ws.new_charmap();
print("Gen 3:",ws.randomize(True))
print("Gen 4:",ws.randomize())