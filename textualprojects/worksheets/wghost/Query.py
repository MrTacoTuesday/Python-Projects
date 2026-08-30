from typing import Literal

if __name__ == "__main__":
    from Base import Mul, Num, Pow, Sum, Var, Expression
else:
    from wghost.Base import Mul, Num, Pow, Sum, Var, Expression


"""
class Query:
    Pattern = Literal["any", "all", "one"];
    Mode = Literal["#", "args", "repr", "var"];
    Vars = dict[str, "Query"];
    class Result:
        Vars = dict[Var, Expression];
        def __init__(self, matches: bool, result: Expression, vars: Vars = {}):
            self.matches = matches;
            self.result = result;
            self.vars = vars;
    
    @staticmethod
    def Or(*args, **kwargs) -> "Query": return Query(*args, pattern="one", **kwargs);
    @staticmethod
    def Exact(*args, **kwargs) -> "Query": return Query(*args, pattern="all", **kwargs);
    
    def __init__(self, *args, pattern: Pattern, mode: Mode|str = "#", type: type[Expression]|None = None, queryvars: Vars = {}) -> None:
        self.args = args;
        self.pattern = pattern;
        self.mode = mode;
        self.type = type;
        self.queryvars = queryvars;
        self.resultvars: Query.Result.Vars = {};
        
    def Match(self, expression: Expression, queryvars: Vars) -> Result:
        #if self.mode
        raise NotImplementedError;
"""


"""
SearchPattern_Quadratic = Query.Or(
    Query.Or( #
        # [a][x]^2 + ([b][x])? + ([c])? version
        Query.Exact(
            
            type=Sum
        ),
        Query.Exact(
            
            type=Mul
        ),
        "pow:*x,2"
    ),
    Query.Exact( # [a][x]^(2[u]) + ([b][x]^[u])? + ([c])? version
        
    ),
    queryvars={
        "pow:*x,2": Query.Exact(  # matches type:Pow, args[0]:{type:*}->$x
            # query [x]^2
            "*x", # Pow.args[0] matches this
            Query.Exact( # Pow.args[1] matches this
                # query 2
                "2",
                pattern="repr",
                type=Num
            ),
            mode="args",
            type=Pow
        ),
        "*x": Query.Exact( # anything matches this
            # query [x]
            "x",
            mode="var"
        ),
    }
);
"""

class ExpressionSearch():
    def __init__(self, base_pattern: Expression) -> None:
        self.pattern = base_pattern;
        self.vars = base_pattern.GetVars();
        pass
    ...


if __name__ == "__main__":
    Quadratic = Sum(Mul(Var("a"), Pow(Var("x"), Num(2))), Mul(Var("b"), Var("x")), Var("c"));
    

"""
Search could be in the form of input.Substitute({Exp(...):Var(...), ...}).FullyReduce() == raw_match_pattern;

so: 17n(x+5)^2+12(x+5)-88 -> exp
    17n -> a
    12 -> b
    -88 -> c
    x+5 -> x
... # implement search algorithm to guess these variables, keeping a dict of failed vars
e = exp.Substitute(17n: a, 12: b, -88: c, x+5: x).FullyReduce() # ax^2+bx+c
e == QuadraticExpression # ax^2+bx+c == ax^2+bx+c ? TRUE
"""

"""
{
    "Sum": { # searches for a Sum that matches these parameters
        "Mul": { # searches for a Mul that matches these parameters
            "Pow": { # has a Pow with these matches
                "Var": "$1", # Pow.base is any variable, identified as $1
                "Num": "2" # Num.__repr__() is exactly 2
            },
            "*": "$a" # everything else (*) is identified as $a; var a is returned now, substituting * for Var('a')
        },
        "Mul?": { # searches for a Mul that matches these parameters
            "Pow|Var": { # has either of these matches
                "Pow": { # has a Pow with these matches
                    "Var": "$1", # Pow.base is any variable, identified as $1
                    "Num": "1" # Num.__repr__() is exactly 1
                },
                "Var": "$1", # has a var, matching $1 or assigning to $1 if unassigned
            },
            "*": "$b" # everything else (*) is identified as $b; var b is returned now, substituting * for Var('b')
        },
        "Mul": {
            "Mul": { # searches for a Mul that matches these parameters
                "Pow?": { # matches a Pow if present, else ignores
                    "Var": "$1", # Pow.base is any variable, identified as $1
                    "Num": "0" # Num.__repr__() is exactly 0
                },
                "*": "$b" # everything else (*) is identified as $b; var b is returned now, substituting * for Var('b')
            }
        }
    }
}
"""
