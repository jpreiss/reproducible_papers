import sys

import numpy as np
import pandas as pd


def taylor_series(x, derivs):
    y = np.zeros_like(x)
    s = 1.0
    for i, d in enumerate(derivs):
        y += s * derivs[i] * (x ** i)
        s /= (i + 1)
    return y


def main(outpath, inpath):

    records = []
    xs = np.linspace(-np.pi, np.pi, 100)
    max_order = 5

    for x, y in zip(xs, np.sin(xs)):
        records.append({
            "x": x,
            "y": y,
            "order": "exact",
        })

    sine_derivs = np.loadtxt(inpath + "/sine_derivatives.csv")

    for order in range(1, max_order + 1, 2):
        ys = taylor_series(xs, sine_derivs[:(order+1)])
        for x, y in zip(xs, ys):
            records.append({
                "x": x,
                "y": y,
                "order": str(order),
            })

    df = pd.DataFrame(records)
    df.to_feather(outpath)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
