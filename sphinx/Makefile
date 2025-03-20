# Minimal Makefile for Sphinx documentation
#
# You can set these variables from the command line, and also
# from the environment
SPHINXOPTS         		?=	-c .
SPHINXBUILD        		?=	sphinx-build
SPHINX_SOURCE_DIR  		?=	../
SPHINX_BUILD_DIR   		?=	../docs
SPHINX_APIDOC_BUILD_DIR =	$(SPHINX_SOURCE_DIR)modules	 

.PHONY: help install copy-images apidoc remove-apidoc html Makefile

# Copy images before running any Sphinx command (except for help)
copy-images:
	@echo "Copying images from ../assets/img/ to ./assets/img/..."
	cp -vr ../assets/img/* ./assets/img/

# Generate reStructuredText files from Python modules using sphinx-apidoc
apidoc:
	@echo "Running sphinx-apidoc..."
	sphinx-apidoc -f -o $(SPHINX_APIDOC_BUILD_DIR) $(SPHINX_SOURCE_DIR)

remove-apidoc:
	@echo "Removing sphinx-apidoc files..."
	- rm -rv $(SPHINX_APIDOC_BUILD_DIR)

# "help" target does not copy images
help:
	@$(SPHINXBUILD) -M help "$(SPHINX_SOURCE_DIR)" "$(SPHINX_BUILD_DIR)" $(SPHINXOPTS) $(O)

# HTML target depends on apidoc so that sphinx-apidoc runs first
html: copy-images
	@$(SPHINXBUILD) -M html "$(SPHINX_SOURCE_DIR)" "$(SPHINX_BUILD_DIR)" $(SPHINXOPTS) $(O)

clean: remove-apidoc
	@$(SPHINXBUILD) -M html "$(SPHINX_SOURCE_DIR)" "$(SPHINX_BUILD_DIR)" $(SPHINXOPTS) $(O)

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option. $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SPHINX_SOURCE_DIR)" "$(SPHINX_BUILD_DIR)" $(SPHINXOPTS) $(O)
