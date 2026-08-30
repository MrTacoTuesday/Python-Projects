# The base structure of the system

import math
from typing import Callable, Literal, Protocol, runtime_checkable

from matplotlib.figure import Figure
from matplotlib.font_manager import FontProperties
from matplotlib.text import Text

if __name__ == "__main__":
    from FileHandler import ENSURE_TMP, TMP_FILE;
else:
    from wghost.FileHandler import ENSURE_TMP, TMP_FILE;

DEBUG_SORTKEY = False;

Substitutions = dict["Expression", "Expression"];

@runtime_checkable
class Expression(Protocol):

    def sign(self) -> Literal[-1,0,1,None]: ...;
    
    def order(self) -> int: ...;
    
    def __repr__(self) -> str: ...;
    
    def Substitute(self, o: Substitutions) -> "Expression": ...;
    
    def Approx(self, ndigits: int|None = None) -> "Expression": ...;
    
    def Reduce(self) -> "Expression": 
        return self;
    
    def FullyReduce(self) -> "Expression": 
        return self;
    
    def _sortkey(self) -> str: ...;
    
    def LaTeX(self, fontsize: float = 32) -> Figure:
        fig = Figure();
        fig.add_artist(Text(text="$"+self.__repr__()+"$", fontproperties=FontProperties(size=fontsize), parse_math=True));
        return fig;
    
    def GetVars(self) -> "list[Var]": ...
    
def SaveFigure(figure: Figure | Expression, filename: str) -> None:
    ENSURE_TMP();
    if isinstance(figure, Expression): figure = figure.LaTeX();
    figure.savefig(TMP_FILE(filename,"png"), bbox_inches='tight');
    figure.clear();
    del figure;

@runtime_checkable
class ListExpression(Expression, Protocol):
    args: list[Expression];
    
    def __init__(self, *args: Expression) -> None: 
        assert len(args) >= 2, self.__class__.__name__ + " must have at least two arguments";
        self.args = [];
        for arg in args:
            self.args.extend(arg.args) if isinstance(arg, self.__class__) else self.args.append(arg);
    
    def Approx(self, ndigits: int|None = None) -> Expression: 
        return self.__class__(*[arg.Approx(ndigits) for arg in self.args]);
                
    def Substitute(self, o: Substitutions) -> Expression:
        if self in o:
            return o[self];
        return self.__class__(*[arg.Substitute(o) for arg in self.args]);
    
    def _reverses_sort(self) -> bool: ...;
    
    def _sort(self) -> Expression:
        self.args = list(sorted(self.args, reverse=self._reverses_sort(), key=lambda a: a._sortkey()));
        return self;
    
    def GetVars(self) -> "list[Var]":
        _r = [];
        for arg in self.args:
            _r.extend(arg.GetVars());
        return _r;

class Num(Expression):
    
    def __init__(self, val: int | float) -> None:
        self.value = val;
        
    def order(self) -> int:
        return 0;
        
    def sign(self) -> None | Literal[-1,0,1]:
        if self.value < 0:
            return -1;
        elif self.value > 0:
            return 1;
        elif self.value == 0:
            return 0;
        return None;
    
    def abs(self) -> "Num":
        return Num(abs(self.value));
    
    @staticmethod
    def operate(method: "Callable[[int|float, int|float],int|float]", a: "Num", b: "Num") -> "Num":
        return Num(method(a.value, b.value));
    
    def __repr__(self) -> str: 
        if self.sign() is None:
            return "undefined";
        return self.value.__repr__();
        
    def Substitute(self, o: Substitutions) -> Expression: 
        if self in o:
            return o[self];
        return self;
    def Approx(self, ndigits: int|None = None) -> Expression: 
        if ndigits is not None:
            try:
                return Num(round(self.value, ndigits));
            except:
                pass
        return self;
    
    def _sortkey(self) -> str: 
        if DEBUG_SORTKEY: print("DEBUG:", "exn:", self, "_sortkey:", "0");
        return "0";
    
    def GetVars(self) -> "list[Var]":
        return [];

class Var(Expression):
    
    def __init__(self, s: str) -> None:
        self.name = s;
        
    def order(self) -> int:
        return 0;
        
    def sign(self) -> Literal[None]: return None;
    
    def __repr__(self) -> str: return self.name;
        
    def Substitute(self, o: Substitutions) -> "Expression":
        if self in o:
            return o[self];
        return self;
    def Approx(self, ndigits: int|None = None) -> Expression: 
        return self;
    
    def _sortkey(self) -> str: 
        if DEBUG_SORTKEY: print("DEBUG:", "exn:", self, "_sortkey:", self.name);
        return self.name;
    
    def GetVars(self) -> "list[Var]":
        return [self];
    
