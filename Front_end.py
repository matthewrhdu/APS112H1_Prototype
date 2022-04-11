from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import pyplot as plt, animation
import csv
from PIL import ImageTk,Image
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# To send warning emails
gmailUser = 'aps112team144@gmail.com'
gmailPassword = 'tutorial0126'
recipients = ['team144test1@gmail.com', 'team144test2@gmail.com']
time_under_threshold = [0, 0, 0, 0, 0]

# Global vars
threshold = 2
img = None

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
image_canvas = Canvas(root, width=(min(screen_width, screen_height)-50), height=(min(screen_width, screen_height)-50))
image_canvas.grid(row = 2, column = 0)

# Safety description
lbl_image = Label(root, justify="center", text="", font=("Arial", 25))
lbl_image.grid(row=3, column=0)

# Setting up the graph
fig = plt.Figure(figsize=(min(screen_width, screen_height) / 100, min(screen_width, screen_height) / 100), dpi=100)
ax = fig.add_subplot(xlim=(0, 60), ylim=(0, 10))
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
canvas.get_tk_widget().grid(row = 2, column = 1, rowspan=2)


# Opens a csv file into a list
def read_csv(file_name, index):
    y_vals = []
    with open(file_name, newline="") as file:
        reader = csv.reader(file, delimiter=' ', quotechar='|')
        for row in reader:
            num = row[0]
            num = round(float(num),2)
            y_vals.append(num)
    return y_vals[index : index+60]

# Animates the graph
def animate(i):
    global threshold
    global time_under_threshold

    # Reads data
    x = [j for j in range(60)]
    y = read_csv("data1.csv", i)
    y2 = read_csv("data2.csv", i)
    y3 = read_csv("data3.csv", i)
    y4 = read_csv("data4.csv", i)
    y5 = read_csv("data5.csv", i)

    # Updates the lines
    threshold_line.set_data(x, [threshold for _ in range(60)])
    line.set_data(x, y)
    line2.set_data(x, y2)
    line3.set_data(x, y3)
    line4.set_data(x, y4)
    line5.set_data(x, y5)

    # Determine which picture to load
    global img
    values = [y[-1], y2[-1], y3[-1], y4[-1], y5[-1]]

    global time_under_threshold
    safe, units = is_safe(values)

    if safe:
        # Change the picture
        img = Image.open("thumbsup.jpg")
        lbl_image["text"] = "The library is SAFE"
        time_under_threshold = [0,0,0,0,0]
    else:
        # Change the picture
        img = Image.open("exclaim.jpg")
        lbl_image["text"] = "The library is NOT SAFE"
    
        # Sending a warning email
        for i, x in enumerate(units):
            # Record time under threshold
            if x == 1:
                time_under_threshold[i] += 1
            else:
                time_under_threshold[i] = 0

            # Decide which message to send
            if time_under_threshold[i] == 1:
                message = "Warning, unit " + str(i + 1) + " has gone under the threshold for safe air exchange."

                msg = MIMEMultipart()
                msg['From'] = f'"Team 144" <{gmailUser}>'
                msg['To'] = ", ".join(recipients)
                msg['Subject'] = "Riverdale Air Exchange Warning"
                msg.attach(MIMEText(message))

                try:
                    mailServer = smtplib.SMTP('smtp.gmail.com', 587)
                    mailServer.ehlo()
                    mailServer.starttls()
                    mailServer.ehlo()
                    mailServer.login(gmailUser, gmailPassword)
                    mailServer.sendmail(gmailUser, recipients, msg.as_string())
                    mailServer.close()
                    print ('Email sent!')
                except:
                    print ('Something went wrong...')
            elif time_under_threshold[i] == 10:
                message = "URGENT, unit " + str(i + 1) + " has gone under the threshold for safe air exchange for over 10 minutes."
                
                msg = MIMEMultipart()
                msg['From'] = f'"Team 144" <{gmailUser}>'
                msg['To'] = ", ".join(recipients)
                msg['Subject'] = "Riverdale Air Exchange URGENT Warning"
                msg.attach(MIMEText(message))

                try:
                    mailServer = smtplib.SMTP('smtp.gmail.com', 587)
                    mailServer.ehlo()
                    mailServer.starttls()
                    mailServer.ehlo()
                    mailServer.login(gmailUser, gmailPassword)
                    mailServer.sendmail(gmailUser, recipients, msg.as_string())
                    mailServer.close()
                    print ('Email sent!')
                except:
                    print ('Something went wrong...')

    resized_image = img.resize((min(screen_width, screen_height)-50,min(screen_width, screen_height)-50))

    img = ImageTk.PhotoImage(resized_image)

    # Load the image
    image_canvas.create_image(0,0, image = img, anchor="nw")

    return line, line2, line3, line4, line5,


# Check if values are above the threshold
def is_safe(values):
    global threshold
    times = [0,0,0,0,0]
    safe = True
    for i, value in enumerate(values):
        if value < threshold:
            times[i] += 1
            safe = False
    return safe, times


# Graph animation
anim = animation.FuncAnimation(fig, animate, interval=50, blit=True)

mainloop()