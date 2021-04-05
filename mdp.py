from node import Node
from action import Action

class Mdp:
    GAMMA = 0.8

    CONV_FACTOR = 10e-9

    @staticmethod
    def Q(state, action, board, circular):
        return {"action": action,
                "value": sum(transition.prob*(transition.reward + Mdp.GAMMA * board[transition.end_pt].value)
                             for transition in state.set_transitions(action, board, circular))}

    @staticmethod
    def markovDecision(layout, circle):
        import numpy
        dices = {
            "security_dice": 1,
            "normal_dice": 2,
            "risky_dice": 3
        }
        board = [Node(pos, layout[pos], 0) for pos in range(len(layout))]
        board[0].n_type, board[-1].n_type = 0, 0
        board[-1].value = 0
        print(board)
        while True:
            for i in range(len(board)-1):
                state = board[i]
                if state.pos == 14:
                    state.value = 0
                else:
                    state.new_value = max(Mdp.Q(state, action, board, circle)["value"] for action in Action.ROLL)
                    x = [Mdp.Q(state, action, board, circle) for action in Action.ROLL]
                    for q in x:
                        if q["value"] == state.new_value:
                            state.optimal_action = q["action"]


            if max(abs(state.value - state.new_value) for state in board) < Mdp.CONV_FACTOR:
                return [numpy.array([node.new_value for node in board[:-1]]),
                        numpy.array([dices[node.optimal_action] for node in board[:-1]])]

            for val in board:
                val.value = val.new_value