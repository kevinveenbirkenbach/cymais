# nginx-redirect-www

## 📌 Overview
The `nginx-redirect-www` role is designed to automate the process of setting up redirects from `www.domain.tld` to `domain.tld` for all domains and subdomains configured within the `{{nginx.directories.http.servers}}` directory. This role dynamically identifies configuration files following the pattern `*domain.tld.conf` and creates corresponding redirection rules.

## Role Description
This role performs several key tasks:
1. **Find Configuration Files**: Locates all `.conf` files in the `{{nginx.directories.http.servers}}` directory that match the `*.*.conf` pattern, ensuring that only domain and subdomain configurations are selected.
   
2. **Filter Domain Names**: Processes each configuration file, extracting the domain names and removing both the `.conf` extension and the `{{nginx.directories.http.servers}}` path.

3. **Prepare Redirect Domain Mappings**: Transforms the filtered domain names into a source-target mapping format, where `source` is `www.domain.tld` and `target` is `domain.tld`.

4. **Include nginx-redirect-domain Role**: Applies the redirection configuration using the `nginx-redirect-domain` role with the dynamically generated domain mappings.

## Notes
- This role is designed to work in environments where domain and subdomain configurations follow the naming pattern `*domain.tld.conf`.
- It automatically excludes any configurations that begin with `www.`, preventing duplicate redirects.

---

This `nginx-redirect-www` role was crafted by [Kevin Veen-Birkenbach](https://www.veen.world) with insights and guidance provided by ChatGPT, an advanced AI language model from OpenAI. The development process, including the discussions with ChatGPT that shaped this role, can be [here](https://chat.openai.com/share/a68e3574-f543-467d-aea7-0895f0e00bbb) explored in detail.