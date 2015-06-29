#!/bin/bash
pip3 install --allow-all-external -r etc/requirements.txt
pip3 install -e git://github.com/quantopian/zipline.git@cc77a523220c980f3c741b073a0f3eea5ca8db51#egg=zipline
