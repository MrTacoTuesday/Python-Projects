from math import nan
from os import listdir, remove
from typing import overload
from matplotlib.pyplot import figure;
from matplotlib.pyplot import close;
from random import randint

from genie import reduce_fractional_ratio

## SETUP
_TMP_DIR = "./obj/_tmp_old";
def CLEAR_TMP() -> None: 
    for i in listdir(_TMP_DIR): remove(_TMP_DIR + "/" + i);
CLEAR_TMP();

    
class Problem:
    def __init__(self, question: str, answer: str, notes: str = "") -> None:
        self.question = question;
        self.answer = answer;
        self.notes = notes;
    def make_latex_image_file(self, filename: str, key: bool = False) -> None:
        fig = figure();
        fig.text(0, 1, self.question, fontsize=20);
        if key:
            fig.set_figheight(fig.get_figheight() + 0.6 + 0.25*len(self.answer.splitlines()) + 0.12*len(self.notes.splitlines()));
            fig.text(0.05, 0.9, self.answer, fontsize=16);
            fig.text(0.1, 0.5, self.notes, fontsize=8);
        fig.savefig(f'{_TMP_DIR}/{filename}.png', bbox_inches='tight');
        close(fig);
class Fraction:
    def __init__(self, num: int, den: int) -> None:
        self.numerator = num;
        self.denominator = den;
    def reduce(self) -> "Fraction":
        return Fraction(*reduce_fractional_ratio(self.numerator, self.denominator));
    def abs(self) -> "Fraction":
        return Fraction(abs(self.numerator), abs(self.denominator));
    def resolve(self) -> float:
        if self.denominator == 0:
            return nan;
        return self.numerator/self.denominator;
    def inverted(self) -> "Fraction":
        return Fraction(self.denominator, self.numerator);
    @overload
    def __mul__(self, other: "int | Fraction") -> "Fraction":
        ...
    @overload
    def __mul__(self, other: float) -> float:
        ...
    def __mul__(self, other: "int|float|Fraction") -> "Fraction | float":
        if isinstance(other, float):
            return self.resolve() * other;
        elif isinstance(other, Fraction):
            return Fraction(self.numerator*other.numerator, self.denominator*other.denominator);
        return Fraction(self.numerator*other, self.denominator);
    @overload
    def __truediv__(self, other: "int | Fraction") -> "Fraction":
        ...
    @overload
    def __truediv__(self, other: float) -> float:
        ...
    def __truediv__(self, other: "int|float|Fraction") -> "Fraction | float":
        if isinstance(other, float):
            return self.resolve() / other;
        elif isinstance(other, Fraction):
            return Fraction(self.numerator*other.denominator, self.denominator*other.numerator);
        return Fraction(self.numerator*other, self.denominator);
    @overload
    def __rmul__(self, other: "int | Fraction") -> "Fraction":
        ...
    @overload
    def __rmul__(self, other: float) -> float:
        ...
    def __rmul__(self, other: "int|float|Fraction") -> "Fraction | float":
        if isinstance(other, float):
            return self.resolve() * other;
        elif isinstance(other, Fraction):
            return Fraction(self.numerator*other.numerator, self.denominator*other.denominator);
        return Fraction(self.numerator*other, self.denominator);
    @overload
    def __rtruediv__(self, other: "int | Fraction") -> "Fraction":
        ...
    @overload
    def __rtruediv__(self, other: float) -> float:
        ...
    def __rtruediv__(self, other: "int|float|Fraction") -> "Fraction | float":
        if isinstance(other, float):
            return self.resolve() / other;
        elif isinstance(other, Fraction):
            return Fraction(self.numerator*other.denominator, self.denominator*other.numerator);
        return Fraction(self.numerator*other, self.denominator);
    @overload
    def __add__(self, other: float) -> float:
        ...
    @overload
    def __add__(self, other: "int|Fraction") -> "Fraction":
        ...
    def __add__(self, other: "int|float|Fraction") -> "Fraction | float":
        if isinstance(other, float):
            return self.resolve() + other;
        elif isinstance(other, Fraction):
            return Fraction(self.numerator*other.denominator+self.denominator*other.numerator, self.denominator*other.denominator);
        return Fraction(self.numerator+other*self.denominator, self.denominator);
    @overload
    def __radd__(self, other: float) -> float:
        ...
    @overload
    def __radd__(self, other: "int|Fraction") -> "Fraction":
        ...
    def __radd__(self, other: "int|float|Fraction") -> "Fraction | float":
        if isinstance(other, float):
            return self.resolve() + other;
        elif isinstance(other, Fraction):
            return Fraction(self.numerator*other.denominator+self.denominator*other.numerator, self.denominator*other.denominator);
        return Fraction(self.numerator+other*self.denominator, self.denominator);
    def __repr__(self, resolves: bool = True) -> str:
        if resolves:
            if abs(self.denominator)==1:
                return str(self.numerator*self.denominator);
            elif self.numerator == 0:
                return "0";
            elif self.denominator == 0:
                return "\\text{undefined}";
        return f"{"-" if self.numerator*self.denominator<0 else ""}\\frac{{{abs(self.numerator)}}}{{{abs(self.denominator)}}}";
