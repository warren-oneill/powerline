#!/bin/bash

nosetests --with-coverage --with-timer --cover-package=gg.powerline &> tests/report.txt
flake8 tests gg
