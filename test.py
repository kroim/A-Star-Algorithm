import matplotlib.pyplot as plt
import numpy as np

x = [1, 2, 3, 4, 5]
y = [1, 2, 3, 4, 5]

fig, ax = plt.subplots(1, 1)
for i in range(len(x)):
    if i > 0:
        plt.plot([x[i-1], x[i]], [y[i-1], y[i]], color='#000')
for j in range(len(x)):
    plt.scatter(x[j], y[j], s=100, edgecolors='#000', facecolor='#000')
fig.show()

