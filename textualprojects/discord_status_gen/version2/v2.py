from random import choice, choices, randint, random
from typing import Callable, Literal, Never, TypeVar;

## UTILS ##
if True:

    class OPTIONS:
        DEBUG: bool = False;
        
        @staticmethod
        def SetDebugMode() -> None:
            OPTIONS.DEBUG = True;
            
    def Debug(scope: str, item: str, value: object) -> None:
        if OPTIONS.DEBUG:
            print(f"\33[38;2;158;0;0m\33[1mDEBUG::\33[0m \33[2m{scope}:{item} {repr(value)}\33[0m");
    
    _T = TypeVar("_T");
    def DebugResult(scope: str, value: _T) -> _T:
        Debug(scope, "result", value);
        return value;
    
    def DebugError(scope: str, error: Exception) -> Never:
        if OPTIONS.DEBUG:
            print(f"\33[38;2;158;0;0m\33[1mDEBUG:: ERROR\33[0m \33[2m{scope}:\33[0m\n{repr(error)}");
        raise error;

    def load_nlsv(file_name: str) -> list[str]:
        with open(file_name, "r") as f:
            return f.read().splitlines();

    def test_fx_out(func: Callable|str):
        if isinstance(func, str):
            func_desc = str(func);
            func_code = compile(func, __file__, "eval");
            func = lambda: eval(func_code);
        else:
            func_desc = func.__name__;
            
        print(f"Testing function '{func_desc}' (press ENTER for next run or type and enter anything to exit)");
        i = 1;
        while input(f"run {i} > {func()} <") == "":
            i += 1;

    def ordered_list(items: list[str], oxford_comma: bool = False) -> str:
        """examples: 
        \nordered_list(["this","that","the other"], False) == "this, that and the other";
        \nordered_list(["this","that","the other"], True) == "this, that, and the other";""";
        if len(items) == 0: 
            return "";
        elif len(items) == 1:
            return items[0];
        if oxford_comma:
            _1 = items[-1];
            return ", ".join(items).replace(f", {_1}", f", and {_1}");
        else:
            _1 = items.pop();
        return f"{", ".join(items)} and {_1}";

    def adjective_list(items: list[str]) -> str:
        """examples: 
        \nadjective_list(["slimy","green"], False) == "slimy, green";
        \nadjective_list(["sticky","slimy","green"]) == "sticky, slimy, green";""";
        if len(items) == 0: 
            return "";
        return ", ".join(items);

    def scaled_randint(min: int, max: int, scale: float = 0.75) -> int:
        """conditions:
        - min < max, 
        - scale in (-1,1) else scale = 1-1/scale, default is 0.75 or 'the next option is 25% less likely than the last one'
        - scales of -1, 0, or 1 give the same result as random.randint(min,max) 
        \nreturns: 
        - a random number between min and max, inclusive
        - if scale > 0, gives greater weight to values of lesser magnitude
        - if scale < 0 gives greater weight to values of greater magnitude"""
        if min > max:
            DebugError("scaled_randint", ValueError("parameter 'min' must be less than 'max'"));
        elif min == max:
            return min;
        if scale == 0 or abs(scale) == 1:
            return randint(min,max);
        elif abs(scale) > 1:
            scale = 1-1/scale;
        Debug("scaled_randint","range-scale",(min,max));
        Debug("scaled_randint","scale",scale);
        #raise NotImplementedError("The 'scale' feature has not been implemented yet");
        """if min < 0 and max > 0:
            weights = [scale**abs(i) for i in range(min,0,-1)] + [scale**i for i in range(0, max+1)];
        else:
            ..."""
        #_ = 0 if min < 0 and max > 0 else (1 if min + max > 0 else -1) * (1 if scale > 0 else -1);
        _ = (1 if min + max > 0 else -1) * (1 if scale > 0 else -1);
        Debug("scaled_randint","_",_);
        anchor = 0 if _ == 0 else (max if _ == 1 else min);
        Debug("scaled_randint","anchor",anchor);
        weights = [(1/abs(scale))**abs(abs(i)-abs(anchor)) for i in range(min,max+1)];
        Debug("scaled_randint","weights",weights);
        return DebugResult("scaled_randint", choices(range(min,max+1), weights)[0]);
    

## SETUP ##

COLORS = load_nlsv("colors.list");
COLOR_MODIFIERS = load_nlsv("color_modifiers.list");
ADJECTIVES = load_nlsv("adjectives.list");

def g_color(simple: bool = False) -> str:
    color = choice(COLORS);
    Debug("g_color","initial-selection",color);
    if not simple: 
        if random() < 0.2:
            Debug("g_color", "dashed", True);
            _c = [i for i in COLORS];
            _c.remove(color);
            color += "-"+choice(_c);
        else: Debug("g_color", "dashed", False);
        if random() < 0.4:
            Debug("g_color", "modified", True);
            return DebugResult("g_color", f"{choice(COLOR_MODIFIERS)} {color}");
        else: Debug("g_color", "modified", False);
    return DebugResult("g_color", color);

def g_adjective(max_count: int = 3, style: Literal["al", "ol"] = "al") -> str:
    Debug("g_adjective","style",style);
    adjectives = choices(ADJECTIVES,k=scaled_randint(1, max_count));
    Debug("g_adjective","items",adjectives);
    if style == "al":
        return DebugResult("g_adjective", adjective_list(adjectives));
    elif style == "ol":
        return DebugResult("g_adjective", ordered_list(adjectives));
    DebugError("g_adjective", ValueError("Expected parameter 'style' to be either 'al' or 'ol'"));

def g_any_adjective(color_chance: float = 0.1, max: int = 3) -> str:
    if random() < color_chance:
        Debug("g_any_adjective", "choice", "Descriptive Color");
        return DebugResult("g_any_adjective", g_color());
    else:
        Debug("g_any_adjective", "choice", "Adjective List");
        return DebugResult("g_any_adjective", g_adjective(max));
        


## TESTING ##   
#OPTIONS.SetDebugMode();

test_fx_out(g_color);
test_fx_out("g_any_adjective(max=4)");

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