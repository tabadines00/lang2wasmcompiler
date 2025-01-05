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
            expr = tokens[2:]
            self.add_local(var_name)
            self.compile_expression(expr)
            self.wat += f"    local.set ${var_name}\n"
    
    def compile_expression(self, expr):
        for token in expr:
            if token.isdigit():
                self.wat += f"    i32.const {token}\n"
            elif token == "+":
                self.wat += "    i32.add\n"
            elif token == "-":
                self.wat += "    i32.sub\n"
            elif token == "*":
                self.wat += "    i32.mul\n"
            else:  # Variable
                self.wat += f"    local.get ${token}\n"
    
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
