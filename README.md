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

docker run --name mongo -d mongo

docker run --name radio_caneton -d \
    --link some-mongo:mongo \
    radio_caneton
```