class Polynomial:
    def __init__(self, *args: int|float|Fraction, var: str = "x") -> None:
        self.args = tuple(args);
        self.var = var;
    def _repr_lead(self, o: int|float|Fraction, suffix: str = "") -> str:
        num = o.resolve() if isinstance(o, Fraction) else o;
        if num == 1:
            return suffix;
        elif num == -1:
            return "-"+suffix;
        elif num == nan:
            return "\\text{undefined}";
        return str(o)+suffix;
    def _repr_trail(self, o: int|float|Fraction, suffix: str = "") -> str:
        num = o.resolve() if isinstance(o, Fraction) else o;
        if num == 0:
            return "";
        elif num == 1 and suffix != "":
            return suffix;
        elif num == -1  and suffix != "":
            return "-"+suffix;
        elif num == nan:
            return "\\text{undefined}";
        return (f"+{num}" if num >= 0 else str(num)) + suffix;
    def _var_idx(self, i: int) -> str:
        k = len(self.args) - i - 1;
        if k == 0:
            return "";
        elif k == 1:
            return self.var;
        return f"{self.var}^{k}";
    def __repr__(self) -> str:
        return "".join([self._repr_lead(self.args[0], self._var_idx(0))]+[self._repr_trail(self.args[i], self._var_idx(i)) for i in range(1,len(self.args))]);
class Trinomial(Polynomial):
    def __init__(self, a: int|float|Fraction, b: int|float|Fraction, c: int|float|Fraction, var: str = "x") -> None:
        super().__init__(a, b, c, var=var);
class Binomial(Polynomial):
    def __init__(self, a: int | float | Fraction, b: int | float | Fraction, var: str = "x") -> None:
        super().__init__(a, b, var=var);
        self.a = a;
        self.b = b;
    @overload
    def __mul__(self, other: int | float | Fraction) -> "Binomial":
        ...
    @overload
    def __mul__(self, other: "Binomial") -> "Trinomial":
        ...
    def __mul__(self, other: "int | float | Fraction | Binomial") -> "Binomial | Trinomial":
        if isinstance(other, Binomial):
            return Trinomial(self.a * other.a, self.a*other.b+self.b*other.a, self.b*other.b);
        return Binomial(self.a * other, self.b * other);
    def solve(self) -> "SolutionSet":
        return SolutionSet(self.b/self.a);
    @staticmethod
    def generate(lead_bounds: tuple[int,int], trail_bounds: tuple[int,int], var: str = "x") -> "Binomial":
        return Binomial(randint(*lead_bounds), randint(*trail_bounds), var=var);
