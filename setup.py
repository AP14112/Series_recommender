from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="web-series-recommender",
    version="0.1",
    author="Aryaman Prasad",
    packages=find_packages(),
    install_requires=requirements,
    
)
