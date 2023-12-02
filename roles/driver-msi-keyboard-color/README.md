# Ansible Role: driver-msi-keyboard-color

Ansible role to set up dynamic keyboard color change on MSI laptops.

## Requirements

- An MSI laptop
- The `msi-perkeyrgb` tool installed on the system
- Ansible 2.9 or later

## Role Variables

Available variables are listed below, along with their default values:

```yaml
vendor_and_product_id: ""
```

The `vendor_and_product_id` variable is required and should be set to the vendor and product ID of the MSI laptop.

## Dependencies

- `system-aur-helper`

## Example Playbook

```yaml
- hosts: all
  roles:
    - keyboard-color
  vars:
    vendor_and_product_id: "your_vendor_and_product_id"
```

## Author

This role was created by [Kevin Veen-Birkenbach](https://github.com/kevinveenbirkenbach).

## Chat Conversation

To see how this role was developed, you can refer to the [Chat Conversation](https://chat.openai.com/share/41c47fdb-a92d-466d-9e92-5a894fe6bec3) that produced this software.

