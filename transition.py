class Transition:
    def __init__(self, start_pt, end_pt, action, prob, reward):
        self.start_pt, self.end_pt, self.action, self.prob, self.reward = start_pt, end_pt, action, prob, reward