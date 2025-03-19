# Configuration Options 📋

## One Wildcard Certificate for All Subdomains

By default, each subdomain gets its own certificate. You can **enable a wildcard certificate** by setting:

```yaml
enable_wildcard_certificate: true
```

## Pros & Cons of a Wildcard Certificate
### Pros
- ✅ **Improves performance** by reducing TLS handshakes.  
- ✅ **Simplifies certificate management** (one cert for all subdomains).  
### Cons
- ⚠ **Requires manual DNS challenge setup** for Let's Encrypt.  
- ⚠ **Needs additional configuration for automation** (see below).  

If enabled, update your inventory file and follow the **[manual wildcard certificate setup](SETUP.md)**.
