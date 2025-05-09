# Makefile for j2render

ROLES_DIR=./roles
OUTPUT=./group_vars/all/11_applications.yml
SCRIPT=./cli/generate_default_applications.py

build:
	@echo "🔧 Generating $(OUTPUT) from roles in $(ROLES_DIR)..."
	@mkdir -p $(dir $(OUTPUT))
	python3 $(SCRIPT) --roles-dir $(ROLES_DIR) --output-file $(OUTPUT)
	@echo "✅ Output written to $(OUTPUT)"

install: build

test:
	python -m unittest discover -s tests/unit