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
    t1 = t[:,0]
    t2 = t[:,1]
    ind = np.arange(1, len(t) + 1)

    plt.bar(ind - 0.2, t1, 0.4, label = "Backward")
    plt.bar(ind + 0.2, t2, 0.4, label = "Forward")
    plt.ylim(750,980)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.savefig(fig_name)
    plt.show()


if __name__ == "__main__":
    main()
