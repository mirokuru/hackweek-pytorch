import logging
import coloredlogs

import sys
import argparse

from Coach import Coach
from othello.OthelloGame import OthelloGame as Game
from othello.pytorch.NNet import NNetWrapper as nn
from utils import *
from my_aws_functions import *


log = logging.getLogger(__name__)

coloredlogs.install(level='DEBUG')  # Change this from INFO to DEBUG to see more info.

args = dotdict({
    'numIters': 15,  # was 100 and originally 1000
    'numEps': 10,  # was 10 and originally 100     # Number of complete self-play games to simulate during a new iteration.
    'tempThreshold': 15,        #
    'updateThreshold': 0.6,     # During arena playoff, new neural net will be accepted if threshold or more of games are won.
    'maxlenOfQueue': 200000,    # Number of game examples to train the neural networks.
    'numMCTSSims': 25,          # Number of games moves for MCTS to simulate.
    'arenaCompare': 40,         # was 40, Number of games to play during arena play to determine if new net will be accepted.
    'cpuct': 1,

    'checkpoint': './current_model/',
    'load_model': True,
    'load_folder_file': ('./current_model/', 'best.pth.tar'),
    'numItersForTrainExamplesHistory': 20,

})


def retrieve_model():
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', type=int, required=True)
    my_args = parser.parse_args()
    log.info(f'Requested version is {my_args.version}...')
    return handle_versions(my_args.version)


def handle_versions(new_version):
    if not check_for_model(new_version):
        log.info(f'Requested version {new_version} not found yet as expected')
        previous_version = new_version - 1
        if check_for_model(previous_version):
            log.info(f'Previous version {previous_version} found as expected')
            download_model(previous_version)
            return new_version
        else:
            log.info(f'Version {previous_version} not found! Cannot continue!')
            sys.exit()
    else:
        log.info(f'Version {new_version} already found! Will not continue!')
        sys.exit()


def main():
    new_version = retrieve_model()

    log.info('Loading %s...', Game.__name__)
    g = Game(8)

    log.info('Loading %s...', nn.__name__)
    nnet = nn(g)

    if args.load_model:
        log.info('Loading checkpoint "%s/%s"...', args.load_folder_file[0], args.load_folder_file[1])
        nnet.load_checkpoint(args.load_folder_file[0], args.load_folder_file[1])
    else:
        log.warning('Not loading a checkpoint!')

    log.info('Loading the Coach...')
    c = Coach(g, nnet, args)

    if args.load_model:
        log.info("Loading 'trainExamples' from file...")
        c.loadTrainExamples()

    log.info('Starting the learning process 🎉')
    c.learn(new_version)


if __name__ == "__main__":
    main()

