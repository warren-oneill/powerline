#!/bin/bash
pip3 install --allow-all-external -r etc/requirements.txt
pip3 install -e git://github.com/grundgruen/zipline.git@gg-futures#egg=zipline-futures