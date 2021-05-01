# File extensions. Change these according to your preference.
FIGEXT = pgf
DATAEXT = feather

# Subroutines.
LATEXMK = latexmk -pdf -cd -interaction=nonstopmode

#
# Main pdf build.
#

# Unabridged paper.
build/reproducible.pdf: tex/*.tex figs
	$(LATEXMK) -outdir=../build tex/reproducible.tex

# Abridged paper.
abridged_build/reproducible.pdf: tex/*.tex figs
	ABRIDGED=true $(LATEXMK) -outdir=../abridged_build tex/reproducible.tex


#
# Source .zip for arXiv.
#

# Strip comments and unused bibliography from LaTeX source code for arXiv.
build/arxiv: build/reproducible.pdf build/reproducible.bbl
	rm -rf build/arxiv
	arxiv_latex_cleaner tex
	mv tex_arXiv build/arxiv
	cp -r figures build/arxiv/figures
	cp build/reproducible.bbl build/arxiv

# Zipping the arXiv source for upload.
build/arxiv.zip: build/arxiv
	rm -f build/arxiv.zip
	cd build/arxiv; zip -r ../arxiv.zip .


#
# Figures and data files.
#

# Tell Make about all figures manually. TODO: scrape .tex files?
.PHONY: figs

figs: \
figures/sine_taylor.$(FIGEXT) \

# Rules to make figures from data files.
# Figure-generating scripts should take the input data path and output image
# path as the two command-line args.
figures/%.$(FIGEXT): data/%.$(DATAEXT) src/%_plot.py
	python src/$*_plot.py data/$*.$(DATAEXT) $@

# Rule to make figure data files from code.
# Data-generating scripts should take output path as the last command-line arg.
# Each figure can optionally have a subdirectory of inputs as well, in which
#   case the directory path is passed as the second command-line arg.
# If multiple figures depend on the same input, use softlinks.
data/%.$(DATAEXT): src/%_data.py inputs/%/*
	python src/$*_data.py $@ inputs/$*

# Do not delete data files when done building downstream dependencies.
.PRECIOUS: data/%.$(DATAEXT)

# In case a data-generating script doesn't have any input data, don't complain.
inputs/%/*:


#
# Miscellaneous.
#

clean:
	rm -rf data/*
	rm -rf figures/*
	rm -rf build/*
	rm -rf abridged_build/*
