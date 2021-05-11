# reproducible papers

A "framework" (Makefile pattern rules + conventions) for fully reproducible academic papers.
Even though no figures or computational results are committed to the repository,
anyone can generate an exact copy of your published `.pdf` with the following steps<sup>†</sup>:

	git clone paper_repo
	cd paper_repo
	conda env create -f environment.yml
	conda activate paper_env
	make

Capturing the dependencies between LaTeX, figures, data, and code in a Makefile
and storing computational results on disk
ensures that the paper always reflects changes in the data and code
without requiring a full rebuild for every change.

A few other convenient features are included:

- Generate abridged and extended versions from the same `.tex` files
  using environment variables and conditional compilation.
- Strip comments and generate a `.zip` file for arXiv upload.

† We assume a Unix-like system with Anaconda and LaTeX installed.


## Directory structure

This is a low-tech solution using directory layout conventions and Makefile pattern rules.
The hand-written portion of your project is laid out like:

    input/   : Data sets from "the world" -- not your own computational results.
    src/     : Source code for computations, figures, and generated LaTeX.
    tex/     : Hand-written LaTeX code for the paper.

The computed results are laid out like:

    build/   : Final .pdf file and .zip file for arXiv.
    data/    : Computational results, optionally using /inputs/.
    figures/ : Plots, produced from files in /data/.
    tex/     : LaTeX generated from /data/ is added alongside hand-written files.


## Rules for generating figures and LaTeX

The Makefile pattern rules for figures implement the following dependency structure,
where `.data` is your chosen data file format
and `.img` is your chosen image file format:

                             src/x_fig.py --,
    src/x_data.py ---,                      |
                     |                   ,--+--> figures/x.img
     input/x.data --ANY--> data/x.data --+
                     |                   '--+--> tex/x_gen.tex
        <nothing> ---'                      |
                          src/x_gentex.py --'

Figure- and LaTeX-generating scripts always look for the
corresponding `x.data` file. We support three cases:

1) **Program-generated data:**
   If the script `src/x_data.py` exists, `make` will use it to generate `x.data`.
2) **Data from the outside world:**
   If `input/x.data` exists, `make` will copy it to `data/x.data`.
3) **No data needed to make figure/LaTeX:**
   If neither of the above conditions are satisfied,
   `make` will run the figure/LaTeX-generating script anyway.

#### Command-line arguments
Figure-generating scripts should take the input and output paths as command-line arguments:

    python src/x_data.py data/x.data figures/x.img

LaTeX-generating scripts should take the input path as the command-line argument and print to `stdout`:

    python src/x_gentex.py data/x.data > tex/x_gen.tex


#### Intermediate data
It may also be useful to generate data files from other data files, for example:

- Saving intermediate results in very slow computations.
- Building several plots/tables from one experiment.
- Parameterizing a data generation process, with parameters stored as input data.
- etc...

With data-to-data scripts there is no formula to derive the input file name from
the output file name. The user must write the rule manually in the Makefile.
This is demonstrated by the example `sine_taylor_data.py`.

#### List outputs explicitly
`make` will apply the figure- and LaTeX-generating rules in an "opt-in" way
based on the lists `figs` and `texs` in the Makefile. You must edit these
lists whenever you add a new figure or generated LaTeX file.

#### Controlling figure and data formats
The figure and data formats are controlled by the variables `FIGEXT` and
`DATAEXT` in the Makefile.

#### Data is precious
All files in `data/` are marked as `.PRECIOUS` in the Makefile, so they will
not be deleted even though they are
[intermediate files](https://www.gnu.org/software/make/manual/html_node/Chained-Rules.html).


## Abriged/Extended versions

The included `tex/preamble.tex` implements conditional compilation based on the
environment variable `ABRIDGED`. See the example `tex/reproducible.tex` for usage.

The default `make` target is the unabridged/extended version.
To build the abridged version, run `make abridged_build/reproducible.pdf`.
It will set the environment variable `ABRIDGED` and store the result separately.


## .zip generation for ArXiv

To package the source code for upload to arXiv, run `make build/arxiv.zip`.
The unabridged version is zipped. The LaTeX source files are passed through
[arxiv-latex-cleaner](https://github.com/google-research/arxiv-latex-cleaner)
to strip comments. The zipped package includes only the `.bbl` file generated
by BibTeX instead of the `.bib` files, so only the references you used in the
paper are included.


## Examples

Overall, there are six kinds of recipes this Makefile will run.
We provide examples of each:

| Input | Output | Description        | Example                  |
|:-----:|--------|--------------------|--------------------------|
| ---   | Data   | Data generation    | `sine_derivs_data.py`    |
| ---   | Figure | Figure generation  | `quadratic_roots_fig.py` |
| ---   | TeX    | TeX generation     | `quadratic_gentex.py`    |
| Data  | Data   | Processing         | `sine_taylor_data.py`    |
| Data  | Figure | Visualization      | `sine_taylor_fig.py`     |
| Data  | TeX    | Tables, etc.       | `sine_taylor_gentex.py`  |


## Tips

- If your project contains a lot of source code, it may be better to create a
  separate library-like repository and include it as a git submodule in `src/`.

- To help decouple the computation and plotting stages, we suggest storing all
  the data you *think you might need* in the
  ["tidy data"](https://tidyr.tidyverse.org/articles/tidy-data.html) layout.
  Plotting tools designed to consume "tidy" data make it easy to select and
  combine data to generate many different kinds of plots.

- For deterministic results,
  remember to seed random number generators with a constant.
