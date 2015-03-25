try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
    
config = {
    'description': 'Powerline extension to Zipline',
    'author': 'Grundgrün',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['powerline'],
    'scripts': [],
}

setup(**config)
