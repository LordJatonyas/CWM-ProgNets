# !/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt

# parameters to modify
filename="ping5-1.log"
label='label'
xlabel = 'time'
ylabel = ''
title='CDF for Interval=0.01'
fig_name='ping5-1.png'


t = np.loadtxt(filename, delimiter=" ", dtype="float")
np.transpose(t)
freq_dict = dict()
for time in t:
    if time not in freq_dict:
        freq_dict[time] = 1
    else:
        freq_dict[time] += 1

times = []
freqs = []
for time, iterations in freq_dict.items():
    times.append(time)
    freqs.append(iterations)

plt.plot(times, freqs,label=label)  # Plot some data on the (implicit) axes.
plt.xlabel(xlabel)
plt.ylabel(ylabel)
plt.title(title)
plt.legend()
plt.savefig(fig_name)
plt.show()
