from distutils.core import setup

with open("README.md", "r") as fh:
  long_description = fh.read()

setup(
  name = 'graphene-federation',
  packages = ['graphene_federation'],
  version = '0.0.1',
  license='MIT',
  description = 'Federation implementation for graphene',
  long_description=long_description,
  long_description_content_type="text/markdown",
  author = 'Igor Kasianov',
  author_email = 'super.hang.glider@gmail.com',
  url = 'https://github.com/erebus1/graphene-federation',
  download_url = 'https://github.com/erebus1/graphene-federation/archive/0.0.1.tar.gz',
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