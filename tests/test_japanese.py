import context
import flipper.mecabwrapper
from flipper.japanese import is_hiragana, is_katakana, is_kanji, Text
from flipper.jlpt import n1_kanji_list, n2_kanji_list, n3_kanji_list, \
        n4_kanji_list, n5_kanji_list, has_kanji


def test_is_hiragana():
    assert is_hiragana("あ")
    assert is_hiragana("ぃ")
    assert is_hiragana("ん")
    assert is_hiragana("ば")
    assert is_hiragana("ぞ")
    assert is_hiragana("ぱ")
    assert not is_hiragana("ア")
    assert not is_hiragana("_")
    assert not is_hiragana("漢")
    assert is_hiragana("せいぞう")
    assert not is_hiragana("セイゾウ")


def test_is_katakana():
    assert is_katakana('ア')
    assert is_katakana('ィ')
    assert is_katakana('ン')
    assert is_katakana('バ')
    assert is_katakana('パ')
    assert not is_katakana('あ')
    assert not is_katakana('_')
    assert not is_katakana('漢')
    assert not is_katakana("せいぞう")
    assert is_katakana("セイゾウ")


def test_is_kanji():
    assert is_kanji('漢')
    assert is_kanji('漢字')
    assert not is_kanji('これ漢字じゃない')


def test_translation():
    pass


def test_text():
    text = Text("あいうえお")
    assert "あいうえお" == text
    assert "あいうえお" == text.hiragana
    assert "アイウエオ" == text.katakana
    assert "あいうえお" == text.with_furigana

    text = Text("あ い う え お")
    aiueo_list = text.split()
    assert "あ" == aiueo_list[0]
    assert "い" == aiueo_list[1]
    assert "う" == aiueo_list[2]
    assert "え" == aiueo_list[3]
    assert "お" == aiueo_list[4]
    assert isinstance(aiueo_list, list)
    assert isinstance(aiueo_list[0], Text)
    assert isinstance(aiueo_list[1], Text)
    assert isinstance(aiueo_list[2], Text)
    assert isinstance(aiueo_list[3], Text)
    assert isinstance(aiueo_list[4], Text)
    assert "あ" == aiueo_list[0].hiragana
    assert "ア" == aiueo_list[0].katakana
    assert "あ" == aiueo_list[0].with_furigana

    text = Text("漢字のてすと")
    assert not text.hiragana
    assert not text.katakana
    assert not text.furigana
    assert "漢字のてすと" == text.with_furigana

    text.furigana = "カンジノテスト"
    assert "かんじのてすと" == text.hiragana
    assert "カンジノテスト" == text.katakana
    assert "かんじのてすと" == text.furigana
    assert "漢字のてすと(かんじのてすと)" == text.with_furigana


def test_jlpt():
    assert "氏" in n1_kanji_list
    assert "氏" not in n2_kanji_list
    assert "氏" not in n3_kanji_list
    assert "氏" not in n4_kanji_list
    assert "氏" not in n5_kanji_list

    assert Text("氏") in n1_kanji_list
    assert Text("氏") not in n2_kanji_list
    assert Text("氏") not in n3_kanji_list
    assert Text("氏") not in n4_kanji_list
    assert Text("氏") not in n5_kanji_list

    assert has_kanji(level=5, text="日本")
    assert not has_kanji(level=5, text="薔薇")

    assert Text("日本").has_jlpt_kanji(level=5)
    assert not Text("薔薇").has_jlpt_kanji(level=5)


def test_parse():
    result = flipper.mecabwrapper.parse("私は日本から来ました")
    assert "私は日本から来ました" == "".join([w for w in result])
    assert "わたしはにっぽんからきました" == "".join([w.furigana for w in result])
    assert "私(わたし)は日本(にっぽん)から来(き)ました" == "".join(
        [w.with_furigana for w in result]
    )
