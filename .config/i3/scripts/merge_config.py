#!/usr/bin/env python3

from os import path, listdir, remove
from re import match
from shutil import copyfile
from subprocess import run as subrun

CONFIG_FILE = path.join(path.expanduser('~'), '.config', 'i3', 'config')


def run():
    remove_old_config()
    config_dir, config_files = get_config_files()
    backup('create')
    try:
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
    except:
        backup('recover')
        subrun(['notify-send', '--urgency', 'critical', 'Something went wrong while creating new config - reset to backup'])
        exit(1)
    backup('delete')


def get_config_files():
    user_dir = path.expanduser('~')
    config_dir = path.join(user_dir, '.config', 'i3', 'config.d')
    if path.exists(config_dir):
        try:
            config_files_list = listdir(config_dir)
            config_files_list.sort()
            return (config_dir, config_files_list)
        except:
            subrun(['notify-send', '--urgency', 'critical', 'Error while listing dir'])
            exit(1)
    else:
        subrun(['notify-send', '--urgency', 'critical', 'files and folder do not exist'])
        exit(1)


def remove_old_config():
    if path.exists(CONFIG_FILE):
        remove(CONFIG_FILE)


def backup(state):
    conf_file_bak = path.join(path.expanduser('~'), '.config', 'i3', 'config.bak')
    if state == 'create' and path.exists(CONFIG_FILE):
        if path.exists(conf_file_bak):
            remove(conf_file_bak)
        copyfile(CONFIG_FILE, conf_file_bak)
    elif state == 'delete' and path.exists(conf_file_bak):
        remove(conf_file_bak)
    elif state == 'recover' and path.exists(conf_file_bak):
        if path.exists(CONFIG_FILE):
            remove(CONFIG_FILE)
        copyfile(conf_file_bak, CONFIG_FILE)


if __name__ == '__main__':
    run()
    subrun(['notify-send', 'Config successfully build - You can reload now'])
    exit(0)
