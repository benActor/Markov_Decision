from mdp import Mdp

if __name__ == '__main__':
    from random import randint

    layout = [randint(0, 4) for i in range(15)]
    print(Mdp.markovDecision(layout, False))