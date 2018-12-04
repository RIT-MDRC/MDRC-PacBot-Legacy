
""" Controls NEAT algorithm using the eval_genomes and the run method."""

import os
import neat
# Import neat library
# Find a way to import ghostpathfinding in protoAI botCode

""" Evaluates the genomes until they match the Simple AI requirements in terms of movement direction """
def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        # Network gets output for which direction to go to.
        # Assessing the model based on how much points it got
        # Select the ones that are doing better in points
        # not in movements
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        netOut = net.activate()



def run(config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)



if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config')
    run(config_path)
