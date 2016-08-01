from . import jlpt

__all__ = [
    'is_hiragana',
    'is_katakana',
    'is_kanji',
    'has_kanji',
    'to_hiragana',
    'to_katakana',
    'Text'
]


def is_hiragana(characters):
    if characters is None:
        return False

    for c in characters:
        code_point = ord(c)
        if 0x3040 <= code_point <= 0x309F:
            pass
        else:
            return False
    return True


def is_katakana(characters):
    if characters is None:
        return False

    for c in characters:
        code_point = ord(c)
        if 0x30A0 <= code_point <= 0x30FF:
            pass
        else:
            return False
    return True


def is_kanji(characters):
    if characters is None:
        return False

    for c in characters:
        code_point = ord(c)
        if 0x4E00 <= code_point <= 0x9FD5:
            return True
        else:
            return False
    return True


def has_kanji(text):
    for character in text:
        if is_kanji(character):
            return True
    return False


def to_hiragana(text):
    """Convert text to hiragana form.
    """
    return "".join([hiragana_table.get(c, c) for c in text])


def to_katakana(text):
    """Convert text to katakana form.
    """
    return "".join([katakana_table.get(c, c) for c in text])


class Text(str):
    """A string wrapper with furigana/hiragana/katakana interface.
    """
    def __init__(self, *args, **kwargs):
        str.__init__(*args, **kwargs)
        self._furigana = None

    @property
    def hiragana(self):
        """Returns hiragana.
        """
        _text = self.__str__()
        if has_kanji(_text):
            _text = self.furigana

        if is_hiragana(_text):
            return _text
        elif is_katakana(_text):
            return to_hiragana(_text)
        else:
            return ""

    @property
    def katakana(self):
        """Returns katakana.
        """
        _text = self.__str__()
        if has_kanji(_text):
            _text = self.furigana

        if is_hiragana(_text):
            return to_katakana(_text)
        elif is_katakana(_text):
            return _text
        else:
            return ""

    @property
    def furigana(self):
        """Setter for furigana.
        """
        if is_hiragana(self) or is_katakana(self):
            return self
        else: 
            return self._furigana

    @furigana.setter
    def furigana(self, value):
        """Returns furigana.
        """
        if is_hiragana(value):
            self._furigana = value
        elif is_katakana(value):
            self._furigana = to_hiragana(value)
        else:
            self._furigana = value

    @property
    def with_furigana(self):
        """Returns string with furigana.
        """
        if self.furigana and self != self.furigana:
            return "{0}({1})".format(self.__str__(), self.furigana)
        else:
            return self

    def is_hiragana(self):
        """Check if this text is all hiraagna.
        """
        return is_hiragana(text)

    def is_katakana(self):
        """Check if this text is all katakana.
        """
        return is_katakana(self)

    def has_jlpt_kanji(self, level=None):
        """Check if the text contains specified JLPT level kanji.
        """
        _text = self.__str__()
        rv = jlpt.has_kanji(level, _text)
        print("jlpt.has_kanji {0}, {1}, {2}".format(level, _text, rv))
        return rv

    def __getattribute__(self, name):
        """ """
        attr = str.__getattribute__(self, name)
        if hasattr(attr, '__call__'):
            def newfunc(*args, **kwargs):
                result = attr(*args, **kwargs)
                if hasattr(result, '__iter__'):
                    if isinstance(result, tuple):
                        return (Text(x) for x in result)
                    elif isinstance(result, list):
                        return [Text(x) for x in result]
                if isinstance(result, str):
                    return Text(result)
                else:
                    return result
            return newfunc
        else:
            return attr


hiragana_table = {
    "ア":  "あ",
    "イ":  "い",
    "ウ":  "う",
    "エ":  "え",
    "オ":  "お",

    "カ":  "か",
    "キ":  "き",
    "ク":  "く",
    "ケ":  "け",
    "コ":  "こ",

    "サ":  "さ",
    "シ":  "し",
    "ス":  "す",
    "セ":  "せ",
    "ソ":  "そ",

    "タ":  "た",
    "チ":  "ち",
    "ツ":  "つ",
    "テ":  "て",
    "ト":  "と",

    "ナ":  "な",
    "ニ":  "に",
    "ヌ":  "ぬ",
    "ネ":  "ね",
    "ノ":  "の",

    "ハ":  "は",
    "ヒ":  "ひ",
    "フ":  "ふ",
    "ヘ":  "へ",
    "ホ":  "ほ",

    "マ":  "ま",
    "ミ":  "み",
    "ム":  "む",
    "メ":  "め",
    "モ":  "も",

    "ヤ":  "や",
    "ユ":  "ゆ",
    "ヨ":  "よ",

    "ラ": "ら",
    "リ": "り",
    "ル": "る",
    "レ": "れ",
    "ロ": "ろ",

    "ワ":  "わ",
    "ヲ":  "を",
    "ン":  "ん",

    "ガ":  "が",
    "ギ":  "ぎ",
    "グ":  "ぐ",
    "ゲ":  "げ",
    "ゴ":  "ご",

    "ザ":  "ざ",
    "ジ":  "じ",
    "ズ":  "ず",
    "ゼ":  "ぜ",
    "ゾ":  "ぞ",

    "ダ":  "だ",
    "ヂ":  "ぢ",
    "ヅ":  "づ",
    "デ":  "で",
    "ド":  "ど",

    "バ":  "ば",
    "ビ":  "び",
    "ブ":  "ぶ",
    "ベ":  "べ",
    "ボ":  "ぼ",

    "パ":  "ぱ",
    "ピ":  "ぴ",
    "プ":  "ぷ",
    "ペ":  "ぺ",
    "ポ":  "ぽ",

    "ァ":  "ぁ",
    "ィ":  "ぃ",
    "ゥ":  "ぃ",
    "ェ":  "ぇ",
    "ォ":  "ぉ",
    "ッ":  "っ",
    "ャ":  "ゃ",
    "ュ":  "ゅ",
    "ョ":  "ょ",
}

katakana_table = {v: k for k, v in hiragana_table.items()}

hiragana_list = katakana_table.keys()

katakana_list = hiragana_table.keys()
