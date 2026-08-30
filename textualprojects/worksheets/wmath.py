import math
from typing import Literal, Self, overload
from genie import approx_to_fractional_ratio

    
class Expression:
    
    @property
    def level(self) -> int:
        raise NotImplementedError;
    
    def Solve(self) -> "Solution":
        if isinstance(self, Solution):
            return self;
        elif self.CanStep():
            s = self.SolutionStep();
            return s.Solve();
        raise ValueError(f"Unsolvable Expression: {self}");
        
    def SolutionStep(self) -> "Expression":
        raise NotImplementedError;
    
    def CanStep(self) -> bool:
        raise NotImplementedError;
    
    def Substitute(self, **varargs: "Expression") -> "Expression":
        raise NotImplementedError;
        
    def __repr__(self) -> str:
        raise NotImplementedError;
    
    def __nestedrepr__(self, nester: "Expression") -> str:
        if self.level < nester.level or (self.level == nester.level and not isinstance(self, nester.__class__)):
            return "({})".format(self);
        return self.__repr__();


class Solution(Expression):
    
    @property
    def level(self) -> Literal[0]: return 0;
    def Solve(self) -> "Solution": return self;
    def SolutionStep(self) -> Expression: return self;
    def CanStep(self) -> Literal[False]: return False;
    def Substitute(self, **varargs: Expression) -> Expression: return self;
    def is_numeric(self) -> bool: return False;
    
    def __nestedrepr__(self, nester: Expression) -> str:
        if isinstance(self, Numeric) and self.is_negative():
            return "({})".format(self);
        else:
            return self.__repr__();


class Numeric(Solution):

    def is_numeric(self) -> Literal[True]: return True;

    def is_natural(self) -> bool: raise NotImplementedError;
    def is_whole(self) -> bool: raise NotImplementedError;
    def is_integer(self) -> bool: raise NotImplementedError;
    
    def is_rational(self) -> bool: raise NotImplementedError;
    def is_irrational(self) -> bool: raise NotImplementedError;
        
    def is_real(self) -> bool: raise NotImplementedError;
    def is_imaginary(self) -> bool: raise NotImplementedError;
    
    def is_finite(self) -> bool: raise NotImplementedError;
    def is_infinite(self) -> bool: raise NotImplementedError;
    def is_undefined(self) -> bool: raise NotImplementedError;
    
    def is_positive(self) -> bool: raise NotImplementedError;
    def is_negative(self) -> bool: raise NotImplementedError;
    def is_zero(self) -> bool: raise NotImplementedError;

        
class Operation(Expression):
    
    def __operate__(self) -> Solution: raise NotImplementedError;

 
class UnaryOperation(Operation):
    def __init__(self, e: Expression) -> None:
        super().__init__();
        self.expression = e;
        
    def SolutionStep(self) -> Expression:
        if self.expression.CanStep():
            return self.__class__(self.expression.SolutionStep());
        elif isinstance(self.expression, Solution):
            return self.__operate__();
        raise;
    
    def CanStep(self) -> bool:
        return self.expression.CanStep() or isinstance(self.expression, Solution);
    
    def Substitute(self, **varargs: Solution | Expression) -> Expression:
        return self.__class__(self.expression.Substitute(**varargs));


class BinaryOperation(Operation):
    def __init__(self, lhs: Expression, rhs: Expression) -> None:
        super().__init__();
        self.lhs = lhs;
        self.rhs = rhs;
        
    def SolutionStep(self) -> Expression:
        if self.lhs.CanStep():
            return self.__class__(self.lhs.SolutionStep(), self.rhs);
        elif self.rhs.CanStep():
            return self.__class__(self.lhs, self.rhs.SolutionStep());
        elif isinstance(self.lhs, Solution) and isinstance(self.rhs, Solution):
            return self.__operate__();
        raise;
        
    def CanStep(self) -> bool:
        return self.lhs.CanStep() or self.rhs.CanStep() or (isinstance(self.lhs, Solution) and isinstance(self.rhs, Solution));
    
    def Substitute(self, **varargs: Solution | Expression) -> Expression:
        return self.__class__(self.lhs.Substitute(**varargs), self.rhs.Substitute(**varargs));