class Const(Var):
    def __init__(self, s: str, value: int|float) -> None:
        self.name = s;
        self.ToNum = lambda: Num(value);
    
    def order(self) -> int:
        return 0;
        
    def Substitute(self, o: Substitutions) -> "Expression":
        if self in o:
            return o[self];
        return self;
    
    def Approx(self, ndigits: int|None = None) -> Expression: 
        if ndigits is None:
            return self.ToNum();
        return self.ToNum().Approx(ndigits);
    
    def _sortkey(self) -> str:
        if DEBUG_SORTKEY: print("DEBUG:", "exn:", self, "_sortkey:", "0");
        return "0";
    
    def GetVars(self) -> "list[Var]":
        return [];
    
PI = Const("\\pi", math.pi);
TAU = Const("\\tau", math.tau);

class Negate(Expression):
    def __init__(self, e: Expression) -> None:
        self.expression = e;
    
    def order(self) -> int:
        return 1;
    
    def sign(self) -> None | Literal[-1] | Literal[0] | Literal[1]:
        s = self.expression.sign()
        if s is None:
            return -1;
        return s * -1;
        
    def Substitute(self, o: Substitutions) -> "Expression":
        if self in o:
            return o[self];
        return self.expression.Substitute(o);
    
    def Approx(self, ndigits: int|None = None) -> Expression: 
        return Negate(self.expression.Approx(ndigits));
    def Reduce(self) -> Expression: 
        if isinstance(self.expression, Num):
            return Num(-self.expression.value);
        elif isinstance(self.expression, Negate):
            return self.expression.expression;
        return Negate(self.expression.Reduce());
    def FullyReduce(self) -> Expression:
        e = self.expression.FullyReduce();
        if isinstance(e, Num):
            return Num(-e.value);
        elif isinstance(self.expression, Negate):
            return self.expression.expression;
        return Negate(e);

    def __repr__(self) -> str:
        if isinstance(self.expression, Num) and self.expression.sign() != -1 or isinstance(self.expression, Pow):
            return "-{}".format(self.expression);
        return "-({})".format(self.expression);
    
    def _sortkey(self) -> str:
        if DEBUG_SORTKEY: print("DEBUG:", "exn:", self, "_sortkey:", self.expression._sortkey());
        return self.expression._sortkey();
    
    def GetVars(self) -> "list[Var]":
        return self.expression.GetVars();

class Sum(ListExpression):
    
    def order(self) -> int: return 1;
            
    def sign(self) -> Literal[None]: return None;
    
    def __repr__(self) -> str:
        s = "";
        for i in range(len(self.args)):
            arg = self.args[i];
            if i == 0: 
                s += arg.__repr__();
            else:
                s += ("" if arg.sign() == -1 else "+") + arg.__repr__(); # ex:[12,-7,3] -> 12-7+3
        return s;
    
    def Reduce(self) -> Expression: 
        v = 0;
        args: list[Expression] = []
        for arg in self.args:
            if isinstance(arg, Num):
                v += arg.value;
            else:
                args.append(arg.Reduce());
        if len(args) == 0 or math.isnan(v):
            return Num(v);
        return Sum(*[Num(v), *args])._sort();
    
    def FullyReduce(self) -> Expression: 
        v = 0;
        args: list[Expression] = []
        for arg in self.args:
            a = arg.FullyReduce();
            if isinstance(a, Num):
                v += a.value;
            else:
                args.append(a);
        if len(args) == 0 or math.isnan(v):
            return Num(v);
        return Sum(*[Num(v), *args])._sort();
    
    def _reverses_sort(self) -> bool: return True;
    
    def _sortkey(self) -> str: return "+";
   
