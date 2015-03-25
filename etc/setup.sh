#!/bin/bash
pip3 install -r ../zipline/etc/requirements.txt
pip3 install -r ../zipline/etc/requirements_dev.txt
python3 ../zipline/setup.py install