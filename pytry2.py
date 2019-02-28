import sys
import argparse
import itertools
import subprocess

from irc import client, ctcp
import jaraco.logging
import time

KEY_MAPPINGS_TUPLE = [
    # Left
    ('left', ['SET MAIN 0 0.5', 'SET MAIN 0.5 0.5']),
    ('l', ['SET MAIN 0 0.5', 'SET MAIN 0.5 0.5']),

    # Right
    ('right', ['SET MAIN 1 0.5', 'SET MAIN 0.5 0.5']),
    ('r', ['SET MAIN 1 0.5', 'SET MAIN 0.5 0.5']),

    # Up
    ('up', ['SET MAIN 0.5 0', 'SET MAIN 0.5 0.5']),
    ('u', ['SET MAIN 0.5 0', 'SET MAIN 0.5 0.5']),

    # Down
    ('down', ['SET MAIN 0.5 1', 'SET MAIN 0.5 0.5']),
    ('d', ['SET MAIN 0.5 1', 'SET MAIN 0.5 0.5']),

    # B
    ('b', ['PRESS B', 'RELEASE B']),

    # B right
    ('rb', ['SET MAIN 1 0.5', 'PRESS B', 'RELEASE B', 'SET MAIN 0.5 0.5']),
    ('br', ['SET MAIN 1 0.5', 'PRESS B', 'RELEASE B', 'SET MAIN 0.5 0.5']),
    ('right-b', ['SET MAIN 1 0.5', 'PRESS B', 'RELEASE B', 'SET MAIN 0.5 0.5']),
    ('b-right', ['SET MAIN 1 0.5', 'PRESS B', 'RELEASE B', 'SET MAIN 0.5 0.5']),
    ('bright', ['SET MAIN 1 0.5', 'PRESS B', 'RELEASE B', 'SET MAIN 0.5 0.5']),
    ('rightb', ['SET MAIN 1 0.5', 'PRESS B', 'RELEASE B', 'SET MAIN 0.5 0.5']),

    # B left
    ('lb', ['SET MAIN 0 0.5', 'PRESS B', 'RELEASE B', 'SET MAIN 0.5 0.5']),
    ('bl', ['SET MAIN 0 0.5', 'PRESS B', 'RELEASE B', 'SET MAIN 0.5 0.5']),
    ('b-left', ['SET MAIN 0 0.5', 'PRESS B', 'RELEASE B', 'SET MAIN 0.5 0.5']),
    ('left-b', ['SET MAIN 0 0.5', 'PRESS B', 'RELEASE B', 'SET MAIN 0.5 0.5']),
    ('bleft', ['SET MAIN 0 0.5', 'PRESS B', 'RELEASE B', 'SET MAIN 0.5 0.5']),
    ('leftb', ['SET MAIN 0 0.5', 'PRESS B', 'RELEASE B', 'SET MAIN 0.5 0.5']),

    # B up
    ('ub', ['SET MAIN 0.5 0', 'PRESS B', 'RELEASE B', 'SET MAIN 0.5 0.5']),
    ('bu', ['SET MAIN 0.5 0', 'PRESS B', 'RELEASE B', 'SET MAIN 0.5 0.5']),
    ('up-b', ['SET MAIN 0.5 0', 'PRESS B', 'RELEASE B', 'SET MAIN 0.5 0.5']),
    ('b-up', ['SET MAIN 0.5 0', 'PRESS B', 'RELEASE B', 'SET MAIN 0.5 0.5']),
    ('upb', ['SET MAIN 0.5 0', 'PRESS B', 'RELEASE B', 'SET MAIN 0.5 0.5']),
    ('bup', ['SET MAIN 0.5 0', 'PRESS B', 'RELEASE B', 'SET MAIN 0.5 0.5']),

    # B down
    ('db', ['SET MAIN 0.5 1', 'PRESS B', 'RELEASE B', 'SET MAIN 0.5 0.5']),
    ('bd', ['SET MAIN 0.5 1', 'PRESS B', 'RELEASE B', 'SET MAIN 0.5 0.5']),
    ('b-down', ['SET MAIN 0.5 1', 'PRESS B', 'RELEASE B', 'SET MAIN 0.5 0.5']),
    ('down-b', ['SET MAIN 0.5 1', 'PRESS B', 'RELEASE B', 'SET MAIN 0.5 0.5']),
    ('bdown', ['SET MAIN 0.5 1', 'PRESS B', 'RELEASE B', 'SET MAIN 0.5 0.5']),
    ('downb', ['SET MAIN 0.5 1', 'PRESS B', 'RELEASE B', 'SET MAIN 0.5 0.5']),

    # A
    ('a', ['PRESS A', 'RELEASE A']),

    # Grab
    ('grab', ['PRESS Z', 'RELEASE Z']),
    ('z', ['PRESS Z', 'RELEASE Z']),

    # Shield
    ('s', ['PRESS L', 'RELEASE L']),
    ('shield', ['PRESS L', 'RELEASE L']),

    # Tilt up
    ('ut', ['SET MAIN 0.5 0.4', 'PRESS A', 'RELEASE A', 'SET MAIN 0.5 0.5']),
    ('tu', ['SET MAIN 0.5 0.4', 'PRESS A', 'RELEASE A', 'SET MAIN 0.5 0.5']),
    ('tup', ['SET MAIN 0.5 0.4', 'PRESS A', 'RELEASE A', 'SET MAIN 0.5 0.5']),
    ('upt', ['SET MAIN 0.5 0.4', 'PRESS A', 'RELEASE A', 'SET MAIN 0.5 0.5']),
    ('up-tilt', ['SET MAIN 0.5 0.4', 'PRESS A', 'RELEASE A', 'SET MAIN 0.5 0.5']),
    ('tilt-up', ['SET MAIN 0.5 0.4', 'PRESS A', 'RELEASE A', 'SET MAIN 0.5 0.5']),
    ('uptilt', ['SET MAIN 0.5 0.4', 'PRESS A', 'RELEASE A', 'SET MAIN 0.5 0.5']),
    ('tiltup', ['SET MAIN 0.5 0.4', 'PRESS A', 'RELEASE A', 'SET MAIN 0.5 0.5']),

    # Tilt left
    ('lt', ['SET MAIN 0.4 0.5', 'PRESS A', 'RELEASE A', 'SET MAIN 0.5 0.5']),
    ('tl', ['SET MAIN 0.4 0.5', 'PRESS A', 'RELEASE A', 'SET MAIN 0.5 0.5']),
    ('tleft', ['SET MAIN 0.4 0.5', 'PRESS A', 'RELEASE A', 'SET MAIN 0.5 0.5']),
    ('leftt', ['SET MAIN 0.4 0.5', 'PRESS A', 'RELEASE A', 'SET MAIN 0.5 0.5']),
    ('left-tilt', ['SET MAIN 0.4 0.5', 'PRESS A', 'RELEASE A', 'SET MAIN 0.5 0.5']),
    ('tilt-left', ['SET MAIN 0.4 0.5', 'PRESS A', 'RELEASE A', 'SET MAIN 0.5 0.5']),
    ('lefttilt', ['SET MAIN 0.4 0.5', 'PRESS A', 'RELEASE A', 'SET MAIN 0.5 0.5']),
    ('tiltleft', ['SET MAIN 0.4 0.5', 'PRESS A', 'RELEASE A', 'SET MAIN 0.5 0.5']),

    # Tilt down
    ('dt', ['SET MAIN 0.5 0.6', 'PRESS A', 'RELEASE A', 'SET MAIN 0.5 0.6']),
    ('td', ['SET MAIN 0.5 0.6', 'PRESS A', 'RELEASE A', 'SET MAIN 0.5 0.6']),
    ('tdown', ['SET MAIN 0.5 0.6', 'PRESS A', 'RELEASE A', 'SET MAIN 0.5 0.6']),
    ('downt', ['SET MAIN 0.5 0.6', 'PRESS A', 'RELEASE A', 'SET MAIN 0.5 0.6']),
    ('down-tilt', ['SET MAIN 0.5 0.6', 'PRESS A', 'RELEASE A', 'SET MAIN 0.5 0.6']),
    ('tilt-down', ['SET MAIN 0.5 0.6', 'PRESS A', 'RELEASE A', 'SET MAIN 0.5 0.6']),
    ('downtilt', ['SET MAIN 0.5 0.6', 'PRESS A', 'RELEASE A', 'SET MAIN 0.5 0.6']),
    ('tiltdown', ['SET MAIN 0.5 0.6', 'PRESS A', 'RELEASE A', 'SET MAIN 0.5 0.6']),

    # Tilt right
    ('rt', ['SET MAIN 0.6 0.5', 'PRESS A', 'RELEASE A', 'SET MAIN 0.6 0.5']),
    ('tr', ['SET MAIN 0.6 0.5', 'PRESS A', 'RELEASE A', 'SET MAIN 0.6 0.5']),
    ('tright', ['SET MAIN 0.6 0.5', 'PRESS A', 'RELEASE A', 'SET MAIN 0.6 0.5']),
    ('rightt', ['SET MAIN 0.6 0.5', 'PRESS A', 'RELEASE A', 'SET MAIN 0.6 0.5']),
    ('right-tilt', ['SET MAIN 0.6 0.5', 'PRESS A', 'RELEASE A', 'SET MAIN 0.6 0.5']),
    ('tilt-right', ['SET MAIN 0.6 0.5', 'PRESS A', 'RELEASE A', 'SET MAIN 0.6 0.5']),
    ('righttilt', ['SET MAIN 0.6 0.5', 'PRESS A', 'RELEASE A', 'SET MAIN 0.6 0.5']),
    ('tiltright', ['SET MAIN 0.6 0.5', 'PRESS A', 'RELEASE A', 'SET MAIN 0.6 0.5']),

    # C up
    ('uc', ['SET C 0.5 0', 'SET C 0.5 0.5']),
    ('cu', ['SET C 0.5 0', 'SET C 0.5 0.5']),
    ('cup', ['SET C 0.5 0', 'SET C 0.5 0.5']),
    ('upc', ['SET C 0.5 0', 'SET C 0.5 0.5']),
    ('up-smash', ['SET C 0.5 0', 'SET C 0.5 0.5']),
    ('smash-up', ['SET C 0.5 0', 'SET C 0.5 0.5']),
    ('upsmash', ['SET C 0.5 0', 'SET C 0.5 0.5']),
    ('smashup', ['SET C 0.5 0', 'SET C 0.5 0.5']),

    # C left
    ('lc', ['SET C 0 0.5', 'SET C 0.5 0.5']),
    ('cl', ['SET C 0 0.5', 'SET C 0.5 0.5']),
    ('cleft', ['SET C 0 0.5', 'SET C 0.5 0.5']),
    ('leftc', ['SET C 0 0.5', 'SET C 0.5 0.5']),
    ('left-smash', ['SET C 0 0.5', 'SET C 0.5 0.5']),
    ('leftsmash', ['SET C 0 0.5', 'SET C 0.5 0.5']),
    ('smash-left', ['SET C 0 0.5', 'SET C 0.5 0.5']),
    ('smashleft', ['SET C 0 0.5', 'SET C 0.5 0.5']),

    # C down
    ('dc', ['SET C 0.5 1', 'SET C 0.5 0.5']),
    ('cd', ['SET C 0.5 1', 'SET C 0.5 0.5']),
    ('cdown', ['SET C 0.5 1', 'SET C 0.5 0.5']),
    ('downc', ['SET C 0.5 1', 'SET C 0.5 0.5']),
    ('down-smash', ['SET C 0.5 1', 'SET C 0.5 0.5']),
    ('downsmash', ['SET C 0.5 1', 'SET C 0.5 0.5']),
    ('smash-down', ['SET C 0.5 1', 'SET C 0.5 0.5']),
    ('smashdown', ['SET C 0.5 1', 'SET C 0.5 0.5']),

    # C right
    ('rc', ['SET C 1 0.5', 'SET C 0.5 0.5']),
    ('cr', ['SET C 1 0.5', 'SET C 0.5 0.5']),
    ('cright', ['SET C 1 0.5', 'SET C 0.5 0.5']),
    ('rightc', ['SET C 1 0.5', 'SET C 0.5 0.5']),
    ('smash-right', ['SET C 1 0.5', 'SET C 0.5 0.5']),
    ('smashright', ['SET C 1 0.5', 'SET C 0.5 0.5']),
    ('right-smash', ['SET C 1 0.5', 'SET C 0.5 0.5']),
    ('rightsmash', ['SET C 1 0.5', 'SET C 0.5 0.5']),

    # Taunt
    ('taunt', ['PRESS D_UP', 'RELEASE D_UP']),

    # Start
    ('start', ['PRESS START', 'RELEASE START']),

    # Jump
    ('jump', ['SET MAIN 0.5 0', 'SET MAIN 0.5 0', 'SET MAIN 0.5 0.5']),
    ('j', ['SET MAIN 0.5 0', 'SET MAIN 0.5 0', 'SET MAIN 0.5 0.5'],),

    # Short hop
    ('short-hop', ['SET MAIN 0.5 0', 'SET MAIN 0.5 0.5']),
    ('shorthop', ['SET MAIN 0.5 0', 'SET MAIN 0.5 0.5']),
    ('short-jump', ['SET MAIN 0.5 0', 'SET MAIN 0.5 0.5']),
    ('shortjump', ['SET MAIN 0.5 0', 'SET MAIN 0.5 0.5']),
    ('sh', ['SET MAIN 0.5 0', 'SET MAIN 0.5 0.5']),
    ('sj', ['SET MAIN 0.5 0', 'SET MAIN 0.5 0.5']),

    # Change player
    ('p1', ['p1']),
    ('p2', ['p2']),

    # Advanced Tech
    ('wdr', [
        'SET MAIN 1 1',
        'PRESS X',
        'RELEASE X',
        'PRESS R',
        'RELEASE R',
        'SET MAIN 0.5 0.5',
    ]),
    ('wdl', [
        'SET MAIN 0 1',
        'PRESS X',
        'RELEASE X',
        'PRESS R',
        'RELEASE R',
        'SET MAIN 0.5 0.5',
    ]),

    # misc
    ('toggle-color', ['PRESS X', 'RELEASE X']),
    ('help', ['help']),

    # privileged
    ('mod-end-game', [
        'PRESS L',
        'PRESS R',
        'PRESS A',
        'PRESS START',
        'RELEASE L',
        'RELEASE R',
        'RELEASE A',
        'RELEASE START',
    ]),
    ('mod-end', [
        'PRESS L',
        'PRESS R',
        'PRESS A',
        'PRESS START',
        'RELEASE L',
        'RELEASE R',
        'RELEASE A',
        'RELEASE START',
    ]),
    ('mod-jig', [
        'SET MAIN 0.5 0.4',
        'PRESS A',
        'RELEASE A',
        'SET MAIN 0.5 0.5',
        'SET MAIN 0.5 0.5',
        'SET MAIN 0.5 0.5',
        'SET MAIN 0.5 0.5',
        'SET MAIN 0.5 0.5',
        'SET MAIN 0.5 0.5',
        'SET MAIN 0.5 0.5',
        'SET MAIN 0.5 0.5',
        'SET MAIN 0.5 0.5',
        'SET MAIN 0.5 0.5',
        'SET MAIN 0.5 0.5',
        'SET MAIN 0.5 0.5',
        'PRESS X',
        'RELEASE X',
        'SET MAIN 0.5 0.5',
        'SET MAIN 0.5 0.5',
        'SET MAIN 0.5 0.5',
        'SET MAIN 0.5 0.7',
        'PRESS B',
        'RELEASE B',
        'SET MAIN 0.5 0.5'
    ]),
]

