# Modmake file parser (py)

from enum import Enum
import re

def omit_comments_and_whitespace(txt: str) -> list[str]:
    lines = txt.splitlines();
    result = list();
    ignore = False;
    for line in lines:
        if (line.startswith("|||||")):
            if (ignore):
                ignore = False;
                continue;
            else:
                ignore = True;
        if (ignore or line.isspace() or line == ""): continue;
        result.append(line);
    return result;
    

class Token:    
    def __init__(self, input: str, result: str):
        self.input = input.strip();
        self.result = result.strip();
        
    def __repr__(self):
        return f"\"{self.input}\"=>\"{self.result}\"";

class Action:
    class Type(Enum):
        Item = 0,
        Armor = 1,
        Tool = 2,
        Block = 3,
        Locale = 4,
        ItemTag = 5,
        Craft = 6,
        Destroy = 7,
        Smelt = 8;

class Item:
    def __init__(self, name: str, quantity: int | tuple[int, int]):
        self.name = name;
        self.minQuantity = quantity if isinstance(quantity, int) else quantity[0];
        self.quantity = self.minQuantity;
        self.maxQuantity = quantity if isinstance(quantity, int) else quantity[1];
        
    def __repr__(self):
        return f"{{item:\"{self.name}\",quantity";
    
    def ingredient(self):
        return ""
    
def parse(token: Token):
    action, input = check_action(token.input);
    print(action, input);
    ...
    
def check_action(inp: str) -> tuple[Action.Type, str]:
    matches = re.match(r"[\w+]\[\w+\]", inp);
    if matches:
        rawAction = matches.group(0);
        rawInputs = matches.group(1);
        return (Action.Type(rawAction), rawInputs);
    raise ValueError(f"{inp} does not match format \"ActionName[Inputs]\"");


#print(Item("Iron Ingot", (2,7)));    


def tokenize_statements(statements: list[str]) -> list[Token]:
    tokens = list();
    for statement in statements:
        s = statement.split("->");
        if len(s) == 0: continue;
        input = s[0];
        result = "" if len(s) == 1 else s[1];
        tokens.append(Token(input, result));
    return tokens;

def recompile_tokens(tokens: list[Token]) -> str:
    result = "";
    for token in tokens:
        t = token.input;
        if token.result != "": 
            t += "->" + token.result;
        if result != "": 
            result += "\n" + t;
        else:
            result = t;
    return result;


with open("Minecraft Addition Ideas.modmake") as file:
    data = file.read();

w = omit_comments_and_whitespace(data);

print(w);
print();

t = tokenize_statements(w);

print(t);

print(recompile_tokens(t));

print(parse(t[0]));

