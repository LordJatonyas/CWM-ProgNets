# !/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 [filename]")
        sys.exit()
    filename = sys.argv[1]
    number = filename[-5]
    xlabel = "Iteration"
    ylabel = "Bandwidth"
    title = f'Bandwidth'
    fig_name = f'bandwidth-{number}.png'

    t = np.loadtxt(filename, delimiter=" ", dtype="float")
    ind = np.arange(1, len(t) + 1)

    fig = plt.figure()
    ax = fig.add_axes([0.2, 0.2, 0.7, 0.7])
    ax.bar(ind, t, 0.8)
    ax.set_ylim(ymin=900)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.savefig(fig_name)
    plt.show()


if __name__ == "__main__":
    main()
