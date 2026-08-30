# generates a string returning the name of an everyday object

from enum import Enum


class Style:
    @staticmethod
    def Bolden(a: str) -> str:
        return str(f"\33[1m{a}\33[0m");
    @staticmethod
    def Underline(a: str) -> str:
        return str(f"\33[2m{a}\33[0m");
    @staticmethod
    def Italicize(a: str) -> str:
        return str(f"\33[3m{a}\33[0m");
    @staticmethod 
    def ColorizeRGB(a: str, red: int, green: int, blue: int) -> str:
        return str(f"\33[38;2;{red};{green};{blue}m{a}\33[0m");
    @staticmethod
    def Colorize(a: str, color: "Color") -> str:
        return Style.ColorizeRGB(a, (color.value >> 16) % 256, (color.value >> 8) % 256, (color.value % 256));
    class Color(Enum):
        RED = 0xff0000;
        ORANGE = 0xffa500;
        YELLOW = 0xffff00;
        GREEN = 0x00ff00;
        BLUE = 0x0000ff;
        PURPLE = 0x800080;
        BROWN = 0xa52a2a;
        WHITE = 0xffffff;
        BLACK = 0x000000;
        GREY = 0x808080;
        CYAN = 0x00ffff;
        MAGENTA = 0xff00ff;

# load words from file 'Words.txt', separated by lines
with open("Words.txt") as _WORDS_FILE:
    _RAW_WORDS = _WORDS_FILE.read().splitlines();

WORDS = [Style.Bolden(word.upper()) for word in _RAW_WORDS];

COLOR = [Style.Colorize(color.lower(), Style.Color[color]) for color in Style.Color._member_names_];

HUE = [Style.Italicize(x) for x in (
    "light", "dark", "bright", "dull", "shiny", "sparkling"
)];

SHAPE = [
    "large", "small", "masssive", "tiny", "deformed", "perfect"
];


import random;
def get_shape(fail = 0.8)->list[str]:
    return ([] if random.random() < fail else [random.choice(SHAPE)]);
def get_color_hue(fail1 = 0.3, fail2 = 0.5)->list[str]:
    if (random.random() < fail1): return [];
    return ([] if random.random() < fail2 else [random.choice(HUE)]) + [random.choice(COLOR)];
def get_modified_word(fail1 = 0.8, fail2 = 0.3, fail3 = 0.5)->str:
    return " ".join([*get_shape(fail1), *get_color_hue(fail2, fail3), random.choice(WORDS)]);

for i in range(20):
    print(f"ITEM #{i+1}:\t\t{get_modified_word(0.6, 0.5, 0.4)}");