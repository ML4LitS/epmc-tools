
from setuptools import setup, find_packages

setup(
    name="europmc-dev-tool",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "beautifulsoup4",
        "lxml",
        "spacy",
        "scispacy",
        "tqdm",
        "rapidfuzz",
        "requests",
        "click",
    ],
    entry_points={
        "console_scripts": [
            "jatx2json=europmc_dev_tool.app:main",
            "epmc-cli=europmc_dev_tool.cli:cli",
        ],
    },
    author="Santosh Tirunagari",
    author_email="tsantosh7@gmail.com",
    description="A tool to extract structured JSON from JATS XML, with a focus on accession numbers.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/JATX2JSON",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
