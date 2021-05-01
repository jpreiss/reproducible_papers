# reproducible_papers


## What it does

This repository provides a framework for fully reproducible academic papers.
Even though **no figures or computational results are committed to the repository**,
anyone can generate an exact copy of your published `.pdf` with the following steps<sup>†</sup>:

	git clone paper_repo
	cd paper_repo
	conda env create -f environment.yml
	conda activate paper_env
	make

Since we use Makefiles to express dependencies, you can update figures in your document automatically when any of the relevant code or data changes.

A few other convenient features are included:

- Generate abridged and extended versions from the same `.tex` files
  using environment variables and conditional compilation.
- Strip comments and generate a `.zip` file for arXiv upload.

† We assume a Unix-like system with Anaconda and LaTeX installed.


## How it works

This is a low-tech solution using directory layout conventions and Makefile pattern rules.
Your project is laid out like:

    src/     : Source code for computations and figures.
    tex/     : LaTeX code for the paper.
    inputs/  : Data sets from "the world" -- not your own computational results.

The results are stored like:

    data/    : Computational results, optionally using /inputs/.
    figures/ : Plots, produced from files in /data/.
    build/   : Final .pdf file and .zip file for arXiv.

The Makefile pattern rules implement the following dependency structure:

    inputs/figname/* -----
                          \
    src/figname_data.py -----> data/figname.feather -----> figs/figname.pgf
                                                      /
    src/figname_plot.py ------------------------------

The main functions in `figname_data.py` and `figname_plot.py`
must follow particular command-line argument conventions --
see the included example for details.


**Notes:**

- The Makefile applies these patterns in an "opt-in" way
  based on the list `figs`, which you must edit every time you add a figure.
  Any file that isn't part of `figs` and/or doesn't follow the
  `_data.py` or `_plot.py` naming conventions is ignored.
  Therefore, your library code and other intermediate data can be stored however you wish.

- The figure format is controlled by the variable `FIGEXT` in the Makefile.
  The default is `.pgf`. This format works very nicely with LaTeX,
  but it is not easily viewed as a standalone document.
  Change `FIGEXT` to your preferred format if desired.

- The data format is controlled by the variable `DATAEXT` in the Makefile.
  The default is `.feather`, but this was mostly an arbitrary choice.

- All files in `data/` are marked as `.PRECIOUS` in the Makefile,
  so they will not be deleted even though they are intermediate results.

- Adding your own non-pattern rules to the Makefile can be useful.
  For example, projects using symbolic math might want to add
  a build step that generates a `.tex` file.
  Projects with very slow multi-stage computations might want to add
  files to store intermediate results before `data/figname.feather`.

- If your project contains a very large amount of source code,
  it may be better to create a new library-like repository
  and include it as a git submodule in `src/`.


## Extra features

- The included `tex/preamble.tex` contains the implementation of
  conditional compilation based on the environment variable `ABRIDGED`.
  See the example `tex/reproducible.tex` for usage.

- The default `make` target is the unabridged/extended version.
  To build the abridged version, run
  `make abridged_build/reproducible.pdf`.
  It will set the environment variable for you and store the result separately.

- To package the arXiv source code for the unabridged version,
  run `make build/arxiv.zip`.
