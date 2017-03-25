FROM python:3.6.0

WORKDIR /usr/src/app/

ADD setup.py /usr/src/app/
ADD radio_caneton /usr/src/app/radio_caneton/

RUN pip3 install -e .

CMD python3 -m radio_caneton
