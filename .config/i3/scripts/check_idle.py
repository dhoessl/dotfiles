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


class Idler:
    def __init__(self, timeout) -> None:
        self.timer = 10
        self.timeout = timeout
        self.idle_message_send = False
        self.run()

    def run(self) -> None:
        while True:
            sleep(self.timer)
            idle_time = int(srun(['xprintidle'], capture_output=True).stdout.decode().split()[0]) // 1000
            if self.idle_message_send and idle_time < self.timeout / 2:
                self.idle_message_send = False
            elif not self.idle_message_send and idle_time > self.timeout / 2:
                srun(['notify-send', 'Your idling for about ' + str(self.timeout / 120) + ' minutes'])
                self.idle_message_send = True
            if idle_time > self.timeout:
                if srun('ps x | grep \'i3lock\' | grep -v grep', shell=True, capture_output=True).stdout.decode():
                    continue
                else:
                    if srun(['playerctl', 'status'], capture_output=True).stdout.decode().split()[0] == 'Playing':
                        srun(['playerctl', 'play-pause'])
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


if __name__ == '__main__':
    parser = Parser()
    args = parser.args
    Idler(args.idle_time)
