from fpdf import FPDF;
import random;

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12);
        self.cell(0, 10, 'Math Worksheet', 0, 1, 'C');

    def footer(self):
        self.set_y(-15);
        self.set_font('Arial', 'I', 8);
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C');

    def chapter_title(self, title: str):
        self.set_font('Arial', 'B', 12);
        self.cell(0, 10, title, 0, 1, 'L');
        self.ln(5);

    def chapter_body(self, body: str):
        self.set_font('Arial', '', 12);
        self.multi_cell(0, 10, body); # type: ignore
        self.ln();

def generate_problems(num_problems: int = 10) -> list[str]:
    problems: list[str] = [];
    operations = ['+', '-', '*', '/'];
    a: int;
    b: int;
    for _ in range(num_problems):
        op = random.choice(operations);
        if op == '+':
            a, b = random.randint(1, 100), random.randint(1, 100);
        elif op == '-':
            a, b = random.randint(1, 100), random.randint(1, 100);
            if a < b:
                a, b = b, a;
        elif op == '*':
            a, b = random.randint(1, 12), random.randint(1, 12);
        elif op == '/':
            b = random.randint(1, 12);
            a = b * random.randint(1, 12);
        problems.append(f"{a} {op} {b} = "); # type: ignore
    return problems;

def create_math_worksheet(filename: str = 'math_worksheet.pdf', num_problems: int = 10):
    pdf = PDF();
    pdf.add_page();
    pdf.chapter_title('Solve the following problems:');
    problems = generate_problems(num_problems);
    for problem in problems:
        pdf.chapter_body(problem);
    pdf.output(filename);
    
"""import matplotlib.pyplot as plt;

# Create a plot with LaTeX expression
plt.figure();
plt.text(0.5, 0.5, r'$\alpha > \beta$', fontsize=20, ha='center');
plt.axis('off');
plt.savefig('obj/math_expression.png', bbox_inches='tight');"""

if __name__ == "__main__":
    create_math_worksheet();
    ...