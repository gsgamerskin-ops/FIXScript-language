import sys
import re

variables = {}
functions = {}


def run_block(lines):
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        if not line or line.startswith("//"):
            i += 1
            continue

        if line.startswith("print"):
            match = re.search(r'print\((.*?)\)', line)

            if match:
                value = match.group(1).strip().strip('"')
                print(value)

        elif "=" in line:
            parts = line.split("=", 1)
            var = parts[0].strip()
            value = parts[1].strip().strip('"')
            variables[var] = value

        elif line.startswith("call"):
            name = line.replace("call", "").replace("()", "").strip()

            if name in functions:
                run_block(functions[name])

        i += 1


def parse_functions(code_lines):
    i = 0

    while i < len(code_lines):
        line = code_lines[i].strip()

        if line.startswith("function"):
            name = line.replace("function", "").replace("()", "").strip()

            while "{" not in code_lines[i]:
                i += 1

            i += 1

            block = []

            while "}" not in code_lines[i]:
                block.append(code_lines[i])
                i += 1

            functions[name] = block

        i += 1


if len(sys.argv) < 2:
    print("Usage: python compiler.py file.fix")
    sys.exit()

filename = sys.argv[1]

with open(filename, "r", encoding="utf-8") as f:
    code = f.readlines()

parse_functions(code)

if "Main" in functions:
    run_block(functions["Main"])
else:
    print("Main function not found")0