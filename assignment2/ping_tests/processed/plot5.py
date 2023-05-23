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
    xlabel = "time"
    ylabel = "probability"
    title = f'CDF for Interval={10**(-int(number) - 1)}'
    fig_name = f'ping5-{number}.png'

    t = np.loadtxt(filename, delimiter=" ", dtype="float")
    x = np.sort(t)
    y = 1.00 * np.arange(len(t)) / (len(t) - 1)

    plt.plot(x,y)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.savefig(fig_name)
    plt.show()


if __name__ == "__main__":
    main()