class Operations:
    class Add(BinaryOperation):
        
        @property
        def level(self) -> Literal[1]: return 1; # 4(paren) 3(exp/func) 2(mul/div) 1(add/sub) 0(value)
            
        def __repr__(self) -> str:
            # -32+44
            # 14+29
            # 99-88*3
            # 13+(-12)
            # Mul(
            #   Sub(Var("x"), 1),
            #   Add(Var("x"), 1)
            # )
            # -> (x-1)*(x+1)
            
            return f"{self.lhs.__nestedrepr__(self)}+{self.rhs.__nestedrepr__(self)}";
        
        def __operate__(self) -> Solution:
            if isinstance(self.lhs, Real) and isinstance(self.rhs, Real):
                return self.lhs.Add(self.rhs);
            ... # Solution.Add(self.lhs,self.rhs);
            return super().__operate__();
        
    class Subtract(BinaryOperation):
        
        @property
        def level(self) -> Literal[1]: return 1; # 4(paren) 3(exp/func) 2(mul/div) 1(add/sub) 0(value)
            
        def __repr__(self) -> str:
            return f"{self.lhs.__nestedrepr__(self)}-{self.rhs.__nestedrepr__(self)}";
        
        def __operate__(self) -> Solution:
            if isinstance(self.lhs, Real) and isinstance(self.rhs, Real):
                return self.lhs.Subtract(self.rhs);
            ... # Solution.Add(self.lhs,self.rhs);
            return super().__operate__();
        
    class Divide(BinaryOperation):
        
        @property
        def level(self) -> Literal[2]: return 2; # 4(paren) 3(exp/func) 2(mul/div) 1(add/sub) 0(value)
        
        def __init__(self, numerator: Expression, denominator: Expression) -> None:
            super().__init__(numerator, denominator);
            
        def __repr__(self) -> str:
            return f"\\frac{{{self.lhs}}}{{{self.rhs}}}";

        def __operate__(self) -> Solution:
            if isinstance(self.lhs, Real) and isinstance(self.rhs, Real):
                return self.lhs.Divide(self.rhs);
            ... # Solution.Divide(self.lhs,self.rhs);
            return super().__operate__();
        


"""
16x^2+\\ln{\\frac{33}{18x}}

expression = Operation.Add(Operation.Mult(Integer(16),Operation.Pow(Variable("x"), Integer(2)), Operation.Ln(Fraction(Integer(33),Operation.Mult(Integer(18),Variable("x")))))
expression.substitute(x=4) # -> "16*4^2+\\ln{\\frac{33}{18*4}}"
"""

# TODO: Number base type has INF, UNDEF; Real(Number) has value, PI, TAU, ZERO, ONE; Frac(Real) has num/denom with calced value

