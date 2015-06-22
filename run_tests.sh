#!/bin/bash
nosetests --with-coverage --cover-package=gg.powerline &> tests/README.md
flake8 tests gg

