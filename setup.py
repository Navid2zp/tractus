import pathlib
import tractus
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="tractus",
    version=tractus.__version__,
    description="Trace a HTTP request and gather the performance metrics.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Navid2zp/tractus",
    author="Navid Zarepak",
    author_email="navid2zp@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    packages=find_packages(exclude=("tests",)),
)
