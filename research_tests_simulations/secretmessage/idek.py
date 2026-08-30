from typing import Any


def __enter__(*args: str):
    Args = [parse(arg) for arg in args];
    if isinstance(Args[0], str):
       ... 
    ...
    
def parse(s: str) -> Any:
    try:
        return eval(s, {});
    except:
        return s;

class cipher():
    def __init__(self, ignore_case: bool = False) -> None:
        self.__map: dict[str, str] = {};
        self.__flag = ignore_case;
        
    def add(self, a: str, b: str) -> None:
        if self.__flag:
            self.__map[a.lower()] = b.lower();
        else:
            self.__map[a] = b;
    
    def to_file(self, filename: str) -> None:
        with open(filename+".why", "w") as f:
            for k,v in self.__map.items():
                f.write(f"{k}{v}");
        ...
        
    def parse_file(self, filename: str) -> None:
        ...


a = cipher();
s = 45;
for i in range(256):
    a.add(chr(i), chr(i+s));
a.to_file("ciphers/a")

if __name__ == "__main__":
    import sys;
    __enter__(*sys.argv);