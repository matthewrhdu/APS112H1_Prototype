from random import randint
import calculation_module as calc


def increment(value: float, target: int):
    if value > target:
        return value - 0.5
    elif value < target:
        return value + 0.5
    return value


for n in range(1, 6):
    file = open(f"data{n}.csv", 'w')
    s = ''

    curr_percentage = 1
    for i in range(1000):
        if 500 >= i >= 200:
            curr_percentage = increment(curr_percentage, 25)
        elif 750 >= i >= 500:
            curr_percentage = increment(curr_percentage, 50)
        elif 1000 >= i >= 750:
            curr_percentage = increment(curr_percentage, 99)
        else:
            curr_percentage = increment(curr_percentage, 1)
        val1 = curr_percentage + randint(-100, 100) / 100

        val2 = calc.reverse_rate(val1, (6 + randint(-1000, 1000) / 10000))
        s += f"{round(val1, 2)},{round(val2, 2)}\n"

    file.write(s)
    file.close()

