# generate programming logic problems to work out by hand (in C#)


## BOOLEAN LOGIC

import math
from sys import stdout
from time import sleep
from random import randint, random, choice

def generate_bool(vars: list[str] = ["true","false"], nodes_left:int = -1, last_node="") -> str:
    """generates a C# boolean expression using basic operations
    should get result like: \"false || (true && !false)\""""
    if nodes_left == -1: 
        nodes_left = randint(2,8);
    if last_node == "":
        last_node = choice(vars);
        nodes_left -= 1;
    if nodes_left == 0: 
        return last_node;
    n = randint(1,nodes_left);
    p = nodes_left - n;
    side = random() < 0.5;
    new_node = last_node
    while new_node == last_node:
        new_node = choice(vars) if n == 0 else generate_bool(vars, n);
    L = last_node if not side else new_node;
    if L not in vars: L = f"({L})";
    R = last_node if side else new_node;
    if R not in vars: R = f"({R})";
    if random() < 0.125:
        L = f"!{L}";
    if random() < 0.125:
        R = f"!{R}";
    last_node = choice([" && "," || "]).join((L,R));
    return generate_bool(vars, p, last_node);

def ask_boolean_test_question(vars: dict[str,bool] | None = None, nodes: int = -1) -> bool:
    """generates a C# boolean expression using the provided variables or literals if variables were not provided
    it then proceeds to ask the user to solve it and checks the answer, returning true if the answer was correct"""
    csharp_exp = generate_bool(["true","false"] if vars is None else list(vars.keys()), nodes);
    py_exp = csharp_exp.replace("&&","and").replace("||","or").replace("!","not ");
    msg = "";
    if vars is not None:
        msg += "Given that:\n";
        for (k,v) in vars.items():
            vv = "true" if v else "false";
            py_exp = py_exp.replace(k,vv);
            msg += f"\tbool {k} = {vv};\n";
    py_exp = py_exp.replace("true","True").replace("false","False");
    msg += f"Evaluate the boolean expression:\n\t{csharp_exp};\n";
    answer = "true" if eval(py_exp) else "false";
    print(msg);
    _ans = input(">>> ");
    if _ans == answer:
        print("Correct!");
    elif _ans != answer:
        print("Incorrect!",end="");
        if _ans.lower() == answer:
            print(f"Make sure to use valid syntax: '{answer}'",end="");
        print()
    return _ans == answer;

def generate_boolean_var_dict(count: int, names: list[str] = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")) -> dict[str,bool]:
    """generates a dictionary mapping of variable names to boolean values"""
    _res = {};
    for i in range(count):
        _res[names[i]] = random() < 0.5;
    return _res;

def generate_boolean_test_question(difficulty:int) -> bool:
    """asks the user to solve a boolean expression given a specific difficulty level to generate
    returns true if the question was answered correctly"""
    nodes = max(2,int(1.5 * difficulty ** 0.777));
    if random() < 0.777 ** max(1, difficulty / 3):
        return ask_boolean_test_question(None, nodes);
    else:
        c = max(2, 2 + int(math.log(randint(1,difficulty**2))));
        return ask_boolean_test_question(generate_boolean_var_dict(c), nodes);
    
def delete_last_line():
    "Deletes the last line in the STDOUT";
    # cursor up one line
    stdout.write('\x1b[1A');
    # delete last line
    stdout.write('\x1b[2K');
    
def announce_grade(grade: float):
    """announces a percentage grade and provides \"encouragement\""""
    letter = ""
    match int(grade * 10):
        case 10,9:
            letter += "A";
        case 8:
            letter += "B";
        case 7:
            letter += "C";
        case 6:
            letter += "D";
        case 5,4,3,2,1,0:
            letter += "F";
    high_grade_options = ["Congradulations!","You really know your stuff!","Impressive!","Outstanding!","Perfection!","Magnificent!","Out of this world!","Unbelievable!"];
    mid_grade_options = ["You did good.","Nice job.","Great job.","Not bad.","Keep it up.","You're on your way."];
    low_grade_options = ["You might want to try again...","It's OK...","Ummm ...","You suck...","Better luck next time...","Did you even study?","What are you? A fifth-grader?","Can you even spell your name?"]
    print(end="\33[1;3m");
    if grade >= 0.90:
        print(f"{choice(high_grade_options)} {grade:.1%}, {letter}",end="\33[0m");
    elif grade >= 0.85:
        print(f"{choice(high_grade_options+mid_grade_options)} {grade:.1%}, {letter}",end="\33[0m");
    elif grade >= 0.75:
        print(f"{choice(mid_grade_options)} {grade:.1%}, {letter}",end="\33[0m");
    elif grade >= 0.65:
        print(f"{choice(mid_grade_options+low_grade_options)} {grade:.1%}, {letter}",end="\33[0m");
    else:
        print(f"{choice(low_grade_options)} {grade:.1%}, {letter}",end="\33[0m");
    return;

def generate_boolean_test(question_count: int, stage: int = 1) -> float:
    """creates a test over C# boolean expressions using basic operators, then announces and returns the grade"""
    max_difficulty = stage + int(5*math.log(1 + stage**2));
    correct = 0;
    
    print("\33[1mStarting test on boolean logic operations!\33[0m");
    sleep(1);
    print(f"\t\33[3m{question_count} questions, difficulty range [{stage}, {max_difficulty}]\33[0m\n");
    sleep(1.5);
    input("<Press Enter To Start>");
    delete_last_line();
    
    for i in range(question_count):
        D = randint(stage,max_difficulty);
        print(f"\33[1mQuestion #{i+1}:\33[0m \33[2;3mDifficulty Level {D}\33[0m");
        if generate_boolean_test_question(D):
            correct += 1;
        sleep(0.5);
        print()
    grade = correct / question_count;
    announce_grade(grade);
    return grade;

generate_boolean_test(question_count = 10, stage = 1);