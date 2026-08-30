from functools import reduce
import random
import zipfile


input = "Hello, My name is Weston. I'm 18 years old.";
I = ascii(input).strip("\"'");

L = [ord(_) for _ in I];

print(I);
print(L);


"""a = reduce(lambda x,y: x+y, [chr(0x11000 - i - 1) for i in L]);
print(a);

b = [ord(_) for _ in a];
print(b);

c = [0x11000 - _ - 1 for _ in b];
print(c);"""


def transform_code(code: int, position: int, offset: int) -> str:
    k = (code**2 + position**2 )**2 + offset;
    return hex(k).removeprefix("0x");
    ...
    
def transform(text: str, offset: int) -> str:
    L = [ord(_) for _ in ascii(input).strip("\"'")];
    _r = ""
    for i in range(len(L)):
        k = transform_code(L[i], i, offset);
        if len(k) < 8:
            _r += "0"*(8-len(k));
        _r += k;
    return _r;
        

o = random.randint(-16**5,16**5);
"""print(f"o={o}");

R = [transform(L[i], i, o) for i in range(len(L))];

G = "ghijklmnopqrstuvwxyz";
print(reduce(lambda x,y: x + random.choice(G) + y, R));"""

t = transform(input,o);

print(t);
print(bytes.fromhex(t));
with zipfile.ZipFile("contents.zip", "w") as zf:
    zf.writestr("Message", bytes.fromhex(t));
