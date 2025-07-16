# IT-Infrastructure Automation Framework 🚀

**🔐 One login. ♾️ Infinite application** - ***🤖 Automate the Provisioning of All Your 🌐 Servers and 🖥️ Workstations with a Single Open‑Source Script!***

![CyMaIS Logo](assets/img/logo.png)
---

## What is CyMaIS? 📌

**CyMaIS** is an **automated, modular infrastructure framework** built on **Docker**, **Linux**, and **Ansible**, equally suited for cloud services, local server management, and desktop workstations. At its core lies a **web-based desktop with single sign-on**—backed by an **LDAP directory** and **OIDC**—granting **seamless access** to an almost limitless portfolio of self-hosted applications. It fully supports **ActivityPub applications** and is **Fediverse-compatible**, while integrated **monitoring**, **alerting**, **cleanup**, **self-healing**, **automated updates**, and **backup solutions** provide everything an organization needs to run at scale.

| 📚 | 🔗 |
|---|---|
| 🌐 Try It Live | [![CyMaIS.Cloud](https://img.shields.io/badge/CyMaIS-%2ECloud-000000?labelColor=004B8D&style=flat&borderRadius=8)](https://cymais.cloud) |
| 🔧 Request Your Setup       | [![CyberMaster.Space](https://img.shields.io/badge/CyberMaster-%2ESpace-000000?labelColor=004B8D&style=flat&borderRadius=8)](https://cybermaster.space) |
| 📖 About This Project  | [![GitHub Sponsors](https://img.shields.io/badge/Sponsor-GitHub%20Sponsors-blue?logo=github)](https://github.com/sponsors/kevinveenbirkenbach) [![Build Status](https://github.com/kevinveenbirkenbach/cymais/actions/workflows/test-container.yml/badge.svg?branch=master)](https://github.com/kevinveenbirkenbach/cymais/actions/workflows/test-container.yml?query=branch%3Amaster) [![View Source](https://img.shields.io/badge/View_Source-Repository-000000?logo=github&labelColor=004B8D&style=flat&borderRadius=8)](https://github.com/kevinveenbirkenbach/cymais) |
| ☕️ Support Us               |  [![Patreon](https://img.shields.io/badge/Support-Patreon-orange?logo=patreon)](https://www.patreon.com/c/kevinveenbirkenbach) [![Buy Me a Coffee](https://img.shields.io/badge/Buy%20me%20a%20Coffee-Funding-yellow?logo=buymeacoffee)](https://buymeacoffee.com/kevinveenbirkenbach) [![PayPal](https://img.shields.io/badge/Donate-PayPal-blue?logo=paypal)](https://s.veen.world/paypaldonate) [![Sponsor CyMaIS](https://img.shields.io/badge/Donate–CyMaIS-000000?style=flat&labelColor=004B8D&logo=github-sponsors&logoColor=white&borderRadius=8)](https://github.com/sponsors/kevinveenbirkenbach) |

---

## Key Features 🎯

* **Automated Deployment** 📦
  Turn up servers and workstations in minutes with ready-made Ansible roles.

* **Enterprise-Grade Security** 🔒
  Centralized user management via LDAP & OIDC (Keycloak), plus optional 2FA and encrypted storage.

* **Modular Scalability** 📈
  Grow from small teams to global enterprises by composing only the services you need.

* **Fediverse & ActivityPub Support** 🌐
  Seamlessly integrate Mastodon, Peertube, Matrix and other ActivityPub apps out of the box.

* **Self-Healing & Maintenance** ⚙️
  Automated cleanup, container healing, and auto-updates keep infrastructure healthy without human intervention.

* **Monitoring, Alerting & Analytics** 📊
  Built-in system, application, and security monitoring with multi-channel notifications.

* **Backup & Disaster Recovery** 💾
  Scheduled backups and scripted recovery processes to safeguard your data.

* **Continuous Updates** 🔄
  Automatic patching and version upgrades across the stack.

* **Application Ecosystem** 🚀
  A curated suite of self-hosted apps—from **project management**, **version control**, and **CI/CD** to **chat**, **video conferencing**, **CMS**, **e-learning**, **social networking**, and **e-commerce**—all seamlessly integrated.

More informations about the features you will find [here](docs/overview/Features.md).

---

## Get Started 🚀

### Use it online 🌐 

Give CyMaIS a spin at [CyMaIS.cloud](httpy://cymais.cloud) – sign up in seconds, click around, and see how easy infra magic can be! 🚀🔧✨

### Install locally 💻
1. **Install CyMaIS** via [Kevin's Package Manager](https://github.com/kevinveenbirkenbach/package-manager)
2. **Setup CyMaIS** using:
   ```sh
   pkgmgr install cymais
   ```
3. **Explore Commands** with:
   ```sh
   cymais --help
   ```
---

### Setup with Docker🚢

Get CyMaIS up and running inside Docker in just a few steps. For detailed build options and troubleshooting, see the [Docker Guide](docs/Docker.md).

```bash
# 1. Build the Docker image: the Docker image:
docker build -t cymais:latest .

# 2. Run the CLI interactively:
docker run --rm -it cymais:latest cymais --help
```

---

## License ⚖️

CyMaIS is distributed under the **CyMaIS NonCommercial License**. Please see [LICENSE.md](LICENSE.md) for full terms.

---

## Professional Setup & Support 💼

For expert installation and configuration visit [cybermaster.space](https://cybermaster.space/) or write to us at **[contact@cymais.cloud](mailto:contact@cymais.cloud)**.
