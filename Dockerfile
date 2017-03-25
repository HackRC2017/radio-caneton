FROM python:3.6.0

WORKDIR /usr/src/app/

ADD setup.py /usr/src/app/
ADD rad_caneton /usr/src/app/rad_caneton/

RUN pip3 install -e .

CMD python3 -m rad_caneton
