from setuptools import find_packages, setup

setup(
  name="restserver",
  packages=find_packages(include=["restserver"]),
  version="0.0.1",
  description="Rest server python library",
  author="StidOfficial",
  license="",
  install_requires=[],
  setup_requires=[],
  test_suite="tests"
)