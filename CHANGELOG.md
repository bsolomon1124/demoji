# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- License changed from Apache-2.0 to MIT.

## [2.0.0] - 2026-04-18

### Added

- Bundled Unicode emoji data updated to version 16.0 (from 13.1). Closes #32 and
  #33 — emoji sequences such as `🫶🏻` (heart hands with skin tone) and the
  `🧑🏻‍❤️‍💋‍🧑🏼` family of "kiss: person, person" sequences are now recognized.
- GitHub Actions CI workflow running lint, format, type check, and tests
  across Python 3.10 – 3.14.
- `ruff` for lint + format and [`ty`](https://github.com/astral-sh/ty) for
  type checking.

### Changed

- Moved to a `src/` layout. `demoji` now lives at `src/demoji/`.
- Switched the build backend to [`uv_build`](https://docs.astral.sh/uv/) and
  consolidated all project metadata into `pyproject.toml`.
- Emoji patterns are now compiled once at import time instead of lazily.

### Fixed

- `replace()` and `replace_with_desc()` now strip orphaned U+FE0F / U+FE0E
  variation selectors left in the output when the input contains a stray
  selector. Closes #25.

### Removed

- Support for Python ≤ 3.9. Supported interpreters are now 3.10, 3.11, 3.12,
  3.13, and 3.14.
- `setup.py`, `setup.cfg`, `MANIFEST.in`, `tox.ini`, `.coveragerc`,
  `requirements.txt`, and `requirements/`.
- The optional `ujson` extra; the stdlib `json` module is used exclusively.
- The deprecated `DIRECTORY`, `CACHEPATH`, and `download_codes` module-level
  attributes.
- `black` and `flake8` (replaced by `ruff`).

### Deprecated

- The module-level `set_emoji_pattern()` is retained as a no-op for backwards
  compatibility and may be removed in a future major release.

## [1.1.0] - 2021-07-27

### Added

- `__main__.py` to allow running `python -m demoji`.
- `demoji` console entry-point command.
- Support for stdin (`-`), filename arguments, or piped stdin. Contribution by
  @jap.

## [1.0.0] - 2021-06-11

**Backwards-incompatible release.** `demoji` now bundles a static copy of
Unicode emoji data with the package at install time rather than downloading
codes from unicode.org at runtime.

### Added

- Bundled emoji data shipped with the package (closes #23).
- `EMOJI_VERSION` attribute denoting the Unicode database version in use.
- Optional `ujson` extra for faster loading of emoji data
  (`pip install demoji[ujson]`).
- `importlib_resources` backport required on Python < 3.7.

### Changed

- Internal: functions that call `set_emoji_pattern()` are now decorated with a
  `@cache_setter` to set the cache.
- README updated to reflect bundling behavior.

### Removed

- Support for Python 2 and Python 3.5.
- `download_codes()`, `parse_unicode_sequence()`, `parse_unicode_range()`, and
  `stream_unicodeorg_emojifile()` from the public API.
- The `requests` and `colorama` runtime dependencies.
- Unit tests that asserted the old download-at-runtime behavior.

### Deprecated

- `demoji.DIRECTORY` and `demoji.CACHEPATH`. Accessing them warns with a
  `FutureWarning`.

### Fixed

- Typo in `demoji.__all__` that omitted `demoji.findall_list()`.

## [0.4.0] - 2021-01-26

### Added

- Formal support for Python 3.9.

### Changed

- Updated emoji source list to version 13.1.

### Fixed

- `demoji.last_downloaded_timestamp()` returns correct UTC time.

## [0.3.0] - 2020-04-25

### Added

- `findall_list()` and `replace_with_desc()` functions.

### Changed

- Modernized setup config to use `setup.cfg`.

## [0.2.1] - 2019-12-03

### Added

- Formal Python 3.8 tests via tox.

## [0.2.0] - 2019-09-10

### Added

- Windows support: use [colorama] to support printing ANSI escape sequences on
  Windows. This introduces colorama as a dependency.
- Universal wheel in PyPI release.

### Fixed

- `setup.py` bug that required dependencies to be installed prior to installing
  `demoji` in order to find `__version__`.
- Python 2 + Windows: use `io.open(..., encoding="utf-8")` consistently in
  `setup.py`.

## [0.1.5] - 2019-07-30

### Changed

- Performance improvement: use `re.escape()` rather than failing to compile a
  small subset of codes.

### Removed

- Unused constant in `__init__.py`.

[colorama]: https://github.com/tartley/colorama
[Unreleased]: https://github.com/bsolomon1124/demoji/compare/v2.0.0...HEAD
[2.0.0]: https://github.com/bsolomon1124/demoji/compare/v1.1.0...v2.0.0
[1.1.0]: https://github.com/bsolomon1124/demoji/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/bsolomon1124/demoji/compare/v0.4.0...v1.0.0
[0.4.0]: https://github.com/bsolomon1124/demoji/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/bsolomon1124/demoji/compare/v0.2.1...v0.3.0
[0.2.1]: https://github.com/bsolomon1124/demoji/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/bsolomon1124/demoji/compare/v0.1.5...v0.2.0
[0.1.5]: https://github.com/bsolomon1124/demoji/releases/tag/v0.1.5