class Real(Numeric):
    def __init_subclass__(cls, /) -> None:
        cls.ZERO = cls(0);
        cls.ONE = cls(1);
        cls.__N1 = cls(-1);
        cls.PI = cls(math.pi, _irrational_flag = True);
        cls.INFINITY = cls(math.inf);
        cls.NEGINFINITY = cls(-math.inf);
        cls.UNDEFINED = cls(math.nan);
        cls.TAU = cls(math.tau, _irrational_flag = True);
        return super().__init_subclass__();
    @overload
    def __init__(self, value: int, /) -> None: ...
    @overload
    def __init__(self, value: float, /) -> None: ...
    @overload
    def __init__(self, value: None = None, /) -> None: ...
    @overload
    def __init__(self, value: float, /, _irrational_flag: bool) -> None: ...
    def __init__(self, value: int|float|None = None, _irrational_flag: bool = False) -> None: 
        self.__undefined = value is None or math.isnan(value);
        self.__infinite = math.isinf(value or 0);
        self.value = math.nan if value is None else float(value);
        self.__irrational = _irrational_flag and not (self.__undefined or self.__infinite or self.value.is_integer());
    
    def __repr__(self) -> str:
        if self.__undefined:
            return "undefined";
        elif self.__infinite:
            return "-∞" if self.value < 0 else "∞";
        elif self.__irrational:
            return str(self.value)+"…";
        elif self.value.is_integer():
            return str(int(self.value));
        return str(self.value);
    
    @property
    def as_fraction(self, /) -> Operations.Divide:
        if self.__undefined:
            return Operations.Divide(self.UNDEFINED, self.ZERO);
        if self.__infinite:
            return Operations.Divide(self.__class__(self.value), self.ZERO);
        f = approx_to_fractional_ratio(self.value);
        return Operations.Divide(self.__class__(f[0]), self.__class__(f[1]));
    
    @property
    def numerator(self, /) -> Self:
        if self.__undefined:
            return self.UNDEFINED;
        elif self.__infinite:
            return self.__class__(self.value);
        return self.__class__(approx_to_fractional_ratio(self.value)[1]);
    
    @property
    def denominator(self, /) -> Self:
        if self.__undefined:
            return self.ZERO;
        elif self.__infinite:
            return self.ONE;
        return self.__class__(approx_to_fractional_ratio(self.value)[1]);
    
    @property
    def sign(self, /) -> Self:
        if self.is_undefined():
            return self.UNDEFINED;
        if self.value > 0:
            return self.ONE;
        elif self.value < 0:
            return self.__N1;
        return self.ZERO;
    
    def is_natural(self) -> bool: 
        return self.value.is_integer() and self.value >= 1;
    def is_whole(self) -> bool: 
        return self.value.is_integer() and self.value >= 0;
    def is_integer(self) -> bool:
        return self.value.is_integer();
    
    def is_rational(self) -> bool:
        return not self.__irrational;
    def is_irrational(self) -> bool:
        return self.__irrational;
    
    def is_real(self) -> bool:
        return not self.__undefined;
    def is_imaginary(self) -> bool:
        return False;
    
    def is_finite(self) -> bool: return not self.__infinite;
    def is_infinite(self) -> bool: return self.__infinite;
    def is_undefined(self) -> bool: return self.__undefined;
    
    def is_positive(self) -> bool: return not self.__undefined and self.value > 0;
    def is_negative(self) -> bool: return not self.__undefined and self.value < 0;
    def is_zero(self) -> bool: return not self.__undefined and self.value == 0;
    
    def Add(self, other: Self, /) -> Self: 
        if self.__undefined or other.__undefined:
            return self.UNDEFINED;
        elif self.__infinite and other.__infinite:
                return self.UNDEFINED;
        elif self.__infinite:
            return self.Posit();
        elif other.__infinite:
            return other.Posit();
        return self.__class__(self.value + other.value, _irrational_flag = self.__irrational or other.__irrational);
        
    def Subtract(self, other: Self, /) -> Self: 
        if self.__undefined or other.__undefined:
            return self.UNDEFINED;
        elif self.__infinite and other.__infinite:
                return self.UNDEFINED;
        elif self.__infinite:
            return self.Posit();
        elif other.__infinite:
            return other.Posit();
        return self.__class__(self.value - other.value, _irrational_flag = self.__irrational or other.__irrational);
    
    def Negate(self) -> Self: 
        if self.__undefined:
            return self.UNDEFINED;
        return self.__class__(-self.value, _irrational_flag = self.__irrational);
    
    def Posit(self) -> Self: 
        if self.__undefined:
            return self.UNDEFINED;
        return self.__class__(self.value, _irrational_flag = self.__irrational);
    
    def Multiply(self, other: Self, /) -> Self: 
        if self.__undefined or other.__undefined:
            return self.UNDEFINED;
        if self.__infinite or other.__infinite:
            return self.INFINITY if (self.value < 0 or other.value < 0) else self.NEGINFINITY;
        return self.__class__(self.value*other.value, _irrational_flag = self.__irrational or other.__irrational);
        
    def Divide(self, other: Self, /) -> Self:
        if self.__undefined or other.__undefined:
            return self.UNDEFINED;
        elif self.__infinite and other.__infinite:
            return self.UNDEFINED;
        elif other.__infinite:
            return self.ZERO;
        elif self.__infinite:
            return self.Posit();
        elif other.is_zero():
            return self.UNDEFINED;
        return self.__class__(self.value/other.value, _irrational_flag = self.__irrational or other.__irrational);
        ...
    
    
    """
    def __floordiv__(self, value: Self, /) -> Self: ...
    def __truediv__(self, value: Self, /) -> Self: ...
    def __mod__(self, value: Self, /) -> Self: ...
    def __divmod__(self, value: Self, /) -> tuple[Self, Self]: ...
    def __pow__(self, value: Self, /) -> Self: ...
    def __radd__(self, value: Self, /) -> Self: ...
    def __rsub__(self, value: Self, /) -> Self: ...
    def __rmul__(self, value: Self, /) -> Self: ...
    def __rfloordiv__(self, value: Self, /) -> Self: ...
    def __rtruediv__(self, value: Self, /) -> Self: ...
    def __rmod__(self, value: Self, /) -> Self: ...
    def __rdivmod__(self, value: Self, /) -> tuple[Self, Self]: ...
    def __getnewargs__(self) -> tuple[Self]: ...
    def __trunc__(self) -> int: ...
    def __ceil__(self) -> int: ...
    def __floor__(self) -> int: ...
    def __round__(self, ndigits: int | None = None, /) -> Self: ...
    def __eq__(self, value: object, /) -> bool: ...
    def __ne__(self, value: object, /) -> bool: ...
    def __lt__(self, value: Self, /) -> bool: ...
    def __le__(self, value: Self, /) -> bool: ...
    def __gt__(self, value: Self, /) -> bool: ...
    def __ge__(self, value: Self, /) -> bool: ...
    def __int__(self) -> int: ...
    def __float__(self) -> Self: ...
    def __abs__(self) -> Self: ...
    def __hash__(self) -> int: ...
    def __bool__(self) -> bool: ..."""

