import sys
import re

rules = [
    {
        "name": "No snake_case",
        "pattern": r"\b[_]+[a-zA-Z0-9]+",
        "message": "Avoid using snake_case in JS (use camelCase instead)."
    },
    {
        "name": "Console log ban",
        "pattern": r"\bconsole\.log\(",
        "message": "Avoid using console.log in production code."
    },
    {
        "name": "Debug statements",
        "pattern": r"\bdebugger;",
        "message": "Remove debugger statements before deployment."
    }
]

def load_code(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.readlines()

def check_rules(code_lines):
    for i, line in enumerate(code_lines, start=1):
        for rule in rules:
            if re.search(rule["pattern"], line):
                print(f"🚨 Rule Violation: {rule['name']}")
                print(f"Line {i}: {line.strip()}")
                print(f"💡 Suggestion: {rule['message']}\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python rule_engine.py <file.js>")
    else:
        code = load_code(sys.argv[1])
        check_rules(code)
