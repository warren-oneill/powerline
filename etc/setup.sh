#!/bin/bash
pip3 install --allow-all-external -r etc/requirements.txt
pip3 install -e git://github.com/quantopian/zipline.git@futures-trading#egg=futures-trading
