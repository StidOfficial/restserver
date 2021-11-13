from setuptools import find_packages, setup

with open("README.md", "r") as readme:
  long_description = readme.read()

setup(
  name="restserver",
  version="0.0.1",
  description="Rest server python library",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/StidOfficial/restserver",
  packages=["restserver"],
)