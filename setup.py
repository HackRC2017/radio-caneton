from setuptools import setup

setup(
    name='radio-caneton',
    version='0.1.0',
    packages=['radio_caneton'],
    install_requires=[
        'apscheduler==3.3.1',
        'pymongo==3.4.0',
        'requests==2.13.0',
    ],
)
