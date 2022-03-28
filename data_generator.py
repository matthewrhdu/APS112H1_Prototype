from numpy import sin, radians, pi
from random import randint

for n in range(1, 6):
    file = open(f"data{n}.csv", 'w')
    k = 10
    s = ''
    for i in range(1000):
        val = k * n * sin(pi / 2 * radians(i))
        s += f"{val}\n"

    file.write(s)
    file.close()

