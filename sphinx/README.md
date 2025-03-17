# Documentation

CyMaIS uses [Sphinx](https://www.sphinx-doc.org/) to automatically generate its documentation and leverages the [Awesome Sphinx Theme](https://sphinxawesome.xyz/) for a sleek and responsive design. Enjoy a seamless, visually engaging experience 🚀✨.

## For Users

You can access the documentation [here](https://docs.cymais.cloud/) 🔗. Browse the latest updates and guides to get started.

## For Administrators

### Setup

#### On Localhost

To generate the documentation locally, run the following command:

```bash
pkgmgr shell cymais -c "make refresh"
```

This command cleans the previous build and generates the updated documentation. Once complete, you can view it at the output location (e.g., [templates/html/index.html](templates/html/index.html)) 👀💻.

#### On Server

In your inventory file, enable the **Sphinx** role. When activated, the documentation will be automatically generated and deployed under the **docs** subdomain of your CyMaIS instance. This ensures your documentation is always current and easily accessible 🔄🌐.