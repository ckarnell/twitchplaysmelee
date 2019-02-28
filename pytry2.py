import sys
import argparse
import itertools

from irc import client, ctcp
import jaraco.logging
import time


KEY_MAPPINGS = {
    'left': ['SET MAIN 0 .5', 'SET MAIN .5 .5'],
    'right': ['SET MAIN 1 .5', 'SET MAIN .5 .5'],
    'up': ['SET MAIN .5 1', 'SET MAIN .5 .5'],
    'down': ['SET MAIN .5 0', 'SET MAIN .5 .5'],
    'special': ['PRESS B', 'RELEASE B'],
    'attack': ['PRESS A', 'RELEASE A'],
    'shield': ['PRESS L', 'RELEASE L'],
    'grab': ['PRESS Z', 'RELEASE Z'],
    'c-up': ['SET C .5 1', 'SET C .5 .5'],
    'c-down': ['SET C .5 0', 'SET C .5 .5'],
    'c-left': ['SET C 0 .5', 'SET C .5 .5'],
    'c-right': ['SET C 1 .5', 'SET C .5 .5'],
    'taunt': ['PRESS D_UP', 'RELEASE D_UP'],
}
# TODO: make it more _dirty_
# from xdo import Xdo
target = None
"The nick or channel to which to send messages"

DELAY=0.1

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


def handle_message(arguments, command, source, tags):
    target, msg = arguments[:2]
    messages = ctcp.dequote(msg)

    for message in messages:
        potential_actions = KEY_MAPPINGS.get(message.strip())
        if potential_actions:
            with open('/Users/ericborczuk/Library/Application Support/Dolphin/Pipes/pipe1', 'w') as pipe:
                for action in potential_actions:
                    print(action)
                    pipe.write(action)
                    time.sleep(DELAY)

    message_string = '\n'.join(messages)
    print(f'{target}: {message_string}')


def main():
    global target

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

    setattr(c, '_handle_message', handle_message)
    c.join('#trialsparkplays')

    c.privmsg('#trialsparkplays', 'Commands: <TODO: write something>')
    c.process_data()
    reactor.process_forever()




if __name__ == '__main__':
    main()
