import MeCab
from .japanese import Text

__all__ = [
    'WakatiTagger',
    'YomiTagger',
    'parse'
]


class Tagger(MeCab.Tagger):
    def __init__(self, *args):
        super(Tagger, self).__init__(*args)

    def parse(self, text):
        result = super(Tagger, self).parse(text)
        tokens = result.split()
        if len(tokens) > 1:
            return [Text(token.strip('\n')) for token in tokens]
        else:
            return Text(result.strip('\n'))


class WakatiTagger(Tagger):
    def __init__(self, *args):
        super(WakatiTagger, self).__init__("-Owakati", *args)


class YomiTagger(Tagger):
    def __init__(self, *args):
        super(YomiTagger, self).__init__("-Oyomi", *args)

    def parse(self, text):
        yomi = super(YomiTagger, self).parse(text)
        result = Text(text)
        result.furigana = yomi
        return result


wakati_tagger = WakatiTagger()

yomi_tagger = YomiTagger()


def parse(text):
    wakati, yomi = _parse_into_wakati_and_yomi(text)
    return yomi


def _parse_into_wakati_and_yomi(text):
    wakati = wakati_tagger.parse(text)
    yomi = [yomi_tagger.parse(w) for w in wakati]
    return wakati, yomi
