import os
from setuptools import setup


def read(*rnames):
  return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


setup(
  name = 'graphene-federation',
  packages = ['graphene_federation'],
  version = '0.0.2',
  license='MIT',
  description = 'Federation implementation for graphene',
  long_description=(read('README.md')),
  long_description_content_type='text/markdown',
  author = 'Igor Kasianov',
  author_email = 'super.hang.glider@gmail.com',
  url = 'https://github.com/erebus1/graphene-federation',
  download_url = 'https://github.com/erebus1/graphene-federation/archive/0.0.2.tar.gz',
  keywords = ['graphene', 'gql', 'federation'],
  install_requires=[
          "graphene>=2.1.0,<3"
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    "Intended Audience :: Developers",
    "Topic :: Software Development :: Libraries",
    "Programming Language :: Python :: 3.6",
  ],
)