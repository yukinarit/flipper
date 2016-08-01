import sys
from .n1 import kanji_list as n1_kanji_list
from .n2 import kanji_list as n2_kanji_list
from .n3 import kanji_list as n3_kanji_list
from .n4 import kanji_list as n4_kanji_list
from .n5 import kanji_list as n5_kanji_list

thismodule = sys.modules[__name__]

__all__ = [
    'has_kanji'
]

MIN_LEVEL = 1
MAX_LEVEL = 5


def has_kanji(level, text):
    if not level:
        raise RuntimeError("Level is None")
    if not MIN_LEVEL <= level <= MAX_LEVEL:
        raise RuntimeError("Level is out of range")

    for _level in range(level, MAX_LEVEL+1):
        kanji_list = getattr(thismodule, 'n{0}_kanji_list'.format(_level))
        if not kanji_list:
            return False

        for w in text:
            if w in kanji_list:
                return True

    return False
