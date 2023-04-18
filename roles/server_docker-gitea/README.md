# role server_docker-gitea

## update
```bash 
cd /home/administrator/docker-compose/gitea/
docker-compose down
docker-compose pull
docker-compose up -d
```
Keep in mind to track and to don't interrupt the update process until the migration is done. 

## set variables
```bash
  COMPOSE_HTTP_TIMEOUT=600
  DOCKER_CLIENT_TIMEOUT=600
  GITEA_APPLICATION_DOCKER_CONTAINER=gitea_application_1
  GITEA_DATABASE_DOCKER_CONTAINER=gitea_database_1
```

## recreate
```bash
cd /home/administrator/docker-compose/gitea/ && docker-compose -p gitea up -d --force-recreate
```

## database access
To access the database execute
```bash
  docker exec -it $GITEA_DATABASE_DOCKER_CONTAINER /bin/mysql -u gitea -p
```
## bash in application
docker exec -it $GITEA_APPLICATION_DOCKER_CONTAINER /bin/sh

## update app.ini
```bash
cat > app.ini << EOF
APP_NAME = test @test
RUN_MODE = prod
RUN_USER = git

[repository]
ROOT = /data/git/repositories

[repository.local]
LOCAL_COPY_PATH = /data/gitea/tmp/local-repo

[repository.upload]
TEMP_PATH = /data/gitea/uploads

[server]
APP_DATA_PATH    = /data/gitea
DOMAIN           = test.test
SSH_DOMAIN       = test.test
HTTP_PORT        = 3000
ROOT_URL         = https://test.test/
DISABLE_SSH      = false
SSH_PORT         = 2201
SSH_LISTEN_PORT  = 22
LFS_START_SERVER = true
LFS_CONTENT_PATH = /data/git/lfs
LFS_JWT_SECRET   = testsecret
OFFLINE_MODE     = false

[database]
PATH     = /data/gitea/gitea.db
DB_TYPE  = mysql
HOST     = database:3306
NAME     = gitea
USER     = gitea
PASSWD   = testpasswort
LOG_SQL  = false
SCHEMA   =
SSL_MODE = disable
CHARSET  = utf8mb4

[indexer]
ISSUE_INDEXER_PATH = /data/gitea/indexers/issues.bleve

[session]
PROVIDER_CONFIG = /data/gitea/sessions
PROVIDER        = file

[picture]
AVATAR_UPLOAD_PATH            = /data/gitea/avatars
REPOSITORY_AVATAR_UPLOAD_PATH = /data/gitea/repo-avatars
DISABLE_GRAVATAR              = false
ENABLE_FEDERATED_AVATAR       = true

[attachment]
PATH = /data/gitea/attachments

[log]
MODE                 = console
LEVEL                = info
REDIRECT_MACARON_LOG = true
MACARON              = console
ROUTER               = console
ROOT_PATH            = /data/gitea/log

[security]
INSTALL_LOCK   = true
SECRET_KEY     = test_secret_key
INTERNAL_TOKEN = test_secret_internal_token

[service]
DISABLE_REGISTRATION              = true
REQUIRE_SIGNIN_VIEW               = false
REGISTER_EMAIL_CONFIRM            = false
ENABLE_NOTIFY_MAIL                = false
ALLOW_ONLY_EXTERNAL_REGISTRATION  = false
ENABLE_CAPTCHA                    = false
DEFAULT_KEEP_EMAIL_PRIVATE        = false
DEFAULT_ALLOW_CREATE_ORGANIZATION = true
DEFAULT_ENABLE_TIMETRACKING       = true
NO_REPLY_ADDRESS                  = noreply.test.test

[oauth2]
JWT_SECRET = test_secret

[mailer]
ENABLED = false

[openid]
ENABLE_OPENID_SIGNIN = true
ENABLE_OPENID_SIGNUP = true
EOF
```
