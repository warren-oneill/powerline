try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
    
setup(
    description='Powerline extension to Zipline',
    author='Grundgruen',
    version='0.1',
    install_requires=['nose'],
    packages=['powerline'],
    name='powerline'
)