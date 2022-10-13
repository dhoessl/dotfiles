#!/usr/bin/env python3

from os import path, listdir, remove
from re import match

CONFIG_FILE = path.join(path.expanduser('~'), '.config', 'i3', 'config')


def run():
    remove_old_config()
    config_dir, config_files = get_config_files()
    for config in config_files:
        with open(path.join(config_dir, config), 'r') as fp:
            delete_line = False
            for line in fp.readlines():
                if delete_line:
                    delete_line = False
                    continue
                elif match('##', line):
                    delete_line = True
                    continue
                else:
                    with open(CONFIG_FILE, 'a') as fp2:
                        fp2.write(line)


def get_config_files():
    user_dir = path.expanduser('~')
    config_dir = path.join(user_dir, '.config', 'i3', 'config.d')
    if path.exists(config_dir):
        try:
            return (config_dir, listdir(config_dir))
        except:
            print('Error while listing dir')
            exit(1)
    else:
        print('files and folder do not exist')
        exit(1)


def remove_old_config():
    if path.exists(CONFIG_FILE):
        remove(CONFIG_FILE)


if __name__ == '__main__':
    run()
