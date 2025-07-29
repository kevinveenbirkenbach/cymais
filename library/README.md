# Custom Modules (`library/`) for Infinito.Nexus

This directory contains **custom Ansible modules** developed specifically for the Infinito.Nexus project.

## When to Use the `library/` Directory

- **Place custom Ansible modules here:**  
  Use this directory for any Python modules you have written yourself that are not part of the official Ansible distribution.
- **Extend automation capabilities:**  
  Custom modules allow you to implement logic, workflows, or integrations that are not available through built-in Ansible modules or existing community collections.
- **Project-specific functionality:**  
  Use for project- or infrastructure-specific tasks, such as managing custom APIs, provisioning special infrastructure resources, or integrating with internal systems.

### Examples

- Managing a special internal API for your company.
- Automating a resource that has no official Ansible module.
- Creating a highly customized deployment step for your environment.

## Usage Example

In your playbook, call your custom module as you would any other Ansible module:
```yaml
- name: Use custom Infinito.Nexus module
  infinito_my_custom_module:
    option1: value1
    option2: value2
````

Ansible automatically looks in the `library/` directory for custom modules during execution.

## When *not* to Use the `library/` Directory

* Do **not** place shared utility code here—put that in `module_utils/` for use across multiple modules or plugins.
* Do **not** put filter or lookup plugins here—those belong in `filter_plugins/` or `lookup_plugins/` respectively.

## Further Reading

* [Developing Ansible Modules](https://docs.ansible.com/ansible/latest/dev_guide/developing_modules.html)
* [Best Practices: Organizing Custom Modules](https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_documenting.html)