# demoji

Accurately find or remove [emojis](https://en.wikipedia.org/wiki/Emoji) from a blob of text using
data from the Unicode Consortium's [emoji code repository](https://unicode.org/Public/emoji/).

[![License](https://img.shields.io/github/license/bsolomon1124/demoji.svg)](https://github.com/bsolomon1124/demoji/blob/master/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/demoji.svg)](https://pypi.org/project/demoji/)
[![Status](https://img.shields.io/pypi/status/demoji.svg)](https://pypi.org/project/demoji/)
[![Python](https://img.shields.io/pypi/pyversions/demoji.svg)](https://pypi.org/project/demoji)

-------

## Install

```bash
pip install demoji
# or, with uv:
uv add demoji
```

`demoji` supports Python 3.10 – 3.14 and bundles Unicode emoji data (version 16.0) at install time,
so no network access is required at runtime. See [CHANGELOG.md](CHANGELOG.md) for the full history.

To report a regression, please [open a GitHub issue](https://github.com/bsolomon1124/demoji/issues/new?assignees=&labels=&template=bug_report.md&title=).

## Basic Usage

`demoji` exports several text-related functions for find-and-replace functionality with emojis:

```python
>>> tweet = """\
... #startspreadingthenews yankees win great start by 🎅🏾 going 5strong innings with 5k’s🔥 🐂
... solo homerun 🌋🌋 with 2 solo homeruns and👹 3run homerun… 🤡 🚣🏼 👨🏽‍⚖️ with rbi’s … 🔥🔥
... 🇲🇽 and 🇳🇮 to close the game🔥🔥!!!….
... WHAT A GAME!!..
... """
>>> demoji.findall(tweet)
{
    "🔥": "fire",
    "🌋": "volcano",
    "👨🏽\u200d⚖️": "man judge: medium skin tone",
    "🎅🏾": "Santa Claus: medium-dark skin tone",
    "🇲🇽": "flag: Mexico",
    "👹": "ogre",
    "🤡": "clown face",
    "🇳🇮": "flag: Nicaragua",
    "🚣🏼": "person rowing boat: medium-light skin tone",
    "🐂": "ox",
}
```

See [below](#reference) for function API.

## Command-line Use

You can use `demoji` or `python -m demoji` to replace emojis
in file(s) or stdin with their `:code:` equivalents:

```bash
$ cat out.txt
All done! ✨ 🍰 ✨
$ demoji out.txt
All done! :sparkles: :shortcake: :sparkles:

$ echo 'All done! ✨ 🍰 ✨' | demoji
All done! :sparkles: :shortcake: :sparkles:

$ demoji -
we didnt start the 🔥
we didnt start the :fire:
```

## Reference

```python
findall(string: str) -> Dict[str, str]
```

Find emojis within `string`.  Return a mapping of `{emoji: description}`.

```python
findall_list(string: str, desc: bool = True) -> List[str]
```

Find emojis within `string`.  Return a list (with possible duplicates).

If `desc` is True, the list contains description codes.  If `desc` is False, the list contains emojis.

```python
replace(string: str, repl: str = "") -> str
```

Replace emojis in `string` with `repl`.

```python
replace_with_desc(string: str, sep: str = ":") -> str
```

Replace emojis in `string` with their description codes.  The codes are surrounded by `sep`.

```python
last_downloaded_timestamp() -> datetime.datetime
```

Show the timestamp of last download for the emoji data bundled with the package.

## Footnote: Emoji Sequences

Numerous emojis that look like single Unicode characters are actually multi-character sequences.  Examples:

- The keycap 2️⃣ is actually 3 characters, U+0032 (the ASCII digit 2), U+FE0F (variation selector), and U+20E3 (combining enclosing keycap).
- The flag of Scotland 7 component characters, `b'\\U0001f3f4\\U000e0067\\U000e0062\\U000e0073\\U000e0063\\U000e0074\\U000e007f'` in full esaped notation.

(You can see any of these through `s.encode("unicode-escape")`.)

`demoji` is careful to handle this and should find the full sequences rather than their incomplete subcomponents.

The way it does this it to sort emoji codes by their length, and then compile a concatenated regular expression that will greedily search for longer emojis first, falling back to shorter ones if not found.  This is not by any means a super-optimized way of searching as it has O(N<sup>2</sup>) properties, but the focus is on accuracy and completeness.

```python
>>> from pprint import pprint
>>> seq = """\
... I bet you didn't know that 🙋, 🙋‍♂️, and 🙋‍♀️ are three different emojis.
... """
>>> pprint(seq.encode('unicode-escape'))  # Python 3
(b"I bet you didn't know that \\U0001f64b, \\U0001f64b\\u200d\\u2642\\ufe0f,"
 b' and \\U0001f64b\\u200d\\u2640\\ufe0f are three different emojis.\\n')
```