class Mul(ListExpression):
    
    def order(self) -> int:
        return 2;
            
    def sign(self) -> Literal[-1,1]:
        s = self.args[0].sign();
        if s is None or s == 0:
            return 1;
        return s;
    
    def __repr__(self) -> str:
        s = "";
        for i in range(len(self.args)):
            arg = self.args[i];
            if (i != 0 and isinstance(arg, Num)):
                s += "({})".format(arg);
            elif arg.order() == 0: 
                s += arg.__repr__();
            elif arg.order() <= self.order() or arg.sign() == -1:
                s += "({})".format(arg);
            else:
                s += arg.__repr__();
        return s;
    
    def Reduce(self) -> Expression: 
        v = 1;
        args: list[Expression] = []
        for arg in self.args:
            if isinstance(arg, Num):
                v *= arg.value;
            else:
                args.append(arg.Reduce());
        if v == 0 or math.isnan(v):
            return Num(0);
        elif len(args) == 0:
            return Num(v);
        elif len(args) == 1:
            if v == 1:
                return args[0];
            elif v == -1:
                return Negate(args[0]);
        if v==1:
            return Mul(*args)._sort();
        elif v==-1:
            return Negate(Mul(*args)._sort());
        return Mul(*[Num(v), *args])._sort();
    
    def FullyReduce(self) -> Expression: 
        v = 1;
        args: list[Expression] = []
        for arg in self.args:
            a = arg.FullyReduce();
            if isinstance(a, Num):
                v *= a.value;
            else:
                args.append(a);
        if v == 0 or math.isnan(v):
            return Num(0);
        elif len(args) == 0:
            return Num(v);
        elif len(args) == 1:
            if v == 1:
                return args[0];
            elif v == -1:
                return Negate(args[0]);
        if v==1:
            return Mul(*args)._sort();
        elif v==-1:
            return Negate(Mul(*args)._sort());
        return Mul(*[Num(v), *args])._sort();

    def _reverses_sort(self) -> bool: return False;

    def _sortkey(self) -> str: return max(*[a._sortkey() for a in self.args]);
    
class Pow(Expression):
    
    def __init__(self, base: Expression, exponent: Expression) -> None:
        self.base = base;
        self.exponent = exponent;
    
    def order(self) -> int:
        return 3;
            
    def sign(self) -> Literal[None]:
        return None;
    
    def __repr__(self) -> str:
        a,b = "", "";
        if self.base.order() == 0:
            a += "{}".format(self.base);
        else:
            a += "({})".format(self.base);
        if self.exponent.order() == 0:
            b += "{}".format(self.exponent);
        else:
            b += "{({})}".format(self.exponent);
        return a+"^"+b;
    
    def Approx(self, ndigits: int|None = None) -> Expression: 
        return Pow(self.base.Approx(ndigits), self.exponent.Approx(ndigits));
                
    def Substitute(self, o: Substitutions) -> "Expression":
        if self in o:
            return o[self];
        return Pow(self.base.Substitute(o), self.exponent.Substitute(o));
    
    def Reduce(self) -> Expression: 
        b,e = self.base, self.exponent;
        if isinstance(b, Num) and isinstance(e, Num):
            return Num(b.value ** e.value);
        if isinstance(b, Mul):
            return Mul(*[Pow(arg, e) for arg in b.args]);
        return Pow(b.Reduce(), e.Reduce()); 
    
    def FullyReduce(self) -> Expression: 
        b,e = self.base.FullyReduce(), self.exponent.FullyReduce();
        if isinstance(b, Num) and isinstance(e, Num):
            return Num(b.value ** e.value);
        if isinstance(b, Mul):
            return Mul(*[Pow(arg, e) for arg in b.args]);
        return Pow(b,e); 
    
    def _sortkey(self) -> str:
        if DEBUG_SORTKEY: print("DEBUG:", "exn:", self, "_sortkey:", "{}:{}".format(self.base._sortkey(), self.exponent._sortkey()));
        return "{}:{}".format(self.base._sortkey(), self.exponent._sortkey());

    def GetVars(self) -> "list[Var]":
        return self.base.GetVars() + self.exponent.GetVars();

if __name__ == "__main__":
    from random import randint;
    
    Quadratic = Sum(Mul(Var("a"), Pow(Var("x"), Num(2))), Mul(Var("b"), Var("x")), Var("c"));
    #Trinomial = Sum(Mul(Var("a"), Pow(Var("x"), Num(3))), Mul(Var("b"), Pow(Var("x"), Num(2))), Mul(Var("c"), Var("x")), Var("d"));
    
    #print(Trinomial.Substitute(a=Num(randint(-9,9)), b=Num(randint(-25,25)), c=Num(randint(-49,49)), d=Num(randint(-99,99))).FullyReduce());
    
    test = Quadratic;
    print(test);
    
    test = test.Substitute({
        Var("a"): Num(1),
        Var("b"): Num(4),
        Var("c"): Num(4)
    }).FullyReduce();
    SaveFigure(test, "test1");
    print(test);
    
    
    test = test.Substitute({Var("x"):Num(7)});
    SaveFigure(test, "test2a");
    print(test);
    
    test = test.Reduce();
    SaveFigure(test, "test2b");
    print(test);
    
    test = test.Reduce();
    SaveFigure(test, "test2c");
    print(test);
    
    
    test = Mul(Sum(Var("x"), Num(2)), Sum(Var("x"), Num(2))).FullyReduce();
    SaveFigure(test, "test3");
    print(test);