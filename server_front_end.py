from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import pyplot as plt, animation
from PIL import ImageTk, Image
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
lbl_intro = Label(root, justify="left", text="Riverdale Library Air Exchange Rate", font=("Arial", 25))\
    .grid(column=0, row=0)
lbl_safe = Label(root, justify="right", text="What is safe?", font=("Arial", 25)).grid(column=1, row=0)

file1 = open("safe.txt", "r")
file2 = open("intro.txt", "r")

# Labels for descriptions
lbl_intro_desc = Label(root, justify="center", wraplength=500, text=file2.readline(), font=("Arial", 12))\
    .grid(column=0, row=1)
lbl_safe_desc = Label(root, justify="center", wraplength=500, text=file1.readline(), font=("Arial", 12))\
    .grid(column=1, row=1)

file1.close()
file2.close()

# The canvas for the image
image_canvas = Canvas(root, width=min(screen_width, screen_height), height=min(screen_width, screen_height))
image_canvas.grid(row=2, column=0)

# Safety description
lbl_image = Label(root, justify="center", text="", font=("Arial", 25))
lbl_image.grid(row=3, column=0)

# Setting up the graph
fig = plt.Figure(figsize=(min(screen_width, screen_height) / 100, min(screen_width, screen_height) / 100), dpi=100)
ax = fig.add_subplot(xlim=(0, 65), ylim=(-10, 10))
ax.set_title('Riverdale Air Exchange Rate')
ax.set_xlabel('Last 60 minutes')
ax.set_ylabel('Air changes per hour')

# Adding lines to the graph
threshold_line, = ax.plot([], [], ':', lw=2, label="Threshold")
line, = ax.plot([], [], lw=5, label="Unit 1")
line2, = ax.plot([], [], lw=5, label="Unit 2")
line3, = ax.plot([], [], lw=5, label="Unit 3")
line4, = ax.plot([], [], lw=5, label="Unit 4")
line5, = ax.plot([], [], lw=5, label="Unit 5")

# Set legend
ax.legend()

# The canvas for the graph
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().grid(row=2, column=1)


def read_csv(data: str) -> Dict[str, List[List[float]]]:
    read_dict = {name_id: [[], []] for name_id in names}
    file = open(data, 'r')

    read_line = file.readline()
    while read_line != '':
        s_line = read_line.split(sep=" ")
        name, data = s_line
        val, t = data.split(sep=",")

        int_time = int(t[:-1])

        if int_time > 60:
            for i in range(len(read_dict[name][0])):
                read_dict[name][0][i] -= 2
            read_dict[name][0].append(60)
        else:
            read_dict[name][0].append(int_time)
        read_dict[name][1].append(float(val))

        # Sets the boundaries to only show 60 data points
        if int_time > 60 and len(read_dict[name][0]) >= 60:
            read_dict[name][0].pop(0)
            read_dict[name][1].pop(0)

        read_line = file.readline()
    return read_dict


# Animates the graph
def animate(i):
    global threshold

    data = read_csv('database.db')

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
    values = [val[-1] for val in [y, y2, y3, y4, y5] if val]

    if is_safe(values):
        img = Image.open("thumbsup.jpg")
        lbl_image["text"] = "The library is SAFE"
    else:
        img = Image.open("exclaim.jpg")
        lbl_image["text"] = "The library is NOT SAFE"

    resized_image = img.resize((min(screen_width, screen_height),
                                min(screen_width, screen_height)))

    img = ImageTk.PhotoImage(resized_image)

    # Load the image
    image_canvas.create_image(0, 0, image=img, anchor="nw")

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
