# Minimal Makefile for Sphinx documentation
#
# You can set these variables from the command line, and also
# from the environment
SPHINXOPTS         ?= -c .
SPHINXBUILD        ?= sphinx-build
SPHINX_SOURCE_DIR  ?= ../
SPHINX_BUILD_DIR   ?= ../docs

.PHONY: help install copy-images apidoc html Makefile

# Copy images before running any Sphinx command (except for help)
copy-images:
	@echo "Copying images from ../assets/img/ to ./assets/img/..."
	cp -r ../assets/img/* ./assets/img/

# Generate reStructuredText files from Python modules using sphinx-apidoc
apidoc:
	@echo "Running sphinx-apidoc..."
	sphinx-apidoc -f -o $(SPHINX_SOURCE_DIR)/modules $(SPHINX_SOURCE_DIR)

# "help" target does not copy images
help:
	@$(SPHINXBUILD) -M help "$(SPHINX_SOURCE_DIR)" "$(SPHINX_BUILD_DIR)" $(SPHINXOPTS) $(O)

# HTML target depends on apidoc so that sphinx-apidoc runs first
html: copy-images apidoc
	@$(SPHINXBUILD) -M html "$(SPHINX_SOURCE_DIR)" "$(SPHINX_BUILD_DIR)" $(SPHINXOPTS) $(O)

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option. $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SPHINX_SOURCE_DIR)" "$(SPHINX_BUILD_DIR)" $(SPHINXOPTS) $(O)