KEY_MAPPINGS = {}
# TODO: make it more _dirty_
# from xdo import Xdo
target = None
"The nick or channel to which to send messages"

# 2 frames
DELAY = 1.0 / 30


def on_connect(connection, event):
    if client.is_channel(target):
        connection.join(target)
        return
    main_loop(connection)


def on_join(connection, event):
    main_loop(connection)


def get_lines():
    while True:
        yield sys.stdin.readline().strip()


def main_loop(connection):
    # print(connection)
    for line in itertools.takewhile(bool, get_lines()):
        print(line)
        connection.privmsg(target, line)
    connection.quit("Using client.py")


def on_disconnect(connection, event):
    raise SystemExit()


P1_FILENAME = '~/Library/Application\\ Support/Dolphin/Pipes/pipe1'
P2_FILENAME = '~/Library/Application\\ Support/Dolphin/Pipes/pipe2'

MODS = ['jigaleepoof', 'twitchplays', 'mrjaeger00']


class TwitchPlays:
    def __init__(self, connection):
        self.user_to_pipe = {}
        self.connection = connection

    def handle_message(self, arguments, command, source, tags):
        target, msg = arguments[:2]
        messages = ctcp.dequote(msg)
        # print(source)
        # print(tags)
        user_name = source.split('!')[0]
        if user_name not in self.user_to_pipe:
            # Give the user mod privileges so they can input the same command
            # multiple times quickly
            self.connection.privmsg('#trialsparkplays', f'/mod {user_name}')
            print(f'Registering {user_name}')
            self.user_to_pipe[user_name] = P1_FILENAME

        for message in messages:
            if message.startswith('mod') and user_name not in MODS:
                return
            potential_actions = KEY_MAPPINGS.get(message.strip())
            if potential_actions:
                for action in potential_actions:
                    if action == 'p1':
                        self.user_to_pipe[user_name] = P1_FILENAME
                    elif action == 'p2':
                        self.user_to_pipe[user_name] = P2_FILENAME
                    else:
                        print(action)
                        subprocess.Popen(
                            f'echo "{action}" > {self.user_to_pipe[user_name]}',
                            shell=True)
                        time.sleep(DELAY)

        message_string = '\n'.join(messages)
        print(f'{user_name}: {message_string}')


