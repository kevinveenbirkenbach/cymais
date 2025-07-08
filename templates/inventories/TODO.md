# Todo 
Implement 

# Inventories Directory

## Purpose

The `inventories/` directory defines environment-specific inventory data for Ansible.

Each subdirectory within `inventories/` represents a dedicated persona or environment (e.g., `enterprise`, `developer`, `gamer`) and contains the necessary templates and variables to generate the final Ansible inventory and variable files.

This structure allows fully automated and reproducible inventory generation using a Python tool.

---

## Directory Structure

```
inventories/
├── <persona-name>/
│   ├── README.md               # Description of the persona or environment
│   ├── inventory.yml.j2        # Jinja2 template for the dynamic inventory file
│   ├── vars.yml.j2             # Jinja2 template for generating group_vars / host_vars
│   └── config.yml              # Metadata and settings for this persona (optional)
```

---

## Purpose of Each File

| File | Purpose |
|------|---------|
| `README.md` | Documentation of the persona/environment, included roles, and intended use case. |
| `inventory.yml.j2` | Jinja2 template that generates the inventory structure (hosts, groups, variables). |
| `vars.yml.j2` | Jinja2 template generating environment-specific variables (used in group_vars or host_vars). |
| `config.yml` | Optional metadata file containing settings like acquired personas, feature flags, default variables. |

---

## Recommended Workflow with Python Tool

1. The Python tool scans `inventories/<persona>` directories.
2. For each persona:
    - Load `config.yml` (optional).
    - Render `vars.yml.j2` → Output: `group_vars/all.yml`
    - Render `inventory.yml.j2` → Output: `inventory.yml`
    - Recursively acquire and merge dependent personas (defined in `config.yml`):
  
```yaml
# Example: inventories/enterprise/config.yml
acquire_personas:
  - corporate
  - administrator
  - developer
```

3. Combine all output into a deployable inventory directory:
```
output/
├── enterprise/
│   ├── inventory.yml
│   └── group_vars/
│       └── all.yml
```

4. The generated inventory is ready for use:
```bash
ansible-playbook -i output/enterprise/inventory.yml site.yml
```

---

## Benefits of This Approach

- Personas remain fully modular and reusable.
- No duplication of host/group data.
- Centralized variable generation per persona.
- Automated and consistent inventory generation.
- Easy documentation per persona via `README.md`.
- Optional Feature Flags or Role Toggles in `config.yml`.
- Scalable for multi-environment setups.

---

## Example Python Features

| Feature | Description |
|---------|-------------|
| Auto Inventory Generation | Render `inventory.yml` and `vars.yml` from Jinja2 templates. |
| Recursive Persona Acquisition | Load dependent personas automatically. |
| Feature Flags | Enable/disable features via `config.yml`. |
| Variable Merging | Combine variables from all acquired personas. |
| Output Directory | Place final inventories in `output/<persona>` directory. |

---

## Example Command

```bash
python generate_inventory.py --persona enterprise --output output/
```

This will render the `enterprise` persona, recursively acquire all dependent personas, and generate a fully deployable inventory with variables.

```