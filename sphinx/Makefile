# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment
SPHINXOPTS    		?= -c .
SPHINXBUILD   		?= sphinx-build
SPHINX_SOURCE_DIR	?= ../
SPHINX_BUILD_DIR 	?= ../docs

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SPHINX_SOURCE_DIR)" "$(SPHINX_BUILD_DIR)" $(SPHINXOPTS) $(O)

.PHONY: help install Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SPHINX_SOURCE_DIR)" "$(SPHINX_BUILD_DIR)" $(SPHINXOPTS) $(O)
