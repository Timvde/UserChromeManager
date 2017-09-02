#!/usr/bin/env python3

from constants import *
from exceptions import NotInitializedException
from re import match
from os import listdir, mkdir
from os.path import join, isdir, exists


def error_in_file():
    print('This file has been manually edited.')
    print('Please manually fix it to be consistent.')
    exit(1)


def get_userchrome_folder():
    profiles = [directory for directory in listdir(path=TOP_PROFILE_FOLDER)
                          if match(PROFILE_REGEX, directory)
                          and isdir(join(TOP_PROFILE_FOLDER, directory))]
    print('Choose your profile folder:')
    for index, profile in enumerate(profiles):
        print(str(index) + '. ' + profile)
    while True:
        try:
            choice = int(input('Choice: '))
            if 0 <= choice < len(profiles):
                break;
            else:
                print('That is not a valid choice.')
        except:
            print('Please enter only the number.')
    return join(TOP_PROFILE_FOLDER, profiles[choice],USERCHROME_FOLDER)


def get_userchrome_file(folder):
    if not isdir(userchrome_folder):
        mkdir(userchrome_folder)
    userchrome_file = join(userchrome_folder, USERCHROME_FILE)
    print(userchrome_file)
    if not exists(userchrome_file):
        open(userchrome_file, 'a').close()
    return userchrome_file


def get_start_index(lines):
    for index, line in enumerate(lines):
        if line == UCM_HEADER:
            return index
    raise NotInitializedException('UCM header not found.')


def get_end_index(lines, start):
    for index, line in enumerate(lines[start:]):
        if line == UCM_FOOTER:
            return index + start
    error_in_file()


def check_consistency(lines, start, end):
    for index in range(start, end):
        if not match(IMPORT_REGEX, lines[index]):
            error_in_file()
    if not lines[end] == NAMESPACE_LINE:
        error_in_file()


def write_to_file(filename, lines, line_number):
    with open(filename, 'r+') as f:
        original_lines = f.readlines()
        f.seek(line_number)
        f.writelines(original_lines[:line_number])
        f.writelines(lines)
        f.writelines(original_lines[line_number:])


def init_userchrome(userchrome_handle):
    initial_content = [UCM_HEADER, NAMESPACE_LINE, UCM_FOOTER]
    # We want our header at the top
    write_to_file(userchrome_handle, initial_content, 0)


def get_ucm_section(userchrome_file):
    with open(userchrome_file, 'r') as f:
        lines = f.readlines()
    try:
        start = get_start_index(lines)
    except NotInitializedException:
        init_userchrome(userchrome_file)
        with open(userchrome_file, 'r') as f:
            lines = f.readlines()
        # It definitely exists now
        start = get_start_index(lines)
    end = get_end_index(lines, start)
    check_consistency(lines, start+1, end-1)
    return start, end


if __name__ == '__main__':
    userchrome_folder = get_userchrome_folder()
    userchrome_file = get_userchrome_file(userchrome_folder)
    start, end = get_ucm_section(userchrome_file)
