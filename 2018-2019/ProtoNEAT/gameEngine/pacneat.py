import os, sys, logging
import neat
import robomodules as rm
from messages import *



ADDRESS = os.environ.get("BIND_ADDRESS","localhost")
PORT = os.environ.get("BIND_PORT", 11297)


num_generations = 300  # Number of generations

class pacneat(rm.ProtoModule):

    def __init__(self, addr, port):
        self.subscriptions = [MsgType.FULL_STATE]
        super().__init__(addr, port, message_buffers, MsgType, self.subscriptions)
        self.state = None


    def msg_received(self, msg, msg_type):
        if msg_type == MsgType.FULL_STATE:
            print(1)



    def tick(self):
        pass

    # Called to evaluate all genomes
    def eval_genomes(genomes, config):
        for genome_id, genome in genomes:
            pass



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
        checkpoint = neat.Checkpointer(generation_interval=5, time_interval_seconds=500)
        pop.add_reporter(stats)
        pop.add_reporter(checkpoint)

        # Run through generations
        # Call function to evaluate genomes in a generation
        best_genome = pop.run(eval_genomes, num_generations)

        # Display the best genome among all num_generations
        print("(Best genome: {0})".format(best_genome))

        # Create a checkpoint

        # Best net
        best_net = neat.nn.FeedForwardNetwork.create(best_genome, config)

    if __name__ == '__main__':
        local_dir = os.path.dirname(__file__)
        config_path = os.path.join(local_dir, 'config')
        run(config_path)

