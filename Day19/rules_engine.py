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

    @property
    def total_rating(self):
        if not self.accepted:
            return 0
        total = 0
        for accepted in self.accepted:
            total += sum(accepted.values())
        return total
