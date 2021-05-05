import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def plot(datapath, figpath):

    # Set up the axes.
    fig, ax = plt.subplots(figsize=(2.75, 2.25), constrained_layout=True)
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    for fn in (ax.axhline, ax.axvline):
        fn(0.0, color="black", linestyle=":", linewidth=1.0)

    # Plot the parabola.
    a = 2
    b = 1
    c = -2
    coeffs = [a, b, c]
    x = np.linspace(-2, 2, 1000)
    y = np.polyval(coeffs, x)
    ax.plot(x, y, color="black")

    # Highlight the roots.
    roots = np.roots(coeffs)
    ax.scatter(roots, np.zeros_like(roots), color="black")

    fig.savefig(figpath)


if __name__ == "__main__":
    _, datapath, figpath = sys.argv
    plot(datapath, figpath)
