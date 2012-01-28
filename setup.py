from setuptools import setup, find_packages

version = __import__('torretta').__version__

setup(
    name = 'torretta',
    version = version,
    description = 'Torrent crawler and downloader',
    author = 'FlaPer87',
    author_email = 'flaper87@flaper87.org',
    url = 'http://github.com/FlaPer87/torretta',
    packages = find_packages(),
    zip_safe=False,
    install_requires=[
    ],
    test_suite='torretta.tests',
)
