import os
import time
from .slackwrapper import SlackWrapper
from .exceptions import ExitCode, FlipperException, \
        SlackConnectionFailuer, InvalidSlackParam
from . import handlers

BOT_ID = os.environ.get("FLIPPER_BOT_ID")

FLIPPER_BOT_TOKEN = os.environ.get('FLIPPER_BOT_TOKEN')

slack_wrapper = SlackWrapper(botid=BOT_ID, token=FLIPPER_BOT_TOKEN)

DEFAULT_READ_WEBSOCKET_DELAY = 1

handlers = [
    handlers.EchoHandler(slack_wrapper),
    handlers.Flipper(slack_wrapper)
]


def check_environ():
    if not BOT_ID:
        raise InvalidSlackParam("Environment variable BOT_ID is empty")
    if not FLIPPER_BOT_TOKEN:
        raise InvalidSlackParam("Environment variable FLIPPER_BOT_TOKEN is empty")


def handle_message(output):
    for handler in handlers:
        handler.handle(output)


def parse_slack_output(slack_rtm_output):
    output_list = slack_rtm_output
    if output_list:
        for output in output_list:
            if output and 'text' in output:
                return output['text'], output['channel']
    return None, None


def main():
    try:
        check_environ()

        if not slack_wrapper.connect():
            raise SlackConnectionFailuer("Connection failed. Invalid Slack token or bot ID?")
        print("Flipper connected and running!")

        while True:
            output_list = slack_wrapper.rtm_read()
            if output_list:
                for output in output_list:
                    handle_message(output)

            time.sleep(DEFAULT_READ_WEBSOCKET_DELAY)
        return ExitCode.Success

    except FlipperException as e:
        print(e)
        return e.code