def main():
    global target
    global KEY_MAPPINGS_TUPLE
    global KEY_MAPPINGS

    KEY_MAPPINGS = {t[0]: t[1] for t in KEY_MAPPINGS_TUPLE}
    if len(KEY_MAPPINGS_TUPLE) != len(KEY_MAPPINGS.keys()):
        keys = [tup[0] for tup in KEY_MAPPINGS_TUPLE]
        dupes = set([x for x in keys if keys.count(x) > 1])
        raise ValueError(f'There are duplicate keys in the key mappings tuple. They are: {dupes}')

    reactor = client.Reactor()
    try:
        c = reactor.server().connect(
            'irc.twitch.tv',
            6667,
            'trialsparkplays',
            password='oauth:gwy1392cwr35hgyvilzo460dkc27en')
    except client.ServerConnectionError:
        print(sys.exc_info()[1])
        raise SystemExit(1)

    twitch_plays = TwitchPlays(connection=c)
    setattr(c, '_handle_message', twitch_plays.handle_message)
    c.join('#trialsparkplays')

    print('Connected!')
    c.privmsg(
        '#trialsparkplays',
        'You control the characters! View available commands here: https://gist.github.com/ckarnell/38d7db3ef9a71da521bfd9fb73ca547e'
    )
    c.process_data()
    reactor.process_forever()


if __name__ == '__main__':
    main()
