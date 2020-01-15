#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name="EmailOctopus",
      version="0.1",
      description="Email Octopus API wrapper",
      license="MIT",
      install_requires=["requests"],
      author="Doug Fenstermacher",
      author_email="douglas.fenstermacher@gmail.com",
      url="https://github.com/dpfens/EmailOctopuS",
      packages = find_packages(),
      keywords= "email",
      zip_safe = True)
