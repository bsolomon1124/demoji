# Changelog

### 0.2.0

- Windows: use the [colorama] package to support printing ANSI escape sequences on Windows;
  this introduces colorama as a dependency.  (See cd343c1.)
- Setup: Fix a bug in `setup.py` that would require dependencies to be installed
  _prior to_ installation of `demoji` in order to find the `__version__`.
  (See d5f429c.)
- Python 2 + Windows support: use `io.open(..., encoding='utf-8')` consistently in` setup.py`.
  (See 1efec5d.)
- Distribution: use a universal wheel in PyPI release. (See 8636a32.)

[colorama]: https://github.com/tartley/colorama

### 0.1.5

- Performance improvement: use `re.escape()` rather than failing to compile a small subset of codes.
- Remove an unused constant in `__init__.py`.
