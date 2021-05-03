"""Example of generating LaTeX code from symbolic math results.

Consider a library like PyLaTeX if you want to generate many environments,
sections, etc. This basic string manipulation is adequate for one or two
mathematical statements.
"""


import sympy as sym


def main():
    a, b, c, x = sym.symbols("a, b, c, x")
    eqn = a * x**2 + b * x + c
    soln = sym.solve(eqn, x)[0]
    print(f"""\
One solution to the equation
\\[
    {sym.latex(eqn)} = 0
\\]
is
\\[
    x = {sym.latex(soln)}.
\\]""")


if __name__ == "__main__":
    main()
