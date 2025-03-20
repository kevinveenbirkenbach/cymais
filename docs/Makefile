# Minimal Makefile for Sphinx documentation
#
# You can set these variables from the command line, and also
# from the environment
SPHINXOPTS         		?=	-c .
SPHINXBUILD        		?=	sphinx-build
SPHINX_SOURCE_DIR  		?=	../
SPHINX_BUILD_DIR   		?=	./build
SPHINX_GENERATED_DIR 	=	./generated

.PHONY: help install copy-images apidoc remove-generated html Makefile

# Copy images before running any Sphinx command (except for help)
copy-images:
	@echo "Copying images from ../assets/img/ to ./assets/img/..."
	cp -vr ../assets/img/* ./assets/img/

# Generate reStructuredText files from Python modules using sphinx-apidoc
generate-apidoc:
	@echo "Running sphinx-apidoc..."
	sphinx-apidoc -f -o $(SPHINX_GENERATED_DIR)/modules $(SPHINX_SOURCE_DIR)

remove-generated:
	@echo "Removing generated files..."
	- find $(SPHINX_GENERATED_DIR)/ -type f ! -name '.gitkeep' -delete

generate-yaml-index:
	@echo "Generating YAML index..."
	python generators/yaml_index.py --source-dir $(SPHINX_SOURCE_DIR) --output-file $(SPHINX_GENERATED_DIR)/yaml_index.rst

generate-ansible-roles:
	@echo "Generating Ansible roles documentation..."
	python generators/ansible_roles.py --roles-dir $(SPHINX_SOURCE_DIR)/roles --output-dir $(SPHINX_GENERATED_DIR)/roles

# "help" target does not copy images
help:
	@$(SPHINXBUILD) -M help "$(SPHINX_SOURCE_DIR)" "$(SPHINX_BUILD_DIR)" $(SPHINXOPTS) $(O)

html: copy-images generate-apidoc generate-yaml-index generate-ansible-roles
	@$(SPHINXBUILD) -M html "$(SPHINX_SOURCE_DIR)" "$(SPHINX_BUILD_DIR)" $(SPHINXOPTS)


clean: remove-generated
	@$(SPHINXBUILD) -M html "$(SPHINX_SOURCE_DIR)" "$(SPHINX_BUILD_DIR)" $(SPHINXOPTS) $(O)

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option. $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SPHINX_SOURCE_DIR)" "$(SPHINX_BUILD_DIR)" $(SPHINXOPTS) $(O)