class SolutionSet(set[int|float|Fraction]):
    def __init__(self, *args: int|float|Fraction) -> None:
        super().__init__();
        self._add(*args);
    def _add(self, *args: int|float|Fraction) -> None:
        for i in args:
            if isinstance(i, Fraction) and i.resolve() != nan:
                self.add(i)
            elif i != nan:
                self.add(i);
    def reduce_fracs(self) -> "SolutionSet":
        return SolutionSet(*[_simplify_if_frac(i) for i in self]);
    def __repr__(self) -> str:
        if len(self) == 0:
            return "\\varnothing";
        elif len(self) == 1:
            return str(self.pop());
        else:
            return "\\{" + ",".join([str(i) for i in self]) + "\\}";
    @staticmethod
    def Union(*s: "SolutionSet") -> "SolutionSet": # type: ignore
        S = SolutionSet();
        for i in s:
            S._add(*i);

def _large_bounds(decimal: int = 2, negatives: bool = False) -> tuple[int, int]:
    return (-10**decimal+1 if negatives else int(10**(decimal-0.8)), 10**decimal-1);
def _gen_values(min: int, max: int) -> tuple[int, int]:
    return (randint(min, max), randint(min,max));
def _simplify_if_frac(num: int|float|Fraction) -> int|float|Fraction:
    if isinstance(num, Fraction):
        return num.reduce();
    return num;


class ProblemGenerator:
    @staticmethod
    def Addition(decimal_places: int = 2, negatives: bool = False) -> Problem:
        a,b = _gen_values(*_large_bounds(decimal_places, negatives));
        return Problem(f"${a}\\plus{b}$", f"${a+b}$", "Basic addition");
    @staticmethod
    def Subtraction(decimal_places: int = 2, negatives: bool = False) -> Problem:
        a,b = _gen_values(*_large_bounds(decimal_places, negatives));
        if (b>a and not negatives):
            a,b = b,a;
        return Problem(f"${a}\\minus{b}$", f"${a-b}$", "Basic subtraction");
    @staticmethod
    def Multiplication(negatives: bool = False) -> Problem:
        a,b = _gen_values(-12 if negatives else 0,12);
        return Problem(f"${a}\\cdot{b}$", f"${a*b}$", "Basic multiplication");
    @staticmethod
    def Division(negatives: bool = False) -> Problem:
        a,b = _gen_values(-12 if negatives else 0,12);
        return Problem(str(Fraction(a*b, b)), f"${a}$", "Basic division");
    @staticmethod
    def QuadraticSimple() -> Problem:
        x1,x2 = _gen_values(-12,12);
        a1,a2 = _gen_values(1,4);
        b1,b2 = Binomial.generate((1,4),(-12,12)), Binomial.generate((1,4),(-12,12));
        exn = b1*b2;
        f1,f2 = b1.solve(), b2.solve();
        F1,F2 = f1.reduce_fracs(), f2.reduce_fracs();
        S = SolutionSet.Union(f1,f2);
        notes = f"""This problem can be solved by setting $y$ to $0$ and factoring:
            Set $y=0$
            >   $0={exn}$
            Factor binomial
            >   $0=({b1})({b2})$
            Solve for x
            >   $0=({b1})$ and $0=({b2})$
            >   ${x1}={Binomial(a1,0)}$ and ${x2}={Binomial(a2,0)}$
            >   $x={f1}$ and $x={f2}$
            Reduce
            >   $x={F1}$ and $x={F2}$
            Write solution set
            >   $x={S}$
        """;
        del x1,x2,a1,a2,f1,f2,F1,F2;
        return Problem(f"$y={exn}$", f"$x={S}$", notes);

def run_test():
    for i in "abc":
        p = ProblemGenerator.QuadraticSimple()
        p.make_latex_image_file(i);
        p.make_latex_image_file(i+"_solution", True);

if __name__ == "__main__":
    run_test();
    ...
    print("FINISHED");