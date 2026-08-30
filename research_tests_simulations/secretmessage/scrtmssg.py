def f() -> str:
    with open("f.txt", "r") as f:
        l1 = f.readline().strip();
        l2 = f.readline().strip();
        s = f.read();
    assert l1.startswith("base=") and len(l1.split("="))==2, "Line 1: Expected format 'base=[integer]'";
    try:
        PARSE_BASE = int(l1.split("=")[1].strip());
    except ValueError:
        raise AssertionError("Line 1: expected format 'base=[integer]'");
    assert PARSE_BASE > 1, "Line 1: Value for 'base' must be greater than 1";
    assert l2.startswith("result=") and len(l2.split("="))==2, "Line 2: Expected format 'result=[integer]'";
    try:
        RESULT_BASE = int(l2.split("=")[1].strip());
    except ValueError:
        raise AssertionError("Line 2: expected format 'result=[integer]'");
    assert RESULT_BASE > 1, "Line 2: Value for 'result' must be greater than 1";
    try:
        val = mapstrtoint(PARSE_BASE, s);
    except ValueError:
        raise AssertionError(f"Line 3+: Expected data to be in base{PARSE_BASE}");
    return mapinttostr(RESULT_BASE, val);



BASES_TO_36 = list("0123456789abcdefghijklmnopqrstuvwxyz");
BASES_TO_64 = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/");
def mapinttostr(base: int, value: int) -> str:
    args = [];
    while value > 0:
        args.append(value % base);
        value //= base;
    args.reverse();
    if base <= 36:
        return "".join(map(BASES_TO_36.__getitem__, args));
    elif base <= 64:
        return "".join(map(BASES_TO_64.__getitem__, args));
    return "".join(map(chr, args));
def mapstrtoint(base: int, value: str) -> int:
    if base <= 36:
        args = [BASES_TO_36.index(arg) for arg in value.lower()];
    elif base <= 64:
        args = [BASES_TO_64.index(arg) for arg in value];
    else:
        args = [];
        for arg in value:
            i = ord(arg);
            assert i < base, f"Unexpected Character: {arg} for base {base}";
            args.append(i);
    i = 0;
    for arg in args:
        i *= base;
        i += arg;
    return i;

print(f());


    