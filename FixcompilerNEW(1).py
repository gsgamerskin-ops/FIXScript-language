import sys
import os
import re

variables = {}
functions = {}

# -------------------------
# EXECUÇÃO DE BLOCO
# -------------------------
def run_block(lines):
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

        # CALL
        elif line.lower().startswith("call"):
            name = line.replace("call", "").strip()

            if name in functions:
                run_block(functions[name])
            else:
                print(f"[WARN] Function '{name}' not found")

        else:
            print(f"[INFO] Unknown command: {line}")

        i += 1


# -------------------------
# PARSER DE FUNÇÕES (CORRIGIDO)
# -------------------------
def parse_functions(code_lines):
    i = 0

    while i < len(code_lines):
        line = code_lines[i].strip()

        # detecta function de forma robusta
        match = re.search(r'function\s+([a-zA-Z0-9_]+)', line, re.IGNORECASE)

        if match:
            name = match.group(1)

            # procura abertura {
            while i < len(code_lines) and "{" not in code_lines[i]:
                i += 1

            i += 1
            block = []

            # captura até }
            while i < len(code_lines) and "}" not in code_lines[i]:
                block.append(code_lines[i])
                i += 1

            functions[name] = block

        i += 1


# -------------------------
# CARREGAR ARQUIVO
# -------------------------
def load_file(path):
    if not os.path.exists(path):
        print(f"[ERROR] File not found: {path}")
        sys.exit()

    with open(path, "r", encoding="utf-8") as f:
        return f.readlines()


# -------------------------
# INPUT DE ARQUIVO (ANDROID SAFE)
# -------------------------
def get_file_path():
    if len(sys.argv) >= 2:
        return sys.argv[1]

    try:
        return input("Digite o caminho do arquivo .fix: ").strip()
    except:
        print("[ERROR] Cannot read input")
        sys.exit()


# -------------------------
# MAIN
# -------------------------
file_path = get_file_path()

code = load_file(file_path)

parse_functions(code)

if "Main" in functions:
    run_block(functions["Main"])
else:
    print("[ERROR] Main function not found")