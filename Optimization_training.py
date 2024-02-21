import pandas
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk

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

def lost_one(a, deg):
    return a+(deg*weight)

def lost_two(a,b,deg):
    return (a-b)^2

def train():
    df = pandas.read_excel("import\import.xlsx")

    #get column names
    x_name = df.columns[0]
    y_name = df.columns[1]

    #create x and y coodinate list
    global x_column, y_column
    x_column = df[x_name].tolist()
    y_column = df[y_name].tolist()

    # print(x_column)
    # print(y_column)

def makegraph():
    #scatter graph
    plt.scatter(x_column,y_column, c ="blue")
    plt.xlabel(x_name)
    plt.ylabel(y_name)

    # get min and max
    if(int(val_x) < min(x_column)):
        global min_x
        min_x = val_x
    else:
        min_x = min(x_column)

    max_x = max(x_column)
    # coord = list(zip(x_column,y_column))
    global slope, intercept
    (slope, intercept), (SSE,), *_ = np.polyfit(x_column, y_column, deg=1, full=True)

    # Plot the trend line.
    line_x = np.linspace(0, max_x+10, 200)
    plt.plot(line_x, slope * line_x + intercept, color='r')

def prediction():
    global val_x
    inputx = input("Enter Value to Predict: ")
    val_x= float(inputx)

train()
prediction()
makegraph()

val_y = float((val_x*slope)+intercept)
print(slope)
print(intercept)
print(val_y)

#add new point to scatter plot
plt.scatter(val_x,val_y, c="red")

#make x axis range

plt.show()
plt.close()

window = tk.Tk()