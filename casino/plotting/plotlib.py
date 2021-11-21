import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def plot_two_dim_value_func(val_func: dict, title: str, x_label: str, y_label: str, z_label: str, z_lim: int, fname: str, flip_xy=False,):
    """Plot a 2D value function

    Args:
        val_func (dict): the value function (2D tuple keys, 1D integer value)
        title (str): the title
        x_label (str): the x label for the plot
        y_label (str): the y label
        z_label (str): the z label
        fname (str): the file name for saving
    """
    idx1 = 0
    idx2 = 1
    if flip_xy:
        idx1 = 1
        idx2 = 0
        swp_lbl = x_label
        x_label = y_label
        y_label = swp_lbl

    min_x = min(k[idx1] for k in val_func.keys())
    max_x = max(k[idx1] for k in val_func.keys())
    min_y = min(k[idx2] for k in val_func.keys())
    max_y = max(k[idx2] for k in val_func.keys())

    x_range = np.arange(min_x, max_x + 1)
    y_range = np.arange(min_y, max_y + 1)
    x_vals, y_vals = np.meshgrid(x_range, y_range)

    # Find value for all (x, y) coordinates
    z_vals = np.apply_along_axis(lambda _: val_func[(_[idx1], _[idx2])] if (_[idx1], _[idx2]) in val_func else 0, 2, np.dstack([x_vals, y_vals]))
    plot_surface(x_vals, y_vals, z_vals, title, x_label, y_label, z_label, z_lim, fname)

def plot_surface(x_vals, y_vals, z_vals, title, x_label: str, y_label: str, z_label: str, z_lim: int, fname: str):
    fig = plt.figure(figsize=(20, 10))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_wireframe(x_vals, y_vals, z_vals, rstride=1, cstride=1)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_zlabel(z_label)
    ax.set_zlim(0,z_lim)
    ax.set_title(title)
    plt.savefig(fname)

def line_plot(x_vals, y_vals, title, x_label, y_label, fname: str):
    fig = plt.figure(figsize=(20,10))
    ax = fig.add_subplot(111)
    ax.plot(x_vals, y_vals)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)
    plt.savefig(fname)