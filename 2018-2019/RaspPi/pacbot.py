import os
import neat
from helper import *

checkpoint_interval = 5 # The interval of being reported per genome in generation
num_generations = 300   # Number of generations

# Activation: Softmax function
def softmax(vec):
    # Convert to numpy array
    output_layer_in = np.array(vec)
    # Set numerator values from output_layer_in
    exponents = [np.exp(row) for row in output_layer_in]
    # Set denominator
    sum_exp = sum(exponents)
    # Create the output layer activation values
    output_vec = [exp/sum_exp for exp in exponents]

    assert output_layer_in.shape == (4,1)

    return output_vec

# Calculate the percentage error
def calc_error(inp, expected):
    percentage_error = abs(inp - expected) / expected * 100
    return percentage_error

# Called to evaluate all genomes
def eval_genomes(genomes, config):
    pass

    # Create Feed Forward Network

def run(config_file):

    # Get config_file and set up
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Add custom activation function to config file
    config.genome_config.add_activation('softmax_custom', softmax)

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
<<<<<<< HEAD:2018-2019/RaspPi/pacbot.py
    for input, point in zip(inputs, points):
        output = best_net.activate(input)
=======
    for inp, point in zip(inputs, points):
        # Prediction
        output = best_net.activate(inp)
>>>>>>> 861ff38f6d87225e5967777b46fab616e609b2d6:2018-2019/pacbot.py
        # Display the output and error
        print("input: {:20}\nexpected output: {:20}\noutput: {:20}\nerror: {:20}".format(input, point, output, calc_error(input, output)))

if __name__ = '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config')
    run(config_path)
