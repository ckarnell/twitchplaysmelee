#! /usr/bin/env python
#
# Example program using client.
#
# This program is free without restrictions; do anything you like with
# it.
#
# Joel Rosdahl <joel@rosdahl.net>

import sys
import argparse
import itertools

from irc import client, ctcp
import jaraco.logging
import pyautogui

# TODO: make it more _dirty_
# from xdo import Xdo
target = None
"The nick or channel to which to send messages"


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
    # pyautogui.press('a')
    pyautogui.typewrite('a')
    message_string = '\n'.join(messages)
    print(f'{target}: {message_string}')


def main():
    global target

    # xdo = Xdo()
    # win_id = xdo.select_window_with_click()
    # print(win_id)
    # xdo.enter_text_window(win_id, 'Python rocks!')

    reactor = client.Reactor()
    # reactor._handle_message = _handle_message
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
    # print(type(c))
    c.process_data()
    reactor.process_forever()




if __name__ == '__main__':
    main()
