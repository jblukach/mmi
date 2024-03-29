from setuptools import setup

from mmi import __version__

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name = "matchmeta",
    version = __version__,
    description = "OS Triage for Anyone and Everyone",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/jblukach/mmi",
    author = "John Lukach",
    author_email = "hello@lukach.io",
    license = "Apache-2.0",
    packages = ["mmi"],
    install_requires = [
        "pybloomfiltermmap3",
        "requests"
    ],
    entry_points = {
        "console_scripts": [
            "mmi=mmi.cli:main"
        ],
    },
    python_requires = ">=3.7"
)