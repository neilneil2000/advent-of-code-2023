class RulesEngine:
    def __init__(self, rules):
        self.rules = rules
        self.accepted = []
        self.rejected = []

    def process_rule(self, part, rule_name):
        for rule in self.rules[rule_name]:
            if isinstance(rule, str):
                return rule
            small, large, next_rule = rule
            if isinstance(small, str):
                small = part[small]
            else:
                large = part[large]
            if small < large:
                return next_rule

    def process_part(self, part):
        rule_name = "in"
        while rule_name not in ["A", "R"]:
            rule_name = self.process_rule(part, rule_name)
        if rule_name == "A":
            self.accepted.append(part)
        else:
            self.rejected.append(part)

    def process_all(self):
        parts = {
            "in": {
                "x": (1, 4000),
                "m": (1, 4000),
                "a": (1, 4000),
                "s": (1, 4000),
            }
        }
        rule_name = "in"
        while ("A" not in parts) or ("R" not in parts) or len(parts) > 2:
            for rule_name in parts.copy():
                parts = self.process_rule_all_parts(
                    rule_name, self.rules[rule_name], parts
                )

    def process_rule_all_parts(self, rule_name, rule, parts):
        for step in rule:
            if isinstance(step, str):
                parts[step] = parts.pop(rule_name)
                return parts
            small, large, next_rule = step
            if isinstance(small, int):
                parts = self.update_parts(
                    parts, rule_name, next_rule, large, small, False
                )
            else:
                parts = self.update_parts(
                    parts, rule_name, next_rule, small, large, True
                )
        return parts

    def update_parts(
        self, parts, input_rule, output_rule, letter, number, less_than: bool
    ):
        if output_rule in parts:
            parts[output_rule] = [parts[output_rule]]
            low, high = parts[output_rule][letter]
            if less_than:
                new_high = min(high, number - 1)
                parts[output_rule][letter].append((low, new_high))
                parts[input_rule][letter] = (new_high + 1, high)
            else:
                new_low = max(low, number + 1)
                parts[output_rule][letter].append((new_low, high))
                parts[input_rule][letter] = (low, new_low - 1)
            pass
        else:
            parts[output_rule] = parts[input_rule].copy()
            low, high = parts[output_rule][letter]
            if less_than:
                new_high = min(high, number - 1)
                parts[output_rule][letter] = (low, new_high)
                parts[input_rule][letter] = (new_high + 1, high)
            else:
                new_low = max(low, number + 1)
                parts[output_rule][letter] = (new_low, high)
                parts[input_rule][letter] = (low, new_low - 1)
        return parts

    @property
    def total_rating(self):
        if not self.accepted:
            return 0
        total = 0
        for accepted in self.accepted:
            total += sum(accepted.values())
        return total
