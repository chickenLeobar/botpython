import typing as t
import environ

# this modules is shared across all modules


import re

env = environ.Env()

env.read_env()


def find_all_words(words, sentence):
    all_words = re.findall(r'\w+', sentence)
    words_found = []
    for word in words:
        if word in all_words:
            words_found.append(word)
    return words_found


def resolver_payload(output: t.Optional[t.Any]):
    for event in output['entry']:
        messaging = event['messaging']
        for x in messaging:
            if x.get('message'):
                recipient_id = x['sender']['id']
                source = {
                    'rid': recipient_id
                }
                if x['message'].get('text'):
                    message = x['message']['text']
                    source.update({
                        'type': 'message',
                        'payload': message,

                    })
                    yield source
                if x['message'].get('attachments'):
                    source.update({
                        'type': 'attachments',
                        'payload': x['message'].get('attachments')
                    })
                    yield source


from difflib import SequenceMatcher


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()
