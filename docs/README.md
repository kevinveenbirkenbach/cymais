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

This command performs the following steps:
- **Copy Images:** Before building, it copies the necessary image assets from `../assets/img/` to `./assets/img/` using the `copy-images` target.
- **Generate API Documentation:** It executes `sphinx-apidoc` (via the `apidoc` target) to automatically generate reStructuredText files for all Python modules. These files are stored under a designated directory (e.g., `modules`), ensuring that every Python file is included in the documentation.
- **Build HTML Documentation:** Finally, it builds the HTML documentation using `sphinx-build` (triggered by the `html` target).

Once complete, you can view the documentation at the output location (e.g., [templates/html/index.html](templates/html/index.html)) 👀💻.

#### On Server

The same commands can be used on the server to ensure that documentation is always up to date. Make sure the server environment is properly configured with the necessary Python packages and assets.

### Additional Commands

- **`make copy-images`:**  
  Copies image files from the assets directory into the local documentation directory. This ensures that all required images are available for the generated documentation.

- **`make apidoc`:**  
  Runs `sphinx-apidoc` to scan all Python files in the source directory and generate corresponding reStructuredText files. This automates the inclusion of all Python modules into the Sphinx documentation.

- **`make html`:**  
  This target depends on the `apidoc` target. It first generates the API documentation and then builds the HTML documentation using `sphinx-build`. This is the standard target to produce the final, viewable documentation.

- **`make refresh`:**  
  A custom target (typically defined as a combination of cleaning the previous build and then running `make html`) that ensures the documentation is regenerated from scratch with the latest changes.

### Debug

To debug and produce a log file, execute:

```bash
pkgmgr shell cymais -c "make refresh SPHINXOPTS='-v -c .' 2>&1 | tee debug.log"
```

This command increases the verbosity of the Sphinx build process and redirects all output to `debug.log`, which is useful for troubleshooting any issues during the documentation build.

```