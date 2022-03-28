import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from typing import Dict, List

X_VALUES = 'x_value'
TOTALS_1 = 'totals_1'
NAMES = 'names'


x_vals = []
y_vals = []

index = 0


def read_csv(data: str) -> Dict[str, List[float]]:
    read_dict = {TOTALS_1: [], X_VALUES: [], NAMES: []}
    file = open(data, 'r')

    line = file.readline()
    n = 0
    while line != '':
        s_line = line.split(sep=" ")

        if s_line[0] not in read_dict[NAMES]:
            read_dict[NAMES].append(s_line[0])
        read_dict[TOTALS_1].append(float(s_line[1][:-1]))
        read_dict[X_VALUES].append(n)

        # Sets the boundaries to only show 60 data points
        if n > 60:
            read_dict[TOTALS_1].pop(0)
            read_dict[X_VALUES].pop(0)

        n += 1
        line = file.readline()
    return read_dict


def animate(i):
    data = read_csv('database.db')

    x = data[X_VALUES]
    y1 = data[TOTALS_1]

    plt.cla()
    plt.ylim((-10, 10))
    if len(x) < 60:
        plt.xlim((0, 60))
    plt.plot(x, y1, label="data1.csv")
    plt.legend(loc='upper left')


ani = FuncAnimation(plt.gcf(), animate, interval=20)

plt.show()
