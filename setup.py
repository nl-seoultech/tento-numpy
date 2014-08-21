#! -*- coding: utf-8 -*-
from setuptools import setup, find_packages

dep_links = [
    # soundfile>=0.0.1
    'https://github.com/admire93/soundfile/tarball/master#egg=soundfile-0.0.1'
]

setup(name='tento_num',
      version='0.0.1',
      author='khj',
      author_email='admire9@gmail.com',
      packages=find_packages(),
      dependency_links=dep_links,
      install_requires=[
          'pytest==2.6.0', 'numpy', 'matplotlib', 'soundfile>=0.0.1'
      ])
