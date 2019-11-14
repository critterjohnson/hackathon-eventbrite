from setuptools import setup, find_packages

setup(
    name="hackbi_eventbrite",
    version="0.1",
    description="some eventbrite tools for the hackbi team",
    author="Critter Johnson",
    author_email="critterjohnson45@gmail.com",
    packages=find_packages(),
    install_requires=["requests", "openpyxl"]
)
