#!/usr/bin/env python3

from subprocess import run as srun
from argparse import ArgumentParser
from time import sleep


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


if __name__ == '__main__':
    parser = Parser()
    args = parser.args
    idle_message_send = False
    while True:
        sleep(10)
        idle_time = srun(['xprintidle'], capture_output=True).stdout.decode().split()[0]
        if idle_message_send and int(idle_time) // 1000 < args.idle_time / 2:
            idle_message_send = False
        elif not idle_message_send and int(idle_time) // 1000 > args.idle_time / 2:
            srun(['notify-send', 'Your idling for about ' + str(args.idle_time / 120) + ' minutes'])
            idle_message_send = True
        if int(idle_time) // 1000 > args.idle_time:
            if srun('ps x | grep \'i3lock\' | grep -v grep', shell=True, capture_output=True).stdout.decode():
                continue
            else:
                srun(['/home/dhoessl/.config/i3/scripts/lock.py'])
