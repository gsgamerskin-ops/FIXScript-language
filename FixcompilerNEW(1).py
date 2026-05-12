import sys
import os
import re

variables = {}
functions = {}

# -------------------------
# EXECUÇÃO DE BLOCO
# -------------------------
def run_block(lines, args=None):
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        if not line or line.startswith("//"):
            i += 1
            continue

        # PRINTF
        if line.lower().startswith("printf"):
            content = line[len("printf"):].strip()
            content = content.strip('"')
            print(content)

        # LOCAL
        elif line.lower().startswith("local"):
            parts = line.split()
            if len(parts) > 1:
                variables[parts[1]] = None

        # ATRIBUIÇÃO
        elif "=" in line:
            var, value = line.split("=", 1)
            variables[var.strip()] = value.strip().strip('"')

        # CALL COM PARÂMETROS
        elif line.lower().startswith("call"):
            parts = line.split()
            name = parts[1]

            call_args = parts[2:]

            if name in functions:
                run_block(functions[name], call_args)
            else:
                print(f"[WARN] Function '{name}' not found")

        i += 1


# -------------------------
# PARSER DE FUNÇÕES
# -------------------------
def parse_functions(code_lines):
    i = 0

    while i < len(code_lines):
        line = code_lines[i].strip()

        match = re.search(r'function\s+([a-zA-Z0-9_]+)', line, re.IGNORECASE)

        if match:
            name = match.group(1)

            while i < len(code_lines) and "{" not in code_lines[i]:
                i += 1

            i += 1
            block = []

            while i < len(code_lines) and "}" not in code_lines[i]:
                block.append(code_lines[i])
                i += 1

            functions[name] = block

        i += 1


# -------------------------
# LIBRARY LOADER (.FXL)
# -------------------------
def load_library(path):
    if not os.path.exists(path):
        print(f"[ERROR] Library not found: {path}")
        return []

    with open(path, "r", encoding="utf-8") as f:
        return f.readlines()


# -------------------------
# IMPORT HANDLER
# -------------------------
def handle_imports(code_lines):
    new_code = []

    for line in code_lines:
        if line.strip().lower().startswith("import"):
            lib = line.replace("import", "").strip().strip('"')

            lib_code = load_library(lib)

            # injeta funções da lib direto no runtime
            parse_functions(lib_code)
        else:
            new_code.append(line)

    return new_code


# -------------------------
# MAIN
# -------------------------
def get_file():
    if len(sys.argv) >= 2:
        return sys.argv[1]
    return input("Digite caminho .fix: ").strip()


file_path = get_file()

if not os.path.exists(file_path):
    print("[ERROR] File not found")
    sys.exit()

with open(file_path, "r", encoding="utf-8") as f:
    code = f.readlines()

# IMPORTS
code = handle_imports(code)

# PARSE
parse_functions(code)

# RUN
if "Main" in functions:
    run_block(functions["Main"])
else:
    print("[ERROR] Main function not found")
