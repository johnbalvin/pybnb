from setuptools import setup

VERSION = '0.0.5'
DESCRIPTION = 'Airbnb scraper in Python'

setup(
    name="gobnb",
    version=VERSION,
    author="John (John Balvin)",
    author_email="<johnchristian@hotmail.es>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    url='https://github.com/johnbalvin/pybnb',
    long_description=open('README.md').read(),
    keywords=['airbnb', 'scraper', 'crawler'],
    install_requires=['curl_cffi','bs4'],
)