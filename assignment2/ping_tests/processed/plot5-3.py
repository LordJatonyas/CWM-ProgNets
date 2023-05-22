# !/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt

# parameters to modify
filename="ping5-3.txt"
label='label'
xlabel = 'time'
ylabel = 'frequency'
title='CDF for Interval=0.0001'
fig_name='ping5-3.png'


t = np.loadtxt(filename, delimiter=" ", dtype="float")
x = np.sort(t)
y = 1.00 * np.arange(len(t)) / (len(t) - 1)

plt.plot(x,y)  # Plot some data on the (implicit) axes.
plt.xlabel(xlabel)
plt.ylabel(ylabel)
plt.title(title)
plt.legend()
plt.savefig(fig_name)
plt.show()
