#!/bin/bash
pip3 install --allow-all-external -r etc/requirements.txt
pip3 install -e git://github.com/warren-oneill/zipline.git@cal-clean#egg=zipline-futures