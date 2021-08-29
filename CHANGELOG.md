# Changelog

## 1.1.0 (unreleased)

- Add a `__main.py__` to allow running `python -m demoji`;
  permit stdin (`-`), file name(s), or piped stdin.

## 1.0.0

**This is a backwards-incompatible release with several substantial changes.**

The largest change is that `demoji` now bundles a static copy of Unicode
emoji data with the package at install time, rather than requiring a runtime
download of the codes from unicode.org.

Changes below are grouped by their corresponding
[Semantic Versioning](https://semver.org/) identifier.

SemVer MAJOR:

- Drop support for Python 2 and Python 3.5
- The `demoji` package now bundles emoji data that is distributed with the
  package at install time, rather than requiring a download of the codes
  from the unicode.org site at runtime (closes #23)
- As a result of the above change, the following functions are **removed**
  from the `demoji` API:
  - `download_codes()`
  - `parse_unicode_sequence()`
  - `parse_unicode_range()`
  - `stream_unicodeorg_emojifile()`

SemVer MINOR:

- The `demoji.DIRECTORY` and `demoji.CACHEPATH` attributes are deprecated
  due to no longer being functionally in used by the package. Accessing them
  will warn with a `FutureWarning`, and these attributes may be removed
  completely in a future release
- `demoji` can now be installed with optional `ujson` support for faster loading
  of emoji data from file (versus the standard library's `json`, which is the
  default); use `python -m pip install demoji[ujson]`
- The dependencies `requests` and `colorama` have been removed completely
- `importlib_resources` (a backport module) is now required for Python < 3.7
- The `EMOJI_VERSION` attribute, newly added to `demoji`, is a `str` denoting
  the Unicode database version in use

SemVer PATCH:

- Fix a typo in `demoji.__all__` to properly include `demoji.findall_list()`
- Internal change: Functions that call `set_emoji_pattern()` are now decorated
  with a `@cache_setter` to set the cache
- Some unit tests have been removed to update the change in behavior from
  downloading codes to bundling codes with install
- Update README to reflect bundling behavior

## 0.4.0

- Update emoji source list to version 13.1. (See 5090eb5.)
- Formally support Python 3.9. (See 6e9c34c.)
- Bugfix: ensure that `demoji.last_downloaded_timestamp()` returns correct UTC time.
  (See 6c8ad15.)

## 0.3.0

- Feature: add `findall_list()` and `replace_with_desc()` functions. (See 7cea333.)
- Modernize setup config to use `setup.cfg`. (See 8f141e7.)

## 0.2.1

- Tox: formally add Python 3.8 tests.

## 0.2.0

- Windows: use the [colorama] package to support printing ANSI escape sequences on Windows;
  this introduces colorama as a dependency.  (See cd343c1.)
- Setup: Fix a bug in `setup.py` that would require dependencies to be installed
  _prior to_ installation of `demoji` in order to find the `__version__`.
  (See d5f429c.)
- Python 2 + Windows support: use `io.open(..., encoding='utf-8')` consistently in `setup.py`.
  (See 1efec5d.)
- Distribution: use a universal wheel in PyPI release. (See 8636a32.)

[colorama]: https://github.com/tartley/colorama

## 0.1.5

- Performance improvement: use `re.escape()` rather than failing to compile a small subset of codes.
- Remove an unused constant in `__init__.py`.
