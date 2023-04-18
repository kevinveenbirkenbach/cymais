# role server_docker-elk

I decided against using this role for security reasons. I recommend to use another tool if you don't want to pay for keeping your logs save and if you don't want to depend on external servers. 

## restart all services
```bash
docker restart elk_logstash_1 && docker restart elk_elasticsearch_1 && docker restart elk_kibana_1
```

## see
- https://logz.io/blog/elk-stack-on-docker/
- https://github.com/kevinveenbirkenbach/server_docker-elk
- https://logz.io/blog/server_docker-logging/
