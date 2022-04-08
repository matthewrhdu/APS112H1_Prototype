import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from typing import Dict, List

X_VALUES = 'x_value'

names = ["data1.csv", "data2.csv", "data3.csv", "data4.csv", "data5.csv"]
lc = {
    "data1.csv": "b-",
    "data2.csv": "y-",
    "data3.csv": "g-",
    "data4.csv": "r-",
    "data5.csv": "-"
}


x_vals = []
y_vals = []

index = 0


def read_csv(data: str) -> Dict[str, List[List[float]]]:
    read_dict = {name_id: [[], []] for name_id in names}
    file = open(data, 'r')

    line = file.readline()
    while line != '':
        s_line = line.split(sep=" ")
        name, data = s_line
        val, t = data.split(sep=",")
        read_dict[name][0].append(int(t))
        read_dict[name][1].append(float(val[:-1]))

        # Sets the boundaries to only show 60 data points
        if len(read_dict[name][0]) > 60:
            read_dict[name][0].pop(0)
            read_dict[name][1].pop(0)

        line = file.readline()
    return read_dict


def animate(i):
    data = read_csv('database.db')
    plt.cla()
    plt.ylim((-50, 50))

    for item in data:
        x_dat = data[item][0]
        y_dat = data[item][1]
        plt.plot(x_dat, y_dat, lc[item], label=item)
    plt.legend(loc='upper left')


if __name__ == "__main__":
    ani = FuncAnimation(plt.gcf(), animate, interval=20)
    plt.show()
