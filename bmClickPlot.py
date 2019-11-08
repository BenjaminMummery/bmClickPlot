import matplotlib.pyplot as plt
import numpy as np 
from matplotlib.widgets import RectangleSelector
import sys

"""
usage:
import bmclick
x = [<data>]
y = [<data>]
coords, ranges = click.plot(x, y)
"""

def onclick(event):
    global press
    # Get the x and y position of the click
    #click_x, click_y = event.xdata, event.ydata

    # Set the global press variable so that ondrag and onrelease knows the 
    # button is pressed
    press = event

    # Make the drag-box disappear
    [p.remove() for p in ax.patches]


def onrelease(event):
    global press, ranges, coords
    if press is not None:
        # Check if the release location is more than a few pixels from the click
        # location
        delta = np.sqrt((press.x-event.x)**2 +(press.y-event.y)**2)

        if delta <= 3: # small movement - assume click and store coords
            # Find the relevent data coordinates
            i_x, data_x = find_nearest(X, press.xdata)
            data_y = float(Y[i_x])

            # Add a dot to the plot at the click location
            ax.scatter(data_x, data_y, c='r', marker='x')
            fig.canvas.draw()

            # Store the coordinates
            print("click at: (%.2f, %.2f), found data at (%.2f, %.2f)" % (press.xdata, press.ydata, data_x, data_y))
            data = [press.xdata, press.ydata, data_x, data_y]
            if coords.sum()==0.:
                for i, val in enumerate(data):
                    coords[0,i] = val
            else:
                coords = np.vstack([coords, data])


        else:   # large movement - assume drag and store ranges
            # Find data that lies within selected range
            i_x_dn, data_x_dn = find_nearest(X, press.xdata)
            i_x_up, data_x_up = find_nearest(X, event.xdata)

            # Flip the indices (if box was drawn right-to-left)
            if i_x_dn > i_x_up: 
                tmp = i_x_dn
                i_x_dn = i_x_up
                i_x_up = tmp

            data_x = X[i_x_dn:i_x_up]
            data_y = Y[i_x_dn:i_x_up]

            # Highlight the selected data on the plot
            ax.plot(data_x, data_y, c='r')
            fig.canvas.draw()

            # Store the range
            print("press at %.2f, %.2f, release at %.2f, %.2f, total movement %.2f" % (press.xdata, press.ydata, event.xdata, event.ydata, delta))
            data = [i_x_dn, i_x_up]
            if ranges.sum()==0.:
                for i, val in enumerate(data):
                    ranges[0,i] = val
            else:
                ranges = np.vstack([ranges, data])
            
        press = None
        

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx, float(array[idx])


def line_select_callback(eclick, erelease):
    x1, y1 = eclick.xdata, eclick.ydata
    x2, y2 = erelease.xdata, erelease.ydata

    rect = plt.Rectangle((min(x1,x2),min(y1,y2)), np.abs(x1-x2), np.abs(y1-y2))
    ax.add_patch(rect)


def plot(x, y):
    global X, Y, ax, fig, coords, ranges, press, rs
    press = None
    X = x
    Y = y

    # Plot the data
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(x, y)

    # List to store coords
    coords = np.zeros((1,4))
    ranges = np.zeros((1,2))

    # Link mouse events to plot and onclick function
    A = fig.canvas.mpl_connect('button_press_event', onclick)
    B = fig.canvas.mpl_connect('button_release_event', onrelease)

    rs = RectangleSelector(ax, line_select_callback,
                       drawtype='box', useblit=True, button=[1], 
                       minspanx=5, minspany=5, spancoords='pixels', 
                       interactive=False, rectprops=dict(facecolor='blue', edgecolor='blue', alpha=0.2, fill=True))

    plt.show()

    return coords, ranges



def test():
    # Generate some data for testing
    test_x = np.sort(np.random.rand(1000, 1)*10, axis=0)
    test_y = np.sin(test_x)

    # Call plot to display clickably
    coords, ranges = plot(test_x, test_y)

    print("Coords (data values):")
    [print(vals) for vals in coords]
    print("Ranges (indices)")
    [print(vals) for vals in ranges]

    # Display the selected data


if __name__=="__main__":
    test()