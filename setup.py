import os
from setuptools import setup

from demoji import __version__

# PyPI upload:
# $ python setup.py sdist bdist_wheel
# $ twine upload dist/demoji-x.y.z*

setup(
    name="demoji",
    version=__version__,
    author="Brad Solomon",
    author_email="brad.solomon.1124@gmail.com",
    description="Accurately remove and replace emojis in text strings.",
    license="Apache 2.0",
    keywords=[
        "emoji",
        "emojis",
        "nlp",
        "natural langauge processing",
        "unicode",
    ],
    url="https://github.com/bsolomon1124/demoji",
    packages=["demoji"],
    long_description=open(
        os.path.join(os.path.abspath(os.path.dirname(__file__)), "README.md")
    ).read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "Topic :: Text Processing",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    install_requires=["requests<3.0.0", "setuptools"],
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
)
