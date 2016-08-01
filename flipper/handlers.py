from argparse import ArgumentParser
from . import japanese
from . import mecabwrapper

__all__ = [
    'SlackRTMHandler',
    'EchoHandler',
    'Flipper'
]


class SlackRTMHandler(object):

    type_to_method_name = {
        "hello": "_hello",
        "message": "_on_message",
    }

    def __init__(self, slack_wrapper):
        self.slack_wrapper = slack_wrapper
        self.at_bot = "<@{0}>:".format(self.slack_wrapper.botid)

    def handle(self, data):
        """
        """
        _type = data.get('type')
        method_name = self.type_to_method_name.get(_type)
        if method_name:
            f = getattr(self, method_name)
            f(data)

    def _hello(self, data):
        pass

    def _on_message(self, data):
        channel = data.get('channel')
        user = data.get('user')
        text = data.get('text')
        timestamp = data.get('ts')

        self.on_message(channel, user, text, timestamp)
        if self.slack_wrapper.botid == user:
            self.on_my_message(channel, user, text, timestamp)
        else:
            self.on_others_message(channel, user, text, timestamp)
        if self.at_bot in text:
            self.on_message_to_me(channel, user, text, timestamp)

    def on_message(self, channel, user, text, timestamp):
        pass

    def on_my_message(self, channel, user, text, timestamp):
        pass

    def on_others_message(self, channel, user, text, timestamp):
        pass

    def on_message_to_me(self, channel, user, text, timestamp):
        pass


class EchoHandler(SlackRTMHandler):
    """EchoHandler for debugging.
    """
    def __init__(self, slack_wrapper):
        super(EchoHandler, self).__init__(slack_wrapper)

    def on_message(self, channel, user, text, timestamp):
        print("EchoHandler::on_message({0}, {1}, {2}, {3})".format(
            channel, user, text, timestamp
        ))

    def on_my_message(self, channel, user, text, timestamp):
        print("EchoHandler::on_my_message({0}, {1}, {2}, {3})".format(
            channel, user, text, timestamp
        ))

    def on_others_message(self, channel, user, text, timestamp):
        print("EchoHandler::on_others_message({0}, {1}, {2}, {3})".format(
            channel, user, text, timestamp
        ))

    def on_message_to_me(self, channel, user, text, timestamp):
        print("EchoHandler::on_message_to_me({0}, {1}, {2}, {3})".format(
            channel, user, text, timestamp
        ))


class Flipper(SlackRTMHandler):
    """
    Flipper core.
    """
    def __init__(self, slack_wrapper):
        super(Flipper, self).__init__(slack_wrapper)
        self.jlpt = None

    def on_others_message(self, channel, user, text, timestamp):
        """
        """
        parser, options = self._parse_args(text)
        if options:
            if options.help:
                self.slack_wrapper.post(
                    channel, "```{0}```".format(parser.format_help())
                )
            self._set_options(options)
            return

        result = mecabwrapper.parse(text)

        text_with_furigana = ""
        if not self.jlpt:
            text_with_furigana = "".join(c.with_furigana for c in result)
        else:
            for c in result:
                # Checks if the text contains kanji which is in the specified JLPT level.
                if c.has_jlpt_kanji(level=self.jlpt):
                    # no furigana, because it is included in the specified JLPT level.
                    text_with_furigana += c
                else:
                    # with furigana
                    text_with_furigana += c.with_furigana
        self.slack_wrapper.post(channel, text_with_furigana)

    def _parse_args(self, text):
        if not text.startswith("flipper"):
            return None, None

        args = text.replace("flipper", "", 1).split()
        parser = ArgumentParser(description="", add_help=False)
        parser.add_argument(
            "-j", "--jlpt", dest="jlpt", type=int,
            default=None, help="Flipper's JLPT level"
        )
        parser.add_argument(
            "-h", "--help", dest="help", default=False,
            action='store_true', help="Print usage"
        )

        parsed = parser.parse_args(args=args)
        return parser, parsed

    def _set_options(self, options):
        if options.jlpt:
            self.jlpt = options.jlpt
