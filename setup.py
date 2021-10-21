from setuptools import setup

with open("README", "r") as f:
    long_description = f.read()

setup(
    name="eBay Webscraper",
    version="1.0",
    description="webscraper and data analysis tool",
    license="MIT",
    author="Mikayla Rivera",
    packages=["eBay Webscraper"],
    install_requires=["requests", "beautifulsoup4", "lxml"],
)
