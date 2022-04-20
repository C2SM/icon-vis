"""A setuptools based setup module.

See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name="icon-vis",  # Required
    version="1.0.0",  # Required
    description="A project for visualizing/plotting ICON",  # Optional
    long_description=long_description,  # Optional
    long_description_content_type="text/markdown",  # Optional (see note above)
    url="https://github.com/C2SM/icon-vis",  # Optional
    author="MeteoSwiss, C2SM",  # Optional
    author_email="victoria.cherkas@meteoswiss.ch, annika.lauber@c2sm.ethz.ch",  # Optional
    package_dir={"": "icon_vis"},  # Optional
    packages=find_packages(where="icon_vis"),  # Required
    python_requires=">=3.7, <4",
    install_requires=[],  # Optional
)
