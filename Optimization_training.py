import pandas
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
import tkinter as tk
from tkinter import filedialog

#global variables
weight = 1
x_name = None
y_name = None
x_column = None
y_column = None
val_x = None
val_y = None
min_x = None
max_x = None
line_x = None
slope = None
intercept = None
filename = None
inputx = None
fig =None
ax =None
window2= None

def lost_one(a, deg):
    return a+(deg*weight)

def lost_two(a,b,deg):
    return (a-b)^2

def train():
    global ax, filename
    df = pandas.read_excel(filename)

    #get column names
    x_name = df.columns[0]
    y_name = df.columns[1]
    ax.set_xlabel(x_name)
    ax.set_ylabel(y_name)
    #create x and y coodinate list
    global x_column, y_column
    x_column = df[x_name].tolist()
    y_column = df[y_name].tolist()


def makegraph():
    #import global variable
    global min_x, max_x, slope, intercept

    #scatter graph
    plt.scatter(x_column,y_column, c ="blue")

    # get min and max for x-axis
    if (val_x != None):
        if(int(val_x) < min(x_column)):
            min_x = val_x
            if (int(val_x) > max(x_column)):
                max_x = int(val_x)
            else:
                max_x = max(x_column)
        else:
            min_x = min(x_column)
            if (int(val_x) > max(x_column)):
                max_x = int(val_x)
            else:
                max_x = max(x_column)
    else:
        min_x = min(x_column)
        max_x = max(x_column)

    #calculate slope and intercept
    (slope, intercept), (SSE,), *_ = np.polyfit(x_column, y_column, deg=1, full=True)

    # Plot the trend line.
    line_x = np.linspace(min_x, max_x+10, 200)
    plt.plot(line_x, slope * line_x + intercept, color='g')
    canvas.draw()

def plotprediction():
    global val_x, val_y, slope, intercept, prediction_input, min_x, max_x
    inputx = prediction_input.get()
    val_x= float(inputx)
    if (slope==None) or (intercept==None):
        print("Please input training data first")
    else:
        val_y = float((val_x*slope)+intercept)
        #add new point to scatter plot
        plt.scatter(val_x,val_y, c="red")

    canvas.draw()

def browseFiles():
    global filename, output_label
    filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("Text files",
                                                        "*.xlsx*"),
                                                       ("all files",
                                                        "*.*")))
    output_label = "File: "+ filename

def cleargraph():
    plt.cla()
    canvas.draw()

#main
show = True
window = tk.Tk()
prediction_input = tk.StringVar()
output_label = tk.StringVar()
output_label = "AI Prediction Graph"
window.config(background = "white")

label_file_explorer = tk.Label(window, 
                            text = output_label,
                            width = 100,
                            height = 2, 
                            fg = "blue"
                            ).grid(row=2,column=0, columnspan=4)

fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=window)
canvas.get_tk_widget().grid(row=0, columnspan=4)
toolbar = NavigationToolbar2Tk(canvas, pack_toolbar = False)
toolbar.grid(row=1, columnspan=4)

button_explore = tk.Button(window, 
                        text = "Browse Files",
                        command = browseFiles
                        ).grid(row=3,column=0)

train_model = tk.Button(
    window,
    text= "Train Model",
    command= train
).grid(row=4,column=0)

plot_graph = tk.Button(
    window,
    text= "Plot Graph",
    command= lambda: [makegraph()]
).grid(row=3,column=1)

clear_graph = tk.Button(
    window,
    text= "Clear Graph",
    command= lambda: [cleargraph()]
).grid(row=4,column=1)

prediction_entry = tk.Entry(
    window,
    fg="gray", 
    width = 20,
    textvariable = prediction_input
).grid(row=3,column=2)

prediction_btn = tk.Button(
    window,
    text= "Make Prediction",
    command = plotprediction
).grid(row=4,column=2)

window.mainloop()