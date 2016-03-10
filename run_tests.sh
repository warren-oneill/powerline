#!/bin/bash

nosetests --with-coverage --with-timer --cover-package=powerline &> tests/report.txt
flake8 tests powerline
