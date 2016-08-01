from slackclient import SlackClient

__all__ = [
    'SlackWrapper',
]


class SlackWrapper(object):
    def __init__(self, slack_client=None, botid=None, token=None):
        self._slack_client = slack_client
        self.botid = botid
        self.token = token

    def connect(self):
        self._slack_client = SlackClient(self.token)
        return self._slack_client.rtm_connect()

    def rtm_read(self):
        return self._slack_client.rtm_read()

    def post(self, channel, message):
        self._slack_client.api_call(
            "chat.postMessage", channel=channel,
            text=message, as_user=True
        )
