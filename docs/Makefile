# PARAMETER (with default values)

# Directory which cointains the Makefile
SPHINX_EXEC_DIR			?= .

# Directory from which the sources will be read
SPHINX_SOURCE_DIR  		?= ../

# Directory which contains the builded files
SPHINX_OUTPUT_DIR   	?= ./output

# Args parsed to the sphinx-build command
SPHINXOPTS         		?= -c $(SPHINX_EXEC_DIR)

# CONSTANTS

# Sphinx build command
SPHINX_BUILD_COMMAND    = sphinx-build

# Directory which contains the auto generated files
SPHINX_GENERATED_DIR 	= $(SPHINX_OUTPUT_DIR)/../generated

# Directory which contains the extracted requirement files
SPHINX_REQUIREMENTS_DIR = $(SPHINX_EXEC_DIR)/requirements

.PHONY: help install copy-images apidoc remove-generated html generate extract-requirements Makefile

extract-requirements:
	@echo "Creating requirement files"
	bash ./scripts/extract-requirements.sh "$(SPHINX_EXEC_DIR)/requirements.yml" "$(SPHINX_REQUIREMENTS_DIR)/apt.txt" "$(SPHINX_REQUIREMENTS_DIR)/pip.txt"

# Copy images before running any Sphinx command (except for help)
copy-images:
	@echo "Copying images from ../assets/img/ to ./assets/img/..."
	cp -vr ../assets/img/* ./assets/img/

# Generate reStructuredText files from Python modules using sphinx-apidoc
generate-apidoc:
	@echo "Running sphinx-apidoc..."
	sphinx-apidoc -f -o $(SPHINX_GENERATED_DIR)/modules $(SPHINX_SOURCE_DIR)

generate-yaml-index:
	@echo "Generating YAML index..."
	python generators/yaml_index.py --source-dir $(SPHINX_SOURCE_DIR) --output-file $(SPHINX_GENERATED_DIR)/yaml_index.rst

generate-ansible-roles:
	@echo "Generating Ansible roles documentation..."
	python generators/ansible_roles.py --roles-dir $(SPHINX_SOURCE_DIR)/roles --output-dir $(SPHINX_GENERATED_DIR)/roles
	@echo "Generating Ansible roles index..."
	python generators/index.py --roles-dir generated/roles --output-file $(SPHINX_SOURCE_DIR)/roles/ansible_role_glosar.rst --caption "Ansible Role Glosar"
	
generate-readmes:	
	@echo "Create required README.md's for index..."
	python generators/readmes.py --generated-dir ./$(SPHINX_GENERATED_DIR)

generate: generate-apidoc generate-yaml-index generate-ansible-roles generate-readmes


remove-generated:
	@echo "Removing generated files..."
	- find $(SPHINX_GENERATED_DIR)/ -type f ! -name '.gitkeep' -delete

help:
	@$(SPHINX_BUILD_COMMAND) -M help "$(SPHINX_SOURCE_DIR)" "$(SPHINX_OUTPUT_DIR)" $(SPHINXOPTS) $(O)

html: copy-images generate
	@echo "Building Sphinx documentation..."
	$(SPHINX_BUILD_COMMAND) -M html "$(SPHINX_SOURCE_DIR)" "$(SPHINX_OUTPUT_DIR)" $(SPHINXOPTS)

just-html:
	@$(SPHINX_BUILD_COMMAND) -M html "$(SPHINX_SOURCE_DIR)" "$(SPHINX_OUTPUT_DIR)" $(SPHINXOPTS)


clean: remove-generated
	@$(SPHINX_BUILD_COMMAND) -M clean "$(SPHINX_SOURCE_DIR)" "$(SPHINX_OUTPUT_DIR)" $(SPHINXOPTS) $(O)

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option. $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINX_BUILD_COMMAND) -M $@ "$(SPHINX_SOURCE_DIR)" "$(SPHINX_OUTPUT_DIR)" $(SPHINXOPTS) $(O)
