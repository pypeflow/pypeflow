# coding: utf-8
from setuptools import setup
from pypeflow import get_version
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
version = get_version()

with open(os.path.join(BASE_DIR, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pypeflow',
    url='https://github.com/pypeflow/pypeflow/',
    download_url='https://github.com/pypeflow/pypeflow/tarball/{}'.format(version),
    version=version,
    author='Gleber Diniz',
    author_email='pypeflowproject@gmail.com',
    description='A static site generator for python developers',
    long_description=long_description,
    packages=['pypeflow'],
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='static site generator'
)
