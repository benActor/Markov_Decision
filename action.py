class Action:
    ROLL = {
        "security_dice": [0, 1],
        "normal_dice": [0, 1, 2],
        "risky_dice": [0, 1, 2, 3]
    }

    @staticmethod
    def r(start_state, final_state, s_node, end_node=None):
        if final_state - start_state == 0 and s_node.n_type == 3:
            return -2
        if end_node and end_node.n_type == 3:
            return final_state - start_state - 2
        return final_state - start_state

    @staticmethod
    def draw_prob(d_type, draw, lane):
        for roll in Action.ROLL[d_type]:
            if roll == draw:
                return 1 / (len(Action.ROLL[d_type]) * lane)

    @staticmethod
    def prob(s_node, d_type, draw):
        lane = 2 if s_node.pos == 2 else 1
        return Action.draw_prob(d_type, draw, lane)
