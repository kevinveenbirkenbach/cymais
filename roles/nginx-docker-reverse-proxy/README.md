# role nginx-docker-reverse-proxy

Uses nginx as an [reverse proxy](https://en.wikipedia.org/wiki/Reverse_proxy) for local docker applications.

## debug
```bash
curl -I {{address}}
```
- https://serverfault.com/questions/434915/nginx-proxy-caching-how-to-check-if-it-is-working

## performance
- https://stackoverflow.com/questions/33703230/caching-images-on-all-folder-levels-of-nginx-reverse-proxy
- https://www.tweaked.io/guide/nginx-proxying/
- https://serverfault.com/questions/796735/nginx-reverse-proxy-is-slow/796740
- https://serverfault.com/questions/741610/what-is-the-difference-between-proxy-request-buffering-and-proxy-buffering-on-ng
- https://askubuntu.com/questions/1103626/should-i-enable-client-max-body-size-proxy-request-buffering-and-proxy-bufferin
- https://serverfault.com/questions/692577/whats-the-difference-between-proxy-buffer-and-proxy-cache-module-in-nginx-confi
- https://github.com/sissbruecker/linkding/issues/88
- https://www.bogotobogo.com/DevOps/Docker/docker-compose-Nginx-Reverse-Proxy-Multiple-Containers.php
