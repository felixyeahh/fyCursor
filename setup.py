
# ! usage: python3 setup.py sdist bdist_wheel
from setuptools import setup, find_packages

import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    LONG_DESCRIPTION = "\n" + fh.read()

# Setting up
setup(
    name="fyCursor",
    version="0.1.6",
    description='Simple sqlite3 cursor',
    author="felixyeahh",
    author_email="<felixyeah@outlook.com>",
    license="MIT",
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    keywords=['python', 'sqlite3', 'database'],
)
