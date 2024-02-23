import pandas
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
import tkinter as tk
from tkinter import filedialog

#global variables
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

def lost_one(act, pred):
    return act-pred

def lost_two(act,pred):
    return (act-pred)^2

def train():
    global ax, filename, x_name, y_name
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
    global min_x, max_x, slope, intercept,ax, val_x

    #scatter graph
    ax.scatter(x_column,y_column, c ="blue")

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

    #set x and y axis label
    if x_name and y_name != None:
        ax.set_xlabel(x_name)
        ax.set_ylabel(y_name)
    #calculate slope and intercept
    (slope, intercept), (SSE,), *_ = np.polyfit(x_column, y_column, deg=1, full=True)

    # Plot the trend line.
    line_x = np.linspace(min_x, max_x+10, 200)
    ax.plot(line_x, slope * line_x + intercept, color='g')
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
        ax.scatter(val_x,val_y, c="red")

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
    global ax, val_x
    ax.cla()
    val_x = None
    canvas.draw()

def optimizer():
    #create new optimizer window
    optimizer = tk.Tk()
    optimizer.geometry("600x600")
    optimizer.configure(background="white")
    optimizer.title("Optimizer")
    opt_label = tk.Label(
                        optimizer, 
                        width = 70,
                        height = 2,
                        font=16,
                        fg = "black",
                        text="Optimizer").pack()
    fig1, ax1 = plt.subplots()
    canvas1 = FigureCanvasTkAgg(fig1, master=optimizer)

    canvas1.get_tk_widget().pack()
    toolbar1 = NavigationToolbar2Tk(canvas1, pack_toolbar = False)
    toolbar1.pack(padx=2,pady=2)

    #optimize training data
    global x_column, y_column, x_name,y_name, slope,intercept
    lost_array = []
    for a in x_column:
        predicted = (a*slope)+intercept
        actual = y_column[x_column.index(a)]
        lost_array.append(lost_one(actual,predicted))
    ax1.scatter(x_column,lost_array)
    z = np.polyfit(x_column, lost_array, 3)
    f = np.poly1d(z)
    x = np.linspace(min(x_column), max(x_column),50)
    y = f(x)
    ax1.plot(x_column,lost_array,'o', x, y)
    ax1.xlim([x_column[0]-1, x_column[-1] + 1 ])

#main
window = tk.Tk()
prediction_input = tk.StringVar()
output_label = tk.StringVar()
output_label = "AI Prediction Graph"
window.config(background = "white")
window.title("AI Optimizer")

label_file_explorer = tk.Label(window, 
                            text = output_label,
                            width = 70,
                            height = 2,
                            font=16,
                            fg = "black"
                            ).grid(row=0,column=0, columnspan=4)

fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=window)
canvas.get_tk_widget().grid(row=1, columnspan=4)
toolbar = NavigationToolbar2Tk(canvas, pack_toolbar = False)
toolbar.grid(row=2, columnspan=4, padx=5,pady=5)

button_explore = tk.Button(window, 
                        text = "Browse Files",
                        command = browseFiles
                        ).grid(row=3,column=0, padx=2,pady=2)

train_model = tk.Button(
    window,
    text= "Train Model",
    command= train
).grid(row=4,column=0, padx=2,pady=2)

plot_graph = tk.Button(
    window,
    text= "Plot Graph",
    command= lambda: [makegraph()]
).grid(row=3,column=1,padx=2,pady=2)

clear_graph = tk.Button(
    window,
    text= "Clear Graph",
    command= lambda: [cleargraph()]
).grid(row=4,column=1,padx=2,pady=2)

prediction_entry = tk.Entry(
    window,
    fg="gray", 
    width = 20,
    textvariable = prediction_input
).grid(row=3,column=2,padx=2,pady=2)

prediction_btn = tk.Button(
    window,
    text= "Make Prediction",
    command = plotprediction
).grid(row=4,column=2,padx=2,pady=2)

prediction_btn = tk.Button(
    window,
    text= "Optimize",
    font= 12,
    command = optimizer
).grid(row=3,rowspan=2, column=3,padx=2,pady=2)

window.protocol("WM_DELETE_WINDOW", window.quit)
window.mainloop()