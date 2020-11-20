import os
from setuptools import find_packages, setup


def read(*rnames):
  return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '0.1.0'

tests_require = [
    "pytest==6.1.1",
    "pytest-cov",
]

dev_require = [
    "black==20.8b1",
    "flake8==3.8.4",
] + tests_require

setup(
  name='graphene-federation',
  packages=find_packages(exclude=["tests"]),
  version=version,
  license='MIT',
  description = 'Federation implementation for graphene',
  long_description=(read('README.md')),
  long_description_content_type='text/markdown',
  author='Igor Kasianov',
  author_email='super.hang.glider@gmail.com',
  url='https://github.com/preply/graphene-federation',
  download_url=f'https://github.com/preply/graphene-federation/archive/{version}.tar.gz',
  keywords=["graphene", "graphql", "gql", "federation"],
  install_requires=[
    "graphene>=2.1.0,<3"
  ],
  classifiers=[
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "Topic :: Software Development :: Libraries",
    "Programming Language :: Python :: 3.6",
  ],
  extras_require={
    "test": tests_require,
    "dev": dev_require,
  },
)
