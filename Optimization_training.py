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

def lost_one(a, deg):
    return a+(deg*weight)

def lost_two(a,b,deg):
    return (a-b)^2

def train():
    global ax
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

    # print(x_column)
    # print(y_column)
    print("model trained")


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
    print("graph plotted")

def plotprediction():
    global val_x, val_y, slope, intercept, prediction_input
    inputx = prediction_input.get()
    val_x= float(inputx)
    plt.clf()
    makegraph()
    if (slope==None) or (intercept==None):
        print("Please input training data first")
    else:
        val_y = float((val_x*slope)+intercept)
        #add new point to scatter plot
        plt.scatter(val_x,val_y, c="red")
    canvas.draw()
    print("prediction plotted")
    print(slope)
    print(intercept)

def browseFiles():
    global filename, output_label
    filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("Text files",
                                                        "*.xlsx*"),
                                                       ("all files",
                                                        "*.*")))
    output_label = "File: "+ filename

#main
show = True
window = tk.Tk()
prediction_input = tk.StringVar()
output_label = tk.StringVar()
output_label = "AI Prediction"
window.config(background = "white")

#graph window
window2 = tk.Tk()
graph_label = tk.Label(text = "Best Fit Graph", background="white", font=12, master=window2).pack()
fig, ax = plt.subplots()
plt.subplots_adjust(top =0.925)
canvas = FigureCanvasTkAgg(fig, master=window2)
canvas.get_tk_widget().pack()
tookbar = NavigationToolbar2Tk(canvas, pack_toolbar = False)

tookbar.pack(anchor = "center", fill = tk.X)

label_file_explorer = tk.Label(window, 
                            text = output_label,
                            width = 100,
                            height = 2, 
                            fg = "blue"
                            ).grid(row=0,column=0, columnspan=2)

button_explore = tk.Button(window, 
                        text = "Browse Files",
                        command = browseFiles
                        ).grid(row=1,column=0)

prediction_entry = tk.Entry(
    window,
    fg="gray", 
    width = 20,
    textvariable = prediction_input
).grid(row=1,column=1)

prediction_btn = tk.Button(
    window,
    text= "Make Prediction",
    command = plotprediction
).grid(row=2,column=1)

train_model = tk.Button(
    window,
    text= "Train Model",
    command= train
).grid(row=2,column=0)

show_graph = tk.Button(
    window,
    text= "Show Graph",
    command= lambda: [makegraph()]
).grid(row=3,column=0)


window.mainloop()