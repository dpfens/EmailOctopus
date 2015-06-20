#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name="EmailOctopusAPI",
      version="0.9",
      description="Email Octopus API wrapper",
      license="MIT",
      install_requires=["requests","pyopenssl","ndg-httpsclient", "pyasn1"],
      author="Doug Fenstermacher",
      author_email="douglas.fenstermacher@gmail.com",
      url="https://github.com/dpfens/EmailOctopusAPI",
      packages = find_packages(),
      keywords= "email",
      zip_safe = True)