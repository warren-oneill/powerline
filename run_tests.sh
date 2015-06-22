#!/bin/bash
nosetests --with-coverage --cover-package=gg.powerline &> tests/report.txt
flake8 tests gg

