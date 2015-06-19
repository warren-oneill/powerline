#!/bin/bash
nosetests --with-coverage --cover-package=gg.powerline
flake8 tests gg examples

