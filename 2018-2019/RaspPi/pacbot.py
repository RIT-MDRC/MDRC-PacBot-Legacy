import os
import neat
import numpy as np
from helper import *

checkpoint_interval = 5 # The interval of being reported per genome in generation
num_generations = 300   # Number of generations

# Called to evaluate all genomes
def eval_genomes(genomes, config):
    pass

    # Create Feed Forward Network

def run(config_file):

    # Get config_file and set up
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)
    # Creates the population
    pop = neat.Population(config)

    # Set Reporters
    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    checkpoint = neat.CheckPointer(checkpoint_interval)
    pop.add_reporter(stats)
    pop.add_reporter(checkpoint)

    # Run through generations
        # Call function to evaluate genomes in a generation
    best_genome = pop.run(eval_genomes, num_generations)

    # Display the best genome among all num_generations
    print("(Best genome: {0})".format(best_genome))

    # Best net
    best_net = neat.nn.FeedForwardNetwork.create(best_genome, config)
    # Get the inputs and outputs form the game and feed it in the network
    for inp, point in zip(inputs, points):
        output = best_net.activate(inp)
        # Display the output and error
        print("input: {:20}\nexpected output: {:20}\noutput: {:20}\nerror: {:20}".format(inp, point, output, calc_error(inp, output)))

if __name__ = '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config')
    run(config_path)
