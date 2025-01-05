class Compiler:
    def __init__(self):
        self.wat = "(module\n"
        self.wat += "  (func $main\n"
        self.locals = []
    
    def add_local(self, name):
        self.locals.append(name)
        self.wat += f"    (local ${name} i32)\n"
    
    def compile_line(self, line):
        tokens = line.strip().split()
        if "=" in tokens:  # Handle assignment
            var_name = tokens[0]
            expr = " ".join(tokens[2:])  # Join the expression part
            self.add_local(var_name)
            self.compile_expression(expr)
            self.wat += f"    local.set ${var_name}\n"
    
    def compile_expression(self, expr):
        # Simple infix expression parsing
        tokens = expr.split()
        output = []
        operators = []
        
        precedence = {'+': 1, '-': 1, '*': 2}
        
        def apply_operator(op):
            right = output.pop()
            left = output.pop()
            self.wat += f"    local.get ${left}\n"
            self.wat += f"    local.get ${right}\n"
            if op == '+':
                self.wat += "    i32.add\n"
            elif op == '-':
                self.wat += "    i32.sub\n"
            elif op == '*':
                self.wat += "    i32.mul\n"
        
        for token in tokens:
            if token.isdigit() or token in self.locals:
                output.append(token)
            elif token in precedence:
                while (operators and operators[-1] in precedence and
                       precedence[token] <= precedence[operators[-1]]):
                    apply_operator(operators.pop())
                operators.append(token)
        
        while operators:
            apply_operator(operators.pop())
    
    def finish(self):
        self.wat += "  )\n)"  # Close the module and function

# Example usage
source = """
x = 3 - 4
y = x * 10
"""

compiler = Compiler()
for line in source.strip().splitlines():
    compiler.compile_line(line)
compiler.finish()
print(compiler.wat)
