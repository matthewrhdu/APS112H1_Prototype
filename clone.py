from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import pyplot as plt, animation
import csv
from PIL import ImageTk,Image
from typing import Dict, List

# Global vars
threshold = 2
img = None
names = ["data1.csv", "data2.csv", "data3.csv", "data4.csv", "data5.csv"]
lc = {
    "data1.csv": "b-",
    "data2.csv": "y-",
    "data3.csv": "g-",
    "data4.csv": "r-",
    "data5.csv": "-"
}

# Create tkinter window
root = Tk()
root.title('Riverdale Library Air Exchange Rate')
screen_width = int(root.winfo_screenwidth() / 2)
screen_height = int(root.winfo_screenheight() / 3 * 2)

# Labels for headings
lbl_intro = Label(root, justify="left", text="Riverdale Library Air Exchange Rate", font=("Arial", 25)).grid(column=0, row=0)
lbl_safe = Label(root, justify="right", text="What is safe?", font=("Arial", 25)).grid(column=1, row=0)

# Labels for descriptions
lbl_intro_desc = Label(root, justify="center", wraplength=500, text="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum").grid(column=0, row=1)
lbl_safe_desc = Label(root, justify="center", wraplength=500, text="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum").grid(column=1, row=1)

# The canvas for the image
image_canvas = Canvas(root, width=min(screen_width, screen_height), height=min(screen_width, screen_height))
image_canvas.grid(row = 2, column = 0)

# Setting up the graph
fig = plt.Figure(figsize=(min(screen_width, screen_height) / 100, min(screen_width, screen_height) / 100), dpi=100)
ax = fig.add_subplot(xlim=(0, 60), ylim=(-55, 55))
ax.set_title('Riverdale Air Exchange Rate')
ax.set_xlabel('Last 60 minutes')
ax.set_ylabel('Air changes per hour')

# Adding lines to the graph
threshold_line, = ax.plot([], [], ':', lw=2, label="Threshold")
line, = ax.plot([], [], lw=2, label="Unit 1")
line2, = ax.plot([], [], lw=2, label="Unit 2")
line3, = ax.plot([], [], lw=2, label="Unit 3")
line4, = ax.plot([], [], lw=2, label="Unit 4")
line5, = ax.plot([], [], lw=2, label="Unit 5")

# Set legend
ax.legend()

# The canvas for the graph
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().grid(row = 2, column = 1)


# # Opens a csv file into a list
# def read_csv(file_name, index):
#     y_vals = []
#     with open(file_name, newline="") as file:
#         reader = csv.reader(file, delimiter=' ', quotechar='|')
#         for row in reader:
#             num = row[0]
#             num = round(float(num),2)
#             y_vals.append(num)
#     return y_vals[index : index+60]


def read_csv(data: str) -> Dict[str, List[List[float]]]:
    read_dict = {name_id: [[], []] for name_id in names}
    file = open(data, 'r')

    line = file.readline()
    while line != '':
        s_line = line.split(sep=" ")
        name, data = s_line
        val, t = data.split(sep=",")
        read_dict[name][0].append(int(t[:-1]))
        read_dict[name][1].append(float(val))

        # Sets the boundaries to only show 60 data points
        if read_dict[name][0][-1] > 60:
            read_dict[name][0].pop()
            read_dict[name][1].pop(0)

        line = file.readline()
    return read_dict


# Animates the graph
def animate(i):
    global threshold

    data = read_csv('database.db')

    # Reads data
    # x = [j for j in range(60)]
    # y = read_csv("data1.csv", i)
    # y2 = read_csv("data2.csv", i)
    # y3 = read_csv("data3.csv", i)
    # y4 = read_csv("data4.csv", i)
    # y5 = read_csv("data5.csv", i)

    y = data[names[0]][1]
    y2 = data[names[1]][1]
    y3 = data[names[2]][1]
    y4 = data[names[3]][1]
    y5 = data[names[4]][1]

    # Updates the lines
    threshold_line.set_data([j for j in range(60)], [threshold for _ in range(60)])
    line.set_data(data[names[0]][0], y)
    line2.set_data(data[names[1]][0], y2)
    line3.set_data(data[names[2]][0], y3)
    line4.set_data(data[names[3]][0], y4)
    line5.set_data(data[names[4]][0], y5)

    # Determine which picture to load
    global img
    values = y + y2 + y3 + y4 + y5
    if is_safe(values):
        img = Image.open("thumbsup.jpg")
    else:
        img = Image.open("exclaim.jpg")

    resized_image = img.resize((min(screen_width, screen_height),
                                min(screen_width, screen_height)))

    img = ImageTk.PhotoImage(resized_image)

    # Load the image
    image_canvas.create_image(0,0, image = img, anchor="nw")

    return line, line2, line3, line4, line5,


# Check if values are above the threshold
def is_safe(values):
    global threshold
    for value in values:
        if value < threshold:
            return False
    return True


# Graph animation
anim = animation.FuncAnimation(fig, animate, interval=20, blit=True)

root.mainloop()
# anim.save(filename="test.mp4")
