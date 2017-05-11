# classroom_service

## Deploy

1. Configure Environment file

**Deploy Environment FILE (container.env)**

```
REST_MONGO_HOST=<Book Attention MongoDB host>
REST_MONGO_PORT=<MongoDB port>
BROKER_HOST=<Docker Engine host machine ip>
C_FORCE_ROOT=true
CELERY_ACCEPT_CONTENT=json
```

2. Run

```
docker-compose stop && docker-compose build && dockder-compose up -d && docker-compose ps
```

## Test

1. Configure Environment file

**Test Environment FILE (container.test.env)**

```
REST_MONGO_HOST=<Book Attention MongoDB host>
REST_MONGO_PORT=<MongoDB port>
BROKER_HOST=<Docker Engine host machine ip>
C_FORCE_ROOT=true
CELERY_ACCEPT_CONTENT=json
```

2. Run

```
./start_test.sh && docker-compose -f docker-compose.test.yml logs --tail="100" classroom_api_test
```
