import sys

import sympy as sym
import pandas as pd


def main(outpath):

    x = sym.Symbol("x")
    y = sym.sin(x)
    n_derivs = 12
    derivs = []
    dy = y
    for i in range(n_derivs):
        val = float(dy.subs(x, 0))
        derivs.append(val)
        dy = sym.diff(dy, x)

    df = pd.DataFrame(dict(
        deriv=derivs
    ))
    df.to_feather(outpath)


if __name__ == "__main__":
    main(sys.argv[1])
