import io
import os
from setuptools import setup


def find_version(filepath):
    version = None
    with io.open(filepath) as f:
        for line in f:
            if line.startswith("__version__"):
                version = line.partition("=")[-1].strip().strip("'\"")
    if not version:
        raise RuntimeError("Could not find version in __init__.py")
    return version


setup(
    name="demoji",
    version=find_version("demoji/__init__.py"),
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
    long_description=io.open(
        os.path.join(os.path.abspath(os.path.dirname(__file__)), "README.md"),
        encoding="utf-8",
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
    install_requires=["requests<3.0.0", "setuptools", "colorama"],
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*",
)
