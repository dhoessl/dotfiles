#!/usr/bin/env python3

from argparse import ArgumentParser
from subprocess import run


def get_args():
    parser = ArgumentParser(description='Program to switch desktop layouts')
    parser.add_argument(
        '--laptop',
        '-l',
        help='set active display to laptop only',
        action='store_true'
    )
    parser.add_argument(
        '--desktop',
        '-d',
        help='set active display to desktop if available',
        action='store_true'
    )
    parser.add_argument(
        '--mixed',
        '-m',
        help='used laptop and desktop display',
        action='store_true'
    )
    parser.add_argument(
        '--reset',
        '-r',
        help='reset the settings',
        action='store_true'
    )
    return parser.parse_args()


def get_display_info():
    info = {'primary': None, 'secondary': None}
    displays = run(
        "xrandr | grep ' connected' | awk '{ print $1 }'",
        shell=True,
        capture_output=True
    ).stdout.decode().split()
    for display in displays:
        if 'eDP' in display:
            info['primary'] = display
        else:
            info['secondary'] = display
    return info


def main(args):
    display_info = get_display_info()
    if args.laptop and display_info['primary']:
        run(
            [
                'xrandr', '--output', display_info['primary'],
                '--auto', '--primary'
            ]
        )
        if display_info['secondary']:
            run(['xrandr', '--output', display_info['secondary'], '--off'])
    elif (args.desktop and display_info['primary']
            and display_info['secondary']):
        run([
            'xrandr',
            '--output', display_info['secondary'], '--auto', '--primary',
            '--output', display_info['primary'], '--off'
        ])
    elif args.mixed and display_info['primary'] and display_info['secondary']:
        run([
            'xrandr',
            '--output', display_info['primary'], '--auto',
            '--output', display_info['secondary'], '--auto',
            '--primary', '--left-of', display_info['primary']
        ])
    else:
        args.reset = True
    if args.reset:
        run(
            [
                'xrandr', '--output', display_info['primary'],
                '--auto', '--primary'
            ]
        )
        if display_info['secondary']:
            run(['xrandr', '--output', display_info['secondary'], '--off'])


if __name__ == '__main__':
    args = get_args()
    main(args)
