# Makefile for j2render

TEMPLATE=./templates/vars/applications.yml.j2
OUTPUT=./group_vars/all/07_applications.yml

build:
	@echo "🔧 Building rendered file from $(TEMPLATE)..."
	@mkdir -p $(dir $(OUTPUT))
	j2r $(TEMPLATE) $(OUTPUT)
	@echo "✅ Output written to $(OUTPUT)"

install: build

test:
	python -m unittest discover -s tests/unit