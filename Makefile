ROLES_DIR         	:= ./roles
APPLICATIONS_OUT  	:= ./group_vars/all/11_applications.yml
APPLICATIONS_SCRIPT := ./cli/generate_defaults_applications.py
INCLUDES_OUT      	:= ./tasks/include-docker-roles.yml
INCLUDES_SCRIPT   	:= ./cli/generate_role_includes.py

.PHONY: build install test

build:
	@echo "🔧 Generating applications defaults → $(APPLICATIONS_OUT) from roles in $(ROLES_DIR)…"
	@mkdir -p $(dir $(APPLICATIONS_OUT))
	python3 $(APPLICATIONS_SCRIPT) --roles-dir $(ROLES_DIR) --output-file $(APPLICATIONS_OUT)
	@echo "✅ Applications defaults written to $(APPLICATIONS_OUT)\n"
	@echo "🔧 Generating Docker role includes → $(INCLUDES_OUT)…"
	@mkdir -p $(dir $(INCLUDES_OUT))
	python3 $(INCLUDES_SCRIPT) $(ROLES_DIR) -o $(INCLUDES_OUT) -p docker-
	@echo "✅ Docker role includes written to $(INCLUDES_OUT)"

install: build
	@echo "⚙️  Install complete."

test:
	@echo "\n🧪 Running Unit Tests..."
	python -m unittest discover -s tests/unit
	@echo "\n🔬 Running Integration Tests..."
	python -m unittest discover -s tests/integration