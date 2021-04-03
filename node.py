from action import Action

from transition import Transition


class Node:
    NODE_TYPES = {
        "ordinary": 0,
        "restart": 1,
        "penalty": 2,
        "prison": 3,
        "gamble": 4
    }

    def __init__(self, pos, n_type=NODE_TYPES["ordinary"], value=0):
        self.pos, self.n_type, self.value, self.new_value = pos, n_type, value, 0
        self.optimal_action = None

    def __repr__(self):
        return str({
            "position": self.pos,
            "type": self.n_type
        })

    def set_transitions(self, d_type, board, circular=False):
        transitions = self.s_primes(d_type, board, circular)
        all_transitions = []
        if d_type != "risky_dice":
            for tran in transitions[d_type]:

                # identical transitions from a point to the other
                identical = list(filter(lambda s: s["initial_pos"] == tran["initial_pos"] and s["pos"] == tran["pos"],
                                        transitions[d_type]))
                prob = sum(map(lambda s: s["prob"], identical))

                reward = Action.r(tran["initial_pos"], tran["pos"], self)

                all_transitions.append(Transition(tran["initial_pos"], tran["pos"], d_type, prob, reward))
        else:
            for tran in transitions[d_type]:

                # identical transitions from a point to the other
                identical = list(filter(lambda s: s["initial_pos"] == tran["initial_pos"] and s["pos"] == tran["pos"],
                                        transitions[d_type]))

                prob = sum(map(lambda s: s["prob"], identical))

                try:
                    reward = Action.r(tran["initial_pos"], tran["pos"], self, board[tran["via"]])
                except:
                    reward = Action.r(tran["initial_pos"], tran["pos"], self)

                all_transitions.append(Transition(tran["initial_pos"], tran["pos"], d_type, prob, reward))
        return Node.rem_dupli(all_transitions)

    def sec_dice_s(self, d_type):
        if self.pos not in [2, 9]:
            return [{"initial_pos": self.pos, "draw": draw, "pos": self.pos + draw,
                     "prob": Action.prob(self, "security_dice", draw)} for draw in Action.ROLL[d_type]]
        if self.pos == 2:
            return self.rem_dupli([{"initial_pos": self.pos, "draw": draw, "pos": self.pos + draw,
                                    "prob": Action.prob(self, "security_dice", draw)} for draw in Action.ROLL[d_type]] +
                                  [{"initial_pos": self.pos, "draw": draw, "pos": self.pos + draw * 8,
                                    "prob": Action.prob(self, "security_dice", draw)} for draw in Action.ROLL[d_type]])
        if self.pos == 9:
            return [{"initial_pos": self.pos, "draw": draw, "pos": self.pos + (draw * 5),
                     "prob": Action.prob(self, "security_dice", draw)} for draw in Action.ROLL[d_type]]

    def set_trap(self):
        penalty = 0
        # if restart penalty brings to pos 0
        if self.n_type == 1:
            penalty = 0

        # if penalty brings 3 cases backward
        if self.n_type == 2:
            if self.pos in [10, 11, 12]:
                penalty = self.pos - 10
            else:
                penalty = self.pos - 3 if self.pos > 2 else 0

        # if prison stay to the same point
        if self.n_type == 3:
            penalty = self.pos

        return penalty

    def norm_dice_s(self, d_type, circular):

        penalty = self.set_trap()

        if self.n_type == 4:
            s = []
            for draw in Action.ROLL[d_type]:
                if not draw:
                    s += [{"initial_pos": self.pos, "draw": draw, "pos": i,
                           "prob": Action.prob(self, "normal_dice", draw)/15} for i in range(15)]
                else:
                    if self.pos not in [2, 9, 12, 13]:
                        s += [{"initial_pos": self.pos, "draw": draw, "pos": self.pos + draw,
                               "prob": Action.prob(self, "normal_dice", draw)}]
                    elif self.pos == 2:
                        s += [{"initial_pos": self.pos, "draw": draw, "pos": self.pos + draw,
                               "prob": Action.prob(self, "normal_dice", draw)}]
                        s += [{"initial_pos": self.pos, "draw": draw, "pos": self.pos + draw + 7,
                               "prob": Action.prob(self, "normal_dice", draw)}]
                    elif self.pos == 9:
                        if not draw:
                            s += [{"initial_pos": self.pos, "draw": draw, "pos": self.pos,
                                   "prob": Action.prob(self, "normal_dice", draw)}]
                        else:
                            if self.pos + draw > 9 and not circular:
                                s += [{"initial_pos": self.pos, "draw": draw, "pos": self.pos + 14,
                                       "prob": Action.prob(self, "normal_dice", draw)}]
                            else:
                                if draw == 1:
                                    s += [{"initial_pos": self.pos, "draw": draw, "pos": self.pos + 5,
                                           "prob": Action.prob(self, "normal_dice", draw)}]
                                else:
                                    s += [{"initial_pos": self.pos, "draw": draw, "pos": 0,
                                           "prob": Action.prob(self, "normal_dice", draw)}]
                    elif self.pos in [12, 13]:
                        if self.pos + draw <= 14:
                            s += [{"initial_pos": self.pos, "draw": draw, "pos": self.pos + draw,
                                   "prob": Action.prob(self, "normal_dice", draw)}]
                        else:
                            if not circular:
                                s += [{"initial_pos": self.pos, "draw": draw, "pos": 14,
                                       "prob": Action.prob(self, "normal_dice", draw)}]
                            else:
                                s += [{"initial_pos": self.pos, "draw": draw, "pos": 15 - self.pos +draw,
                                       "prob": Action.prob(self, "normal_dice", draw)}]


                return s

        elif self.n_type == 0:
            if self.pos not in [2, 9, 12, 13]:
                return [{"initial_pos": self.pos, "draw": draw, "pos": self.pos + draw,
                         "prob": Action.prob(self, "normal_dice", draw)} for draw in Action.ROLL[d_type]]
            if self.pos == 2:
                s = []
                s += [{"initial_pos": self.pos, "draw": draw, "pos": self.pos + draw,
                       "prob": Action.prob(self, "normal_dice", draw)} for draw in Action.ROLL[d_type]]
                for draw in Action.ROLL[d_type]:
                    if draw:
                        s += [{"initial_pos": self.pos, "draw": draw, "pos": self.pos + 7 + draw,
                               "prob": Action.prob(self, "normal_dice", draw)}]
                return s

            if self.pos == 9:
                s = []
                for draw in Action.ROLL[d_type]:
                    if draw + self.pos <= 10:
                        s += [{"initial_pos": self.pos, "draw": draw, "pos": self.pos + (draw * 5),
                               "prob": Action.prob(self, "normal_dice", draw)}]
                    elif draw + self.pos > 10 and not circular:
                        s += [{"initial_pos": self.pos, "draw": draw, "pos": 14,
                               "prob": Action.prob(self, "normal_dice", draw)}]
                    else:
                        s += [{"initial_pos": self.pos, "draw": draw, "pos": 0,
                               "prob": Action.prob(self, "normal_dice", draw)}]
                return s
            if self.pos in [12, 13]:
                s = []
                for draw in Action.ROLL[d_type]:
                    if draw + self.pos <= 14:
                        s += [{"initial_pos": self.pos, "draw": draw, "pos": self.pos + draw,
                               "prob": Action.prob(self, "normal_dice", draw)}]
                    elif draw + self.pos > 14 and not circular:
                        s += [{"initial_pos": self.pos, "draw": draw, "pos": 14,
                               "prob": Action.prob(self, "normal_dice", draw)}]
                    else:
                        s += [{"initial_pos": self.pos, "draw": draw, "pos": 0,
                               "prob": Action.prob(self, "normal_dice", draw)}]
                return s


        else:
            if self.pos not in [2, 9, 12, 13]:
                s = []

                for draw in Action.ROLL[d_type]:
                    if not draw:

                        s += [{"initial_pos": self.pos, "draw": draw, "pos": penalty,
                               "prob": Action.prob(self, "normal_dice", draw)}]
                    else:
                        s += [{"initial_pos": self.pos, "draw": draw, "pos": self.pos + draw,
                               "prob": Action.prob(self, "normal_dice", draw)}]
                return s
            if self.pos == 2:
                s = []
                for draw in Action.ROLL[d_type]:
                    if draw:
                        s += [{"initial_pos": self.pos, "draw": draw, "pos": self.pos + draw,
                               "prob": Action.prob(self, "normal_dice", draw)}]
                    else:
                        s += [{"initial_pos": self.pos, "draw": draw, "pos": penalty,
                               "prob": Action.prob(self, "normal_dice", draw)}]

                for draw in Action.ROLL[d_type]:
                    if draw:
                        s += [{"initial_pos": self.pos, "draw": draw, "pos": self.pos + 7 + draw,
                               "prob": Action.prob(self, "normal_dice", draw)}]
                return s

            if self.pos == 9:
                s = []
                for draw in Action.ROLL[d_type]:
                    if not draw:
                        s += [{"initial_pos": self.pos, "draw": draw, "pos": penalty,
                               "prob": Action.prob(self, "normal_dice", draw)}]
                    elif draw == 1:
                        s += [{"initial_pos": self.pos, "draw": draw, "pos": self.pos + 5,
                               "prob": Action.prob(self, "normal_dice", draw)}]
                    elif draw == 2 and not circular:
                        s += [{"initial_pos": self.pos, "draw": draw, "pos": self.pos + 5,
                               "prob": Action.prob(self, "normal_dice", draw)}]
                    else:
                        s += [{"initial_pos": self.pos, "draw": draw, "pos": 0,
                               "prob": Action.prob(self, "normal_dice", draw)}]
                return s
            if self.pos in [12, 13]:
                s = []
                for draw in Action.ROLL[d_type]:
                    if not draw:
                        s += [{"initial_pos": self.pos, "draw": draw, "pos": penalty,
                               "prob": Action.prob(self, "normal_dice", draw)}]
                    else:
                        if self.pos + draw <= 14:
                            s += [{"initial_pos": self.pos, "draw": draw, "pos": self.pos + draw,
                                   "prob": Action.prob(self, "normal_dice", draw)}]
                        elif self.pos + draw > 14 and not circular:
                            s += [{"initial_pos": self.pos, "draw": draw, "pos": 14,
                                   "prob": Action.prob(self, "normal_dice", draw)}]
                        else:
                            s += [{"initial_pos": self.pos, "draw": draw, "pos": 0,
                                   "prob": Action.prob(self, "normal_dice", draw)}]
                return s


    def set_dest_trap(self, via_node):
        penalty = 0
        # if restart penalty brings to pos 0
        if via_node.n_type == 1:
            penalty = 0

        # if penalty brings 3 cases backward
        if via_node.n_type == 2:
            if via_node.pos in [10, 11, 12]:
                penalty = via_node.pos - 10
            else:
                penalty = via_node.pos - 3 if via_node.pos > 2 else 0

        # if prison stay to the same point
        if via_node.n_type == 3:
            penalty = via_node.pos

        return penalty

    def fill_state(self, via_node, draw):
        s = []
        if via_node.n_type == 4:
            s += [{"initial_pos": self.pos, "draw": draw, "pos": i, "via": via_node.pos,
                   "prob": Action.prob(via_node, "risky_dice", draw)/15} for i in range(15)]
        elif via_node.n_type == 0:
            s += [{"initial_pos": self.pos, "draw": draw, "pos": via_node.pos, "via": None,
                   "prob": Action.prob(via_node, "risky_dice", draw)}]
        else:
            penalty = self.set_dest_trap(via_node)
            s += [{"initial_pos": self.pos, "draw": draw, "pos": penalty, "via": via_node.pos,
                   "prob": Action.prob(via_node, "risky_dice", draw)}]

        return s

    def risky_dice_s(self, d_type, board, circular):
        if self.pos not in [2, 7, 8, 9, 12, 13]:
            s = []
            for draw in Action.ROLL[d_type]:
                via_node = board[self.pos + draw]
                s += self.fill_state(via_node, draw)
            return s

        if self.pos == 2:
            s = []
            for draw in Action.ROLL[d_type]:
                if not draw:
                    via_node = self
                    s += self.fill_state(via_node, draw)
                else:
                    for via_node in [board[self.pos + draw], board[self.pos + draw + 7]]:
                        s += self.fill_state(via_node, draw)
            return s

        if self.pos in [7, 8, 9]:
            s = []
            for draw in Action.ROLL[d_type]:
                if not draw:
                    via_node = self
                    s += self.fill_state(via_node, draw)
                else:
                    if self.pos + draw <= 9:
                        via_node = board[self.pos + draw]
                        s += self.fill_state(via_node, draw)
                    if self.pos + draw > 9 and not circular:
                        s += [{"initial_pos": self.pos, "draw": draw, "pos": 14, "via": None, "prob": Action.prob(self, "risky_dice", draw)}]
                    else:
                        if self.pos + draw + 4 == 14:
                            s += [{"initial_pos": self.pos, "draw": draw, "pos": 14, "via": None, "prob": Action.prob(self, "risky_dice", draw)}]
                        else:
                            via_node = board[self.pos + draw - 10]
                            s += self.fill_state(via_node, draw)
            return s

        if self.pos in [12, 13]:
            s = []
            for draw in Action.ROLL[d_type]:
                if self.pos + draw <= 14:
                    via_node = board[self.pos + draw]
                    s += self.fill_state(via_node, draw)
                elif self.pos + draw > 14 and not circular:
                    via_node = board[14]
                    s += self.fill_state(via_node, draw)
                else:
                    via_node = board[self.pos + draw - 15]
                    s += self.fill_state(via_node, draw)
            return s


    def s_primes(self, d_type, board, circular=False):
        if d_type == "security_dice":
            return {d_type:  self.sec_dice_s(d_type)}

        if d_type == "normal_dice":
            return {d_type: self.norm_dice_s(d_type, circular)}

        if d_type == "risky_dice":
            return {d_type: self.risky_dice_s(d_type, board, circular)}

    @staticmethod
    def rem_dupli(trans_list):
        dupli = []
        unique = []
        for i in range(len(trans_list)):
            if trans_list[i] in trans_list[i + 1:] or trans_list[i] in dupli:
                dupli.append(trans_list[i])
            else:
                unique.append(trans_list[i])
        if dupli:
            return [dupli[0]] + unique
        return unique