Real.__init_subclass__();

if __name__ == "__main__":
    from random import randint, random, choice

    OPERATIONS = BinaryOperation.__subclasses__() + UnaryOperation.__subclasses__();
    
    def generate(nodes: int|None = None, mode: Literal["int", "real", "imag", "mixed"] = "int") -> Expression:
        assert nodes is None or nodes >= 0, "Nodes must be greater than or equal to zero";
        assert mode in ("int", "real", "imag", "mixed"), "Mode must either be 'int', 'real', 'imag', or 'mixed'";
        nodes = randint(1,5) if nodes is None else nodes;
        if nodes == 0:
            if mode == "int" or (mode == "mixed" and random() < 0.5): # TODO: change to 0.333 once Imag has been implemented
                return Real(randint(-99,99));
            elif mode == "real" or (mode == "mixed" and random() < 1): # TODO: change to 0.5 once Imag has been implemented
                return Real(randint(-9999,9999)/100);
            else:
                ... # TODO: implement Imag
                raise NotImplementedError;
        
        nodes -= 1;
        operation = choice(OPERATIONS);
        if issubclass(operation, BinaryOperation): # TODO?: add other choices like Ternary and such eventually
            n = randint(0, nodes);
            return operation(generate(n, mode), generate(nodes - n, mode));
        elif issubclass(operation, UnaryOperation):
            return operation(generate(nodes, mode));
        raise NotImplementedError;

    exp = generate();
    print(exp);
    print();
    while exp.CanStep():
        exp = exp.SolutionStep();
        print(exp);
        
