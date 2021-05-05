import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def plot(datapath, figpath):

    # Read data.
    df = pd.read_feather(datapath)

    # Remap code-oriented column names to plot-oriented names.
    X = "$\\theta$"
    Y = "$\\sin \\theta$"
    df[X] = df["x"]
    df[Y] = df["y"]

    # Make the main plot.
    sns.set_style("whitegrid")
    grid = sns.relplot(
        data=df,
        x=X,
        y=Y,
        hue="order",
        kind="line",
        height=1.8,
        aspect=1.6,
    )

    # Fix up some style details.
    grid.set(xlim=[-np.pi, np.pi], ylim=[-1.8, 1.8])
    sns.despine(left=True, bottom=True)

    # Write to file.
    plt.savefig(figpath)


if __name__ == "__main__":
    _, datapath, figpath = sys.argv
    plot(datapath, figpath)
