# :duck: radio-caneton

## development

```shell
python3 -m venv .env && source .env/bin/activate
pip3 install -e .
python3 -m radio_caneton
```

## docker

```shell
docker build -t radio_caneton .

docker run --name tempo-mongo -d mongo

docker run -d \
    --name radio-caneton \
    --link tempo-mongo:mongo \
    -e 'MONGODB_HOST=mongo' \
    -e 'OBAMO_HOST=<OBAMO_HOST>' \
    radio-caneton
```
