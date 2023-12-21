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
        all_accepted = []
        all_rejected = []
        while parts:
            for rule_name in parts.copy():
                accepted, rejected, parts = self.process_rule_all_parts(
                    rule_name, self.rules[rule_name], parts
                )
                all_accepted.extend(accepted)
                all_rejected.extend(rejected)
        return self.calculate_combos(all_accepted)

    def calculate_combos(self, combinations):
        """Return total number of possible combinations"""
        total = 0
        for combination in combinations:
            working = 1
            for low, high in combination.values():
                working *= high - low + 1
            total += working
        return total

    def process_rule_all_parts(self, rule_name, rule, parts):
        all_accepted = []
        all_rejected = []
        for step in rule:
            if isinstance(step, str):
                if step == "A":
                    all_accepted = [parts.pop(rule_name)]
                elif step == "R":
                    all_rejected = [parts.pop(rule_name)]
                else:
                    parts[step] = parts.pop(rule_name)
                return all_accepted, all_rejected, parts
            small, large, next_rule = step
            if isinstance(small, int):
                accepted, rejected, parts = self.update_parts(
                    parts, rule_name, next_rule, large, small, False
                )

            else:
                accepted, rejected, parts = self.update_parts(
                    parts, rule_name, next_rule, small, large, True
                )
            all_accepted.extend(accepted)
            all_rejected.extend(rejected)
        return all_accepted, all_rejected, parts

    def update_parts(
        self, parts, input_rule, output_rule, letter, number, less_than: bool
    ):
        accepted = []
        rejected = []
        if output_rule == "A":
            accepted = parts[input_rule].copy()
            low, high = accepted[letter]
            if less_than:
                new_high = min(high, number - 1)
                accepted[letter] = (low, new_high)
                parts[input_rule][letter] = (new_high + 1, high)
            else:
                new_low = max(low, number + 1)
                accepted[letter] = (new_low, high)
                parts[input_rule][letter] = (low, new_low - 1)
            accepted = [accepted]
        elif output_rule == "R":
            rejected = parts[input_rule].copy()
            low, high = rejected[letter]
            if less_than:
                new_high = min(high, number - 1)
                rejected[letter] = (low, new_high)
                parts[input_rule][letter] = (new_high + 1, high)
            else:
                new_low = max(low, number + 1)
                rejected[letter] = (new_low, high)
                parts[input_rule][letter] = (low, new_low - 1)
            rejected = [rejected]
        elif output_rule in parts:
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
        return accepted, rejected, parts

    @property
    def total_rating(self):
        if not self.accepted:
            return 0
        total = 0
        for accepted in self.accepted:
            total += sum(accepted.values())
        return total
