import sys

import numpy as np
import pandas as pd


def gentex(datapath):

    # Read data.
    df = pd.read_feather(datapath)

    orders = set(df["order"].unique()) - {"exact"}

    # Pivot on Taylor order.
    df = df.pivot(index="x", columns="order", values="y")
    for order in orders:
        df[order] = (df[order] - df["exact"]).abs()

    del df["exact"]
    maxes = df.max().rename("max error").to_frame().reset_index()
    tex = maxes.to_latex(index=False, float_format="{:0.2f}".format)
    sys.stdout.write(tex)


if __name__ == "__main__":
    gentex(sys.argv[1])
