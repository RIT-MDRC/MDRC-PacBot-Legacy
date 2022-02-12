import numpy as np
import matplotlib.pyplot as plt
from argparse import ArgumentParser


parser = ArgumentParser()
parser.add_argument('-p', '--parameter', action='store_true', help='Plot the parameter space')
parser.add_argument('filename', help='The data file to plot')
args = parser.parse_args()


if not args.parameter:
    with open(args.filename, 'rb') as f:
        all_results = np.load(f)

    print(f'{all_results.shape=}')

    scatter_data = [
        (iter_num, score)
        for iter_num, results in enumerate(all_results)
        for score in results
    ]

    plt.scatter(*zip(*scatter_data), alpha=0.2, edgecolors='none')
    plt.plot(np.mean(all_results, axis=1))
    plt.plot(np.median(all_results, axis=1))
    plt.tight_layout()
    plt.show()

else:
    with open(args.filename, 'rb') as f:
        all_results = np.load(f, allow_pickle=True)
    
    scatter_data = [
        (param_val, score)
        for param_val, results in all_results
        for score in results
    ]

    plt.scatter(*zip(*scatter_data), alpha=0.2, edgecolors='none')
    param_vals, results = zip(*all_results)
    plt.plot(param_vals, np.mean(results, axis=1))
    plt.plot(param_vals, np.median(results, axis=1))
    plt.tight_layout()
    plt.show()
