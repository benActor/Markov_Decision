class Transition:
    def __init__(self, start_pt, end_pt, action, prob, reward):
        self.start_pt, self.end_pt, self.action, self.prob, self.reward = start_pt, end_pt, action, prob, reward

    def __repr__(self):
        return str({
            "from": self.start_pt,
            "to": self.end_pt,
            "with_actions": f"{self.action}",
            "prob": self.prob,
            "reward": self.reward
        })

    def __eq__(self, other):
        if not isinstance(other, Transition):
            return NotImplemented
        return self.start_pt == other.end_pt and \
            self.action == other.action and self.end_pt == other.end_pt