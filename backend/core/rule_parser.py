import json
import re
from rules.rule_schema import Rule
from typing import List

def load_rules(path="rules/rules.json") -> List[Rule]:
    with open(path, "r") as f:
        data = json.load(f)
    return [Rule(**rule) for rule in data]

def apply_rules(code: str, rules: List[Rule]):
    violations = []
    for rule in rules:
        if re.search(rule.pattern, code):
            violations.append({
                "id": rule.id,
                "description": rule.description,
                "severity": rule.severity,
                "recommendation": rule.recommendation
            })
    return violations
