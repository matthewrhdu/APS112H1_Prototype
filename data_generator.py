from numpy import sin, radians, pi
from random import randint

# interval = []
# for n in range(1, 6):
#     file = open(f"data{n}.csv", 'w')
#     const = randint(0, 100) / 20
#     start = randint(60, 200)
#     while start in interval:
#         start = randint(0, 100)
#     end = start + 3
#     interval.append(start)
#     interval.extend([i for i in range(start - 10, start + 10)])
#     s = ''
#     for i in range(1000):
#         if start < i < end:
#             val = 1
#         else:
#             val = 5 + const
#         s += f"{val}\n"
#
#     file.write(s)
#     file.close()

for n in range(1, 6):
    file = open(f"data{n}.csv", 'w')
    const = randint(0, 100) / 20
    s = ''
    for i in range(1000):
        val = const + sin(radians(360) / 40 * i)
        s += f"{val}\n"

    file.write(s)
    file.close()

