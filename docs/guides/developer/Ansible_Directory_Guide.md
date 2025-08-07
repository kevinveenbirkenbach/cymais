## 📖 Infinito.Nexus Ansible & Python Directory Guide

This document provides a **decision matrix** for when to use each default Ansible plugin and module directory in the context of **Infinito.Nexus development** with Ansible and Python. It links to official docs, explains use-cases, and points back to our conversation.

---

### 🔗 Links & References

* Official Ansible Plugin Guide: [https://docs.ansible.com/ansible/latest/dev\_guide/developing\_plugins.html](https://docs.ansible.com/ansible/latest/dev_guide/developing_plugins.html)
* Official Ansible Module Guide: [https://docs.ansible.com/ansible/latest/dev\_guide/developing\_modules.html](https://docs.ansible.com/ansible/latest/dev_guide/developing_modules.html)
* This conversation: [Link to this conversation](https://chat.openai.com/)

---

### 🛠️ Repo Layout & Default Directories

```plaintext
ansible-repo/
├── library/                # 📦 Custom Ansible modules
├── filter_plugins/         # 🔍 Custom Jinja2 filters
├── lookup_plugins/         # 👉 Custom lookup plugins
├── module_utils/           # 🛠️ Shared Python helpers for modules
├── action_plugins/         # ⚙️ Task-level orchestration logic
├── callback_plugins/       # 📣 Event callbacks (logging, notifications)
├── inventory_plugins/      # 🌐 Dynamic inventory sources
├── strategy_plugins/       # 🧠 Task execution strategies
└── ...                     # Other plugin dirs (connection, cache, etc.)
```

---

### 🎯 Decision Matrix: Which Folder for What?

| Folder               | Type                 | Use-Case                                 | Example (Infinito.Nexus)                                | Emoji |
| -------------------- | -------------------- | ---------------------------------------- | ----------------------------------------------------- | ----- |
| `library/`           | **Module**           | Write idempotent actions                 | `cloud_network.py`: manage VPCs, subnets              | 📦    |
| `filter_plugins/`    | **Filter plugin**    | Jinja2 data transforms in templates/vars | `to_camel_case.py`: convert keys for API calls        | 🔍    |
| `lookup_plugins/`    | **Lookup plugin**    | Fetch external/secure data at runtime    | `vault_lookup.py`: pull secrets from Infinito.Nexus Vault     | 👉    |
| `module_utils/`      | **Utility library**  | Shared Python code for modules           | `infinito_client.py`: common API client base class      | 🛠️   |
| `action_plugins/`    | **Action plugin**    | Complex task orchestration wrappers      | `deploy_stack.py`: sequence Terraform + Ansible steps | ⚙️    |
| `callback_plugins/`  | **Callback plugin**  | Customize log/report behavior            | `notify_slack.py`: send playbook status to Slack      | 📣    |
| `inventory_plugins/` | **Inventory plugin** | Dynamic host/group sources               | `azure_inventory.py`: list hosts from Azure tags      | 🌐    |
| `strategy_plugins/`  | **Strategy plugin**  | Control task execution order/parallelism | `rolling_batch.py`: phased rollout of VMs             | 🧠    |

---

### 📝 Detailed Guidance

1. **library/** 📦

   * **When?** Implement **one-off, idempotent actions** (create/delete cloud resources).
   * **Why?** Modules under `library/` are first in search path for `ansible` modules.
   * **Docs:** [https://docs.ansible.com/ansible/latest/dev\_guide/developing\_modules.html](https://docs.ansible.com/ansible/latest/dev_guide/developing_modules.html)

2. **filter\_plugins/** 🔍

   * **When?** You need **data manipulation** (lists, strings, dicts) inside Jinja2.
   * **Why?** Extends `|` filters in templates and variable declarations.
   * **Docs:** [https://docs.ansible.com/ansible/latest/dev\_guide/developing\_plugins.html#filter-plugins](https://docs.ansible.com/ansible/latest/dev_guide/developing_plugins.html#filter-plugins)

3. **lookup\_plugins/** 👉

   * **When?** You must **retrieve secret/external data** during playbook compile/runtime.
   * **Why?** Lookup plugins run before tasks, enabling dynamic variable resolution.
   * **Docs:** [https://docs.ansible.com/ansible/latest/dev\_guide/developing\_plugins.html#lookup-plugins](https://docs.ansible.com/ansible/latest/dev_guide/developing_plugins.html#lookup-plugins)

4. **module\_utils/** 🛠️

   * **When?** Multiple modules share **common Python code** (HTTP clients, validation).
   * **Why?** Avoid code duplication; modules import these utilities.
   * **Docs:** [https://docs.ansible.com/ansible/latest/dev\_guide/developing\_modules.html#module-utils](https://docs.ansible.com/ansible/latest/dev_guide/developing_modules.html#module-utils)

5. **action\_plugins/** ⚙️

   * **When?** You need to **wrap or extend** module behavior at task invocation time.
   * **Why?** Provides hooks before/after module execution.
   * **Docs:** [https://docs.ansible.com/ansible/latest/dev\_guide/developing\_plugins.html#action-plugins](https://docs.ansible.com/ansible/latest/dev_guide/developing_plugins.html#action-plugins)

6. **callback\_plugins/** 📣

   * **When?** You want **custom event handlers** (logging, progress, notifications).
   * **Why?** Receive play/task events for custom output.
   * **Docs:** [https://docs.ansible.com/ansible/latest/dev\_guide/developing\_plugins.html#callback-plugins](https://docs.ansible.com/ansible/latest/dev_guide/developing_plugins.html#callback-plugins)

7. **inventory\_plugins/** 🌐

   * **When?** Hosts/groups come from **dynamic sources** (cloud APIs, databases).
   * **Why?** Replace static `inventory.ini` with code-driven inventories.
   * **Docs:** [https://docs.ansible.com/ansible/latest/dev\_guide/developing\_plugins.html#inventory-plugins](https://docs.ansible.com/ansible/latest/dev_guide/developing_plugins.html#inventory-plugins)

8. **strategy\_plugins/** 🧠

   * **When?** You need to **customize execution strategy** (parallelism, ordering).
   * **Why?** Override default `linear` strategy (e.g., `free`, custom batches).
   * **Docs:** [https://docs.ansible.com/ansible/latest/dev\_guide/developing\_plugins.html#strategy-plugins](https://docs.ansible.com/ansible/latest/dev_guide/developing_plugins.html#strategy-plugins)

---

### 🚀 Infinito.Nexus Best Practices

* **Organize modules** by service under `library/cloud/` (e.g., `vm`, `network`, `storage`).
* **Shared client code** in `module_utils/infinito/` for authentication, request handling.
* **Secrets lookup** via `lookup_plugins/vault_lookup.py` pointing to Infinito.Nexus Vault.
* **Filters** to normalize data formats from cloud APIs (e.g., `snake_to_camel`).
* **Callbacks** to stream playbook results into Infinito.Nexus Monitoring.

Use this matrix as your **single source of truth** when extending Ansible for Infinito.Nexus! 👍 

---

This matrix was created with the help of ChatGPT 🤖—see our conversation [here](https://chatgpt.com/canvas/shared/682b1a62d6dc819184ecdc696c51290a).
