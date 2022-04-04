from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
import csv
from PIL import ImageTk,Image

index = 0
threshold = 2


def read_csv(file_name, index):
    y_vals = []
    with open(file_name, newline="") as file:
        reader = csv.reader(file, delimiter=' ', quotechar='|')
        for row in reader:
            num = row[0]
            num = round(float(num),2)
            y_vals.append(num)
            # if len(y_vals) > 60:
            #     y_vals.pop(0)
    return y_vals[index : index+60]


def is_safe(values, threshold):
    for value in values:
        if value < threshold:
            return False
    return True


# plot function is created for
# plotting the graph in
# tkinter window
def plot():
    global index
    global threshold
    # air exchange rates from each unit
    y = read_csv("data1.csv", index)
    y2 = read_csv("data2.csv", index)
    y3 = read_csv("data3.csv", index)
    y4 = read_csv("data4.csv", index)
    y5 = read_csv("data5.csv", index)

    # the figure that will contain the plot
    fig = Figure(figsize = (8, 5), dpi = 100)


    # adding the subplot
    plot1 = fig.add_subplot(111) 

    # plotting the graph
    plot1.set_title("Riverdale Library Air Exchange")
    plot1.set(xlabel="Last 60 Minutes", ylabel="Air Changes per Hour")
    plot1.plot(y, label="Unit 1")
    plot1.plot(y2, label="Unit 2")
    plot1.plot(y3, label="Unit 3")
    plot1.plot(y4, label="Unit 4")
    plot1.plot(y5, label="Unit 5")
    plot1.plot([threshold for _ in range(60)],':', label="Threshold")
    plot1.legend()

    for widgets in frame.winfo_children():
        widgets.destroy()

    # creating the Tkinter canvas
    # containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig, master = frame)
    canvas.draw()

    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().grid()

    values = y + y2 + y3 + y4 + y5
    
    global img

    if is_safe(values, threshold):
        img = Image.open("smile.png")
    else:
        img = Image.open("exclaim.png")

    resized_image = img.resize((500,500), Image.ANTIALIAS)

    img = ImageTk.PhotoImage(resized_image)

    canvas2.create_image(0,0, image = img, anchor="nw")

    index += 1
    
    window.after(1000, plot)

# the main Tkinter window
window = Tk()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# setting the title
window.title('Riverdale Air Exchange Rate')

# dimensions of the main window
# window.geometry(str(screen_width)+"x"+str(screen_height))

introduction = Frame(window)
introduction.grid(row=1, columnspan=3)

lbl_intro = Label(introduction, justify="left", text="Riverdale Library Air Exchange Rate", font=("Arial", 25)).grid(column=0, row=1)
lbl_safe = Label(introduction, justify="right", text="What is safe?", font=("Arial", 25)).grid(column=2, row=1)

lbl_intro_desc = Label(introduction, justify="left", wraplength=500, text="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum").grid(column=0, row=2)
lbl_safe_desc = Label(introduction, justify="right", wraplength=500, text="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum").grid(column=2, row=2)

frame1 = Frame(window)
frame1.grid(row=2, column=1)

frame = Frame(window)
frame.grid(row=2, column=2)

# image beside the plot
canvas2 = Canvas(frame1, width=500, height=500)

# place the image
# in the frame
canvas2.grid()

img = None

plot()

# run the gui
window.mainloop()
