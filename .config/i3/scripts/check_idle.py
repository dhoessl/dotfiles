#!/usr/bin/env python3

from subprocess import run as srun
from subprocess import Popen
from argparse import ArgumentParser
from time import sleep
import lock
from os import remove


class Parser:
    def __init__(self) -> None:
        parser = ArgumentParser()
        self.__set_args(parser)
        self.args = parser.parse_args()

    def __set_args(self, parser) -> None:
        parser.add_argument(
            '--idle-time',
            help='Set the seconds after which the lock should be started',
            type=int,
            default=1800
        )
        parser.add_argument(
            '--idle-time-away',
            help='Set the seconds after which the lock'
            'should be started if not in home wifi',
            type=int,
            default=300
        )


class Idler:
    def __init__(self, args) -> None:
        self.timer = 10
        self.timeout_home = args.idle_time
        self.timeout_work = args.idle_time_away
        self.idle_message_send = False
        self.run()

    def run(self) -> None:
        while True:
            sleep(self.timer)
            idle_time = int(
                srun(
                    ['xprintidle'],
                    capture_output=True
                ).stdout.decode().split()[0]
            ) // 1000
            if (is_home()
                    and self.idle_message_send
                    and idle_time < self.timeout_home / 2):
                self.idle_message_send = False
            elif (not is_home()
                    and self.idle_message_send
                    and idle_time < self.timeout_work / 2):
                self.idle_message_send = False
            elif (is_home()
                    and not self.idle_message_send
                    and idle_time > self.timeout_home / 2):
                srun([
                    'notify-send',
                    'Your idling for about '
                    + str(self.timeout_home / 120)
                    + ' minutes'
                ])
                self.idle_message_send = True
            elif (not is_home()
                    and not self.idle_message_send
                    and idle_time > self.timeout_work / 2):
                srun([
                    'notify-send',
                    'Your idling for about '
                    + str(self.timeout_work / 120)
                    + ' minutes'
                ])
                self.idle_message_send = True
            if i3lock_running():
                continue
            elif ((is_home()
                    and idle_time > self.timeout_home)
                    or (not is_home()
                        and idle_time > self.timeout_work)):
                pause_player()
                idle_lock = Lock()
                idle_lock.run()


class Lock:
    def __init__(self) -> None:
        self.lock_location = '/tmp/lock.png'
        lock.create_lockscreen(self.lock_location)

    def run(self) -> None:
        prog_lock = Popen(['i3lock', '-i', self.lock_location])
        prog_lock.wait()
        remove(self.lock_location)


def pause_player() -> None:
    ''' Check if playerctl is running
        If so stop it
    '''
    try:
        playerctl_output = srun(
            [
                'playerctl',
                'status'
            ],
            capture_output=True
        ).stdout.decode().split()[0]
    except:  # noqa: E722
        playerctl_output = 'Pause'
    if playerctl_output == 'Playing':
        srun(['playerctl', 'play-pause'])


def i3lock_running() -> bool:
    ''' Check if i3lock already running'''
    ps_output = srun(
        'ps x |grep \'i3lock\' | grep -v grep',
        shell=True,
        capture_output=True
    ).stdout.decode()
    if ps_output:
        return True
    else:
        return False


def is_home() -> bool:
    ''' Check if I am at home
        If there is the connected device laze.wlan in
        nmcli devices im prob at home
    '''
    nmcli_output = srun(
        ['nmcli', 'dev'],
        capture_output=True
    ).stdout.decode()
    if 'laze.wlan' in nmcli_output:
        return True
    else:
        return False


if __name__ == '__main__':
    parser = Parser()
    args = parser.args
    Idler(args)
