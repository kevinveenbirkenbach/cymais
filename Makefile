ROLES_DIR           := ./roles
APPLICATIONS_OUT    := ./group_vars/all/04_applications.yml
APPLICATIONS_SCRIPT := ./cli/build/defaults/applications.py
USERS_OUT           := ./group_vars/all/03_users.yml
USERS_SCRIPT        := ./cli/build/defaults/users.py
INCLUDES_SCRIPT     := ./cli/build/role_include.py

INCLUDE_GROUPS := $(shell python3 main.py meta invokable_paths -s "-" --no-signal | tr '\n' ' ')

# Directory where these include-files will be written
INCLUDES_OUT_DIR    := ./tasks/groups

# Compute extra users as before
EXTRA_USERS := $(shell \
  find $(ROLES_DIR) -maxdepth 1 -type d -printf '%f\n' \
    | sed -E 's/.*-//' \
    | grep -E -x '[a-z0-9]+' \
    | sort -u \
    | paste -sd, - \
)

.PHONY: build install test

clean:
	@echo "Removing not tracked git files"
	git clean -fdx

tree:
	@echo Generating Tree
	python3 main.py build tree -D 2 --no-signal

build:
	@echo "🔧 Generating users defaults → $(USERS_OUT)…"
	python3 $(USERS_SCRIPT) \
	  --roles-dir $(ROLES_DIR) \
	  --output $(USERS_OUT) \
	  --extra-users "$(EXTRA_USERS)"
	@echo "✅ Users defaults written to $(USERS_OUT)\n"

	@echo "🔧 Generating applications defaults → $(APPLICATIONS_OUT)…"
	python3 $(APPLICATIONS_SCRIPT) \
	  --roles-dir $(ROLES_DIR) \
	  --output-file $(APPLICATIONS_OUT)
	@echo "✅ Applications defaults written to $(APPLICATIONS_OUT)\n"

	@echo "🔧 Generating role-include files for each group…"
	@mkdir -p $(INCLUDES_OUT_DIR)
	@$(foreach grp,$(INCLUDE_GROUPS), \
	  out=$(INCLUDES_OUT_DIR)/$(grp)roles.yml; \
	  echo "→ Building $$out (pattern: '$(grp)')…"; \
	  python3 $(INCLUDES_SCRIPT) $(ROLES_DIR) \
	    -p $(grp) -o $$out; \
	  echo "  ✅ $$out"; \
	)

install: build
	@echo "⚙️  Install complete."

test:
	@echo "🧪 Running Python tests…"
	python -m unittest discover -s tests
	@echo "📑 Checking Ansible syntax…"
	ansible-playbook playbook.yml --syntax-check
