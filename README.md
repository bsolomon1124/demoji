# demoji

Accurately find or remove [emojis](https://en.wikipedia.org/wiki/Emoji) from a blob of text.

[![License](https://img.shields.io/github/license/bsolomon1124/demoji.svg)](https://github.com/bsolomon1124/demoji/blob/master/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/demoji.svg)](https://pypi.org/project/demoji/)
[![Status](https://img.shields.io/pypi/status/demoji.svg)](https://pypi.org/project/demoji/)
[![Python](https://img.shields.io/pypi/pyversions/demoji.svg)](https://pypi.org/project/demoji)

-------

## Basic Usage

`demoji` requires an initial data download from the Unicode Consortium's [emoji code repository](http://unicode.org/Public/emoji/12.0/emoji-test.txt).

On first use of the package, call `download_codes()`:

```python
>>> import demoji
>>> demoji.download_codes()
Downloading emoji data ...
... OK (Got response in 0.14 seconds)
Writing emoji data to /Users/brad/.demoji/codes.json ...
... OK
```

This will store the Unicode hex-notated symbols at `~/.demoji/codes.json` for future use.

`demoji` exports two text-related functions, `findall()` and `replace()`, which behave somewhat the `re` module's `findall()` and `sub()`, respectively.  However, `findall()` returns a dictionary of emojis to their full name (description):

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

The reason that `demoji` requires a download rather than coming pre-packaged with Unicode emoji data is that the emoji list itself is frequently updated and changed.  You are free to periodically update the local cache by calling `demoji.download_codes()` every so often.

To pull your last-downloaded date, you can use the `last_downloaded_timestamp()` helper:

```python
>>> demoji.last_downloaded_timestamp()
datetime.datetime(2019, 2, 9, 7, 42, 24, 433776, tzinfo=<demoji.UTC object at 0x101b9ecf8>)
```

The result will be `None` if codes have not previously been downloaded.

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
