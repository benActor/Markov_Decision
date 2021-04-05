from random import choice, randint
from node import Node


class Simulation:
    @staticmethod
    def print_board(board, node):
        for n in board:
            if n.pos == node.pos:
                print("x", end=" ")
            else:
                print("-", end=" ")

    @staticmethod
    def pos_after_penalty(current_pos, penalty, node, strategy):
        if node.n_type != 0 or strategy != 1:
            if penalty == 1:
                final_position = 0
            elif penalty == 2:
                if current_pos in [10, 11, 12]:
                    final_position = current_pos -10
                elif current_pos < 3:
                    final_position = 0
                else:
                    final_position = current_pos - 3
            elif penalty == 4:
                final_position = randint(0, 14)
            else:
                final_position = current_pos
        else:
            final_position = current_pos

        return final_position

    @staticmethod
    def roll_dice(strategy):
        dices = {
            1: [0, 1],
            2: [0, 1, 2],
            3: [0, 1, 2, 3]
        }
        return choice(dices[strategy])

    @staticmethod
    def move_node(initial_pos, draw, board, strategy, circular=False):
        if initial_pos == 2:
            lane = choice([1, 2])
            if lane == 2:
                pos = initial_pos + 7 + draw
            else:
                pos = initial_pos + draw
        elif initial_pos in [7, 8, 9]:
            if initial_pos + draw < 10:
                pos = initial_pos + draw
            elif initial_pos + draw >= 10 and not circular:
                pos = 14
            else:
                pos = (initial_pos + draw + 4) - 15
        else:
            if initial_pos + draw <= 14:
                pos = initial_pos + draw
            elif initial_pos + draw > 14 and not circular:
                pos = 14
            else:
                pos = initial_pos + draw - 15
        if strategy == 3:
            return Simulation.pos_after_penalty(pos, board[pos].n_type, board[pos], strategy)
        elif strategy == 2:
            if draw == 0:
                return Simulation.pos_after_penalty(pos, board[pos].n_type, board[pos], strategy)
            else:
                return pos
        else:
            return pos

    @staticmethod
    def play(layout, policy, circular=False):
        board = [Node(pos, layout[pos], 0) for pos in range(len(layout))]

        board[0].n_type, board[-1].n_type = 0, 0

        node = board[0]


        end_state = 14

        number_of_turn = 0
        print("AT START")

        Simulation.print_board(board, node)

        while node.pos != end_state:
            strategy = policy[node.pos]
            roll = Simulation.roll_dice(strategy)
            print()
            print("node_pos",node.pos)
            print("roll", roll)
            print("srat,", strategy)

            node = board[Simulation.move_node(initial_pos=node.pos, draw=roll, board=board, strategy= strategy,
                                              circular=circular)]

            if node.n_type == 3:
                number_of_turn += 2
            else:
                number_of_turn += 1

            Simulation.print_board(board, node)

        print()
        print("the number of turn is: ", number_of_turn)

        return number_of_turn
