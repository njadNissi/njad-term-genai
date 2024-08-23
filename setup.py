from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.0.1'
DESCRIPTION = 'Use gemini at your preferred terminal'
LONG_DESCRIPTION = 'A package that allows to use gemini (generative AI model from google) without opening a browser. this helps you ask questions about code and bugs without low ram resources usage.'

# Setting up
setup(
    name="njad-term-genai",
    version=VERSION,
    author="Njad Nissi",
    author_email="<njadnissi@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['google-generativeai', 'pyfiglet'],
    keywords=['python', 'generative ai', 'terminal'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
