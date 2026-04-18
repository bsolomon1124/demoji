"""Find and replace emojis within text strings.

The set of emojis is refreshable from its canonical source at
https://unicode.org/Public/emoji/.
"""

__all__ = (
    "EMOJI_VERSION",
    "findall",
    "findall_list",
    "last_downloaded_timestamp",
    "replace",
    "replace_with_desc",
)
__version__ = "2.0.0"

import datetime
import importlib.resources
import json
import logging
import re
from typing import TypeAlias

logging.getLogger(__name__).addHandler(logging.NullHandler())

EMOJI_VERSION = "16.0"
URL = f"https://unicode.org/Public/emoji/{EMOJI_VERSION}/emoji-test.txt"

# Type alias for the bundled emoji → description mapping. (PEP 695 `type`
# statement requires Python 3.12+; using TypeAlias keeps 3.10/3.11 support.)
CodeMap: TypeAlias = dict[str, str]

# Variation selectors that commonly trail emoji sequences. When an input
# contains a stray U+FE0F (emoji presentation) or U+FE0E (text presentation)
# beside an emoji whose bundled entry doesn't include it, substitution leaves
# the selector orphaned. Strip these from replace-style output.
_ORPHAN_VS_PAT = re.compile(r"[\ufe0e\ufe0f]")


def _load_codes_from_file() -> CodeMap:
    data = (
        importlib.resources.files("demoji")
        .joinpath("codes.json")
        .read_text(encoding="utf-8")
    )
    return json.loads(data)


def _compile_codes(codes: CodeMap) -> re.Pattern[str]:
    # Sort longest-first so multi-codepoint sequences win over their prefixes.
    ordered = sorted(codes.keys(), key=lambda k: -len(k))
    return re.compile(r"|".join(re.escape(c) for c in ordered))


_CODE_TO_DESC: CodeMap = _load_codes_from_file()
_EMOJI_PAT: re.Pattern[str] = _compile_codes(_CODE_TO_DESC)


def findall(string: str) -> CodeMap:
    """Find emojis within ``string``. Return a mapping of ``{emoji: description}``."""
    return {f: _CODE_TO_DESC[f] for f in set(_EMOJI_PAT.findall(string))}


def findall_list(string: str, desc: bool = True) -> list[str]:
    """Find emojis within ``string``; return a list with possible duplicates.

    If ``desc`` is True, return descriptions; otherwise return the matched
    emoji substrings in order.
    """
    if desc:
        return [_CODE_TO_DESC[k] for k in _EMOJI_PAT.findall(string)]
    return _EMOJI_PAT.findall(string)


def replace(string: str, repl: str = "") -> str:
    """Replace emojis in ``string`` with ``repl``."""
    return _ORPHAN_VS_PAT.sub("", _EMOJI_PAT.sub(repl, string))


def replace_with_desc(string: str, sep: str = ":") -> str:
    """Replace emojis in ``string`` with their description, surrounded by ``sep``."""
    found = findall(string)
    result = string
    for emoji, desc in found.items():
        result = result.replace(emoji, sep + desc + sep)
    return _ORPHAN_VS_PAT.sub("", result)


# This variable is updated automatically from scripts/download_codes.py
_LDT = datetime.datetime(2026, 4, 18, 0, 0, 0, 0, tzinfo=datetime.timezone.utc)


def last_downloaded_timestamp() -> datetime.datetime:
    return _LDT


def set_emoji_pattern() -> None:
    """Retained for backwards compatibility; patterns are now compiled at import."""
