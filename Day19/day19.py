from day19_test_input import day19_input
from rules_engine import RulesEngine


def main():
    rules, parts = parse_input()
    engine = RulesEngine(rules)
    for part in parts:
        engine.process_part(part)
    print(f"Part1: {engine.total_rating}")

    answer = engine.process_all()
    print(f"Part2: {answer}")


def parse_input():
    rules, parts = day19_input.split("\n\n")
    rules = parse_rules(rules)
    parts = parse_parts(parts)
    return rules, parts


def parse_rules(rules):
    rules = rules.splitlines()
    parsed_rules = {}
    for rule in rules:
        rule_name, rule_elements = rule.split("{")
        rule_elements = rule_elements.split(",")
        parsed_element = []
        for element in rule_elements:
            if ":" not in element:
                parsed_element.append(element.strip("}"))
                continue
            comparator, next_rule = element.split(":")
            if "<" in comparator:
                small = comparator[0]
                large = int(comparator[2:])
            else:
                large = comparator[0]
                small = int(comparator[2:])
            parsed_element.append((small, large, next_rule))
        parsed_rules[rule_name] = parsed_element.copy()
    return parsed_rules


def parse_parts(parts: str):
    parts = parts.splitlines()
    parsed_parts = []
    for part in parts:
        part = part.split(",")
        part_dict = {}
        for element in part:
            element = element.strip("{}")
            parameter, value = element.split("=")
            part_dict[parameter] = int(value)
        parsed_parts.append(part_dict)
    return parsed_parts


if __name__ == "__main__":
    main()
