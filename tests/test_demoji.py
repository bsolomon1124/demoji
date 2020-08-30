# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import datetime
import os
import re

import pytest

import demoji

person_tipping_hand = "💁"  # length 1
man_tipping_hand = "💁‍♂️"  # length 4
woman_tipping_hand = "💁‍♀️"  # length 4


@pytest.fixture
def tweet():
    return """\
#startspreadingthenews yankees win great start by 🎅🏾 going 5strong innings with 5k’s🔥 🐂
solo homerun 🌋🌋 with 2 solo homeruns and👹 3run homerun… 🤡 🚣🏼 👨🏽‍⚖️ with rbi’s … 🔥🔥
🇲🇽 and 🇳🇮 to close the game🔥🔥!!!….
WHAT A GAME!!..
"""


@pytest.fixture
def dt():
    return datetime.datetime(2010, 1, 1)


def test_utc(dt):
    utc = demoji.utc
    assert utc.tzname(dt) == 'UTC'
    assert utc.utcoffset(dt) == utc.dst(dt) == datetime.timedelta(0)
    now = datetime.datetime.utcnow().replace(tzinfo=demoji.utc)
    assert now.utcoffset() == datetime.timedelta(0)


def test_setup():
    if demoji.PY2:
        assert len(person_tipping_hand) == 2
        assert len(man_tipping_hand) == 5
        assert len(woman_tipping_hand) == 5
    else:
        assert len(person_tipping_hand) == 1
        assert len(man_tipping_hand) == 4
        assert len(woman_tipping_hand) == 4


def test_load_codes_from_file_raises_if_dne():
    if os.path.isfile(demoji.CACHEPATH):
        os.remove(demoji.CACHEPATH)
    with pytest.raises(IOError):
        demoji._load_codes_from_file()
    assert demoji.last_downloaded_timestamp() is None


def test_set_emoji_pattern_no_json_raises():
    if os.path.isfile(demoji.CACHEPATH):
        os.remove(demoji.CACHEPATH)
    with pytest.raises(IOError):
        demoji.set_emoji_pattern()
    assert demoji.last_downloaded_timestamp() is None


def test_download():
    assert demoji.download_codes() is None
    assert type(demoji._EMOJI_PAT) == type(re.compile(""))  # noqa
    assert isinstance(demoji._CODE_TO_DESC, dict)
    assert os.path.isfile(demoji.CACHEPATH)


def test_last_downloaded_timestamp_rettype():
    ts = demoji.last_downloaded_timestamp()
    assert isinstance(ts, datetime.datetime)


def test_demoji_main(tweet):
    assert not demoji.findall("Hi")
    assert demoji.replace("Hi") == "Hi"
    assert not demoji.findall("2 ! $&%((@)# $)@ ")
    assert demoji.findall("The 🌓 shall rise again") == {
        "🌓": "first quarter moon"
    }
    allhands = "Someone actually gets paid to make a %s, a %s, and a %s" % (
        person_tipping_hand,
        man_tipping_hand,
        woman_tipping_hand,
    )
    assert demoji.findall(allhands) == {
        person_tipping_hand: "person tipping hand",
        man_tipping_hand: "man tipping hand",
        woman_tipping_hand: "woman tipping hand",
    }
    assert (
        demoji.replace(allhands)
        == "Someone actually gets paid to make a , a , and a "
    )
    assert (
        demoji.replace(allhands, "X")
        == "Someone actually gets paid to make a X, a X, and a X"
    )
    assert isinstance(demoji.last_downloaded_timestamp(), datetime.datetime)

    # Something for everyone...
    batch = [
        "😀",
        "😂",
        "🤩",
        "🤐",
        "🤢",
        "🙁",
        "😫",
        "🙀",
        "💓",
        "🧡",
        "🖤",
        "👁️‍🗨️",
        "✋",
        "🤙",
        "👊",
        "🙏",
        "👂",
        "👱‍♂️",
        "🧓",
        "🙍‍♀️",
        "🙋",
        "🙇",
        "👩‍⚕️",
        "👩‍🔧",
        "👨‍🚒",
        "👼",
        "🦸",
        "🧝‍♀️",
        "👯‍♀️",
        "🤽",
        "🤼‍♀️",
        "🏴󠁧󠁢󠁳󠁣󠁴󠁿",
        "👩‍👧‍👦",
        "🐷",
        "2️⃣",
        "8️⃣",
        "🆖",
        "🈳",
        "الجزيرة‎",
        "傳騰訊入股Reddit 言論自由不保?",
        "🇩🇯",
        "⬛",
        "🔵",
        "🇨🇫",
        "‼",
    ]
    assert len(demoji.findall(" xxx ".join(batch))) == len(batch) - 2
    assert demoji.findall(tweet) == {
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


def test_utils():
    assert (
        demoji.parse_unicode_sequence("1F468 200D 2764 FE0F 200D 1F468")
        == "\U0001F468\U0000200D\U00002764\U0000FE0F\U0000200D\U0001F468"
    )
    assert demoji.parse_unicode_sequence("1F468") == "\U0001F468"
    assert list(demoji.parse_unicode_range("2648..2653")) == [
        "♈",
        "♉",
        "♊",
        "♋",
        "♌",
        "♍",
        "♎",
        "♏",
        "♐",
        "♑",
        "♒",
        "♓",
    ]


def test_findall_list(tweet):
    assert len(demoji.findall_list(tweet, True)) \
        == len(demoji.findall_list(tweet, False))
    assert demoji.findall_list(tweet, True)
    assert demoji.findall_list(tweet, False)
    assert 'santa claus' in demoji.findall_list(tweet, True)[0].lower()
    assert '🔥' == demoji.findall_list(tweet, False)[1]


def test_replace_with_desc(tweet):
    assert demoji.replace_with_desc(tweet, ":") == '#startspreadingthenews yankees win great start by :Santa Claus: medium-dark skin tone: going 5strong innings with 5k’s:fire: :ox:\nsolo homerun :volcano::volcano: with 2 solo homeruns and:ogre: 3run homerun… :clown face: :person rowing boat: medium-light skin tone: :man judge: medium skin tone: with rbi’s … :fire::fire:\n:flag: Mexico: and :flag: Nicaragua: to close the game:fire::fire:!!!….\nWHAT A GAME!!..\n'
    assert demoji.replace_with_desc(tweet, "|") == '#startspreadingthenews yankees win great start by |Santa Claus: medium-dark skin tone| going 5strong innings with 5k’s|fire| |ox|\nsolo homerun |volcano||volcano| with 2 solo homeruns and|ogre| 3run homerun… |clown face| |person rowing boat: medium-light skin tone| |man judge: medium skin tone| with rbi’s … |fire||fire|\n|flag: Mexico| and |flag: Nicaragua| to close the game|fire||fire|!!!….\nWHAT A GAME!!..\n'
