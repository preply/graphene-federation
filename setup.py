import os
from setuptools import setup


def read(*rnames):
  return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '0.1.0'

setup(
  name = 'graphene-federation',
  packages = ['graphene_federation'],
  version = version,
  license='MIT',
  description = 'Federation implementation for graphene',
  long_description=(read('README.md')),
  long_description_content_type='text/markdown',
  author = 'Igor Kasianov',
  author_email = 'super.hang.glider@gmail.com',
  url = 'https://github.com/preply/graphene-federation',
  download_url = f'https://github.com/preply/graphene-federation/archive/{version}.tar.gz',
  keywords = ['graphene', 'gql', 'federation'],
  install_requires=[
          "graphene>=2.1.0"
      ],
  classifiers=[
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "Topic :: Software Development :: Libraries",
    "Programming Language :: Python :: 3.6",
  ],
)
