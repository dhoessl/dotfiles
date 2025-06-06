#!/usr/bin/env python3

from psutil import process_iter
from os import remove, path
from pathlib import Path
from time import sleep


def collect_procs() -> list:
    openvpn_procs = []
    for proc in process_iter(['name']):
        if 'openvpn' in proc.info['name']:
            openvpn_procs.append(proc.info['name'])
    return openvpn_procs


def check_procs(proc_list) -> None:
    if ('nm-openvpn-service' in proc_list
            and not path.exists('/tmp/wavevpn.info')):
        Path('/tmp/wavevpn.info').touch()
    elif ('nm-openvpn-service' not in proc_list
            and path.exists('/tmp/wavevpn.info')):
        remove('/tmp/wavevpn.info')
    if ('openvpn' in proc_list
            and not path.exists('/tmp/norisvpn.info')):
        Path('/tmp/norisvpn.info').touch()
    elif ('openvpn' not in proc_list
            and path.exists('/tmp/wavevpn.info')):
        remove('/tmp/norisvpn.info')


if __name__ == '__main__':
    while True:
        proc_list = collect_procs()
        check_procs(proc_list)
        sleep(30)
