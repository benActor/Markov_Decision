from mdp import Mdp
import  numpy

if __name__ == '__main__':
    from random import randint
    layout = numpy.array([randint(0, 4) for i in range(15)])
    print(Mdp.markovDecision(layout, True))
    
    print(Simulation.play(layout, Mdp.markovDecision(layout, True), True))
