from mdp import Mdp
from simulation import Simulation
import numpy

if __name__ == '__main__':
    from random import randint
    layout = numpy.array([randint(0, 4) for i in range(15)])

    optimal_policy = Mdp.markovDecision(layout, True)[1]

    print(optimal_policy)
    print(Simulation.play(layout, optimal_policy, True))

