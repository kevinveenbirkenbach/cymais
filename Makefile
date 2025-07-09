ROLES_DIR         	:= ./roles
APPLICATIONS_OUT  	:= ./group_vars/all/04_applications.yml
APPLICATIONS_SCRIPT := ./cli/generate_applications.py
USERS_OUT  			:= ./group_vars/all/03_users.yml
USERS_SCRIPT		:= ./cli/generate_users.py
INCLUDES_OUT      	:= ./tasks/utils/server-roles.yml
INCLUDES_SCRIPT   	:= ./cli/generate_playbook.py

EXTRA_USERS := $(shell \
	find $(ROLES_DIR) -maxdepth 1 -type d -name 'web-app*' -printf '%f\n' \
	| sed -E 's/^web-app[_-]?//' \
	| grep -E -x '[a-z0-9]+' \
	| paste -sd, - \
)

.PHONY: build install test

build:
	@echo "🔧 Generating applications defaults → $(APPLICATIONS_OUT) from roles in $(ROLES_DIR)…"
	python3 $(USERS_SCRIPT) --roles-dir $(ROLES_DIR) --output $(USERS_OUT) --extra-users "$(EXTRA_USERS)"
	@echo "✅ Users defaults written to $(USERS_OUT)\n"
	python3 $(APPLICATIONS_SCRIPT) --roles-dir $(ROLES_DIR) --output-file $(APPLICATIONS_OUT)
	@echo "✅ Applications defaults written to $(APPLICATIONS_OUT)\n"
	@echo "🔧 Generating users defaults → $(USERS_OUT) from roles in $(ROLES_DIR)…"
	@echo "🔧 Generating Docker role includes → $(INCLUDES_OUT)…"
	@mkdir -p $(dir $(INCLUDES_OUT))
	python3 $(INCLUDES_SCRIPT) $(ROLES_DIR) -o $(INCLUDES_OUT) \
		-p web-app \
		-p web-svc \
		-p svc-openldap \
		-p svc-rdbms-postgres \
		-p svc-rdbms-mariadb
	@echo "✅ Docker role includes written to $(INCLUDES_OUT)"

install: build
	@echo "⚙️  Install complete."

test:
	@echo "🧪 Running Python Tests..."
	python -m unittest discover -s tests
	@echo "📑 Syntax Checking Ansible Playbook..."
	ansible-playbook playbook.yml --syntax-check
