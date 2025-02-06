# role nginx
This role sets up an nginx server. It was developed by [Kevin Veen-Birkenbach](https://www.veen.world).
## Debug

### General Debugging
```bash 
journalctl -f -u nginx
```

### Detailled Debugging
Set ``enable_debugenable_debug: true``.
#### Follow logs of one host
```bash
journalctl -u nginx -f | grep "<<hostname>>"
```


### Activate detailled Debugging:

## performance
- https://www.monitis.com/blog/6-best-practices-for-optimizing-your-nginx-performance/
- https://www.nginx.com/blog/tuning-nginx/
- https://davidwalsh.name/enable-gzip
- https://www.nginx.com/blog/performance-tuning-tips-tricks/
- https://medium.com/pixelpoint/best-practices-for-cache-control-settings-for-your-website-ff262b38c5a2
- https://www.nginx.com/blog/nginx-caching-guide/
- https://meta.discourse.org/t/using-nginx-as-proxy-server-is-very-slow-but-it-is-very-fast-if-using-nginx-in-docker-why/168972
