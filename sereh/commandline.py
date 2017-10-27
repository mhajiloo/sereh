#!/usr/bin/env python
import argparse
import os
import re

from sereh.subfile import Subtitle

SHIFT_REGEX = r'^(-?\d+h)?(-?\d+m)?(-?\d+s)?(-?\d+ms)?$'


def shift_validator(string):
    if string is None:
        return string

    if not re.match(SHIFT_REGEX, string):
        raise argparse.ArgumentTypeError('must be in the form []h[]m[]s[]ms, eg. 1h22m1s100ms, 1400ms, -1h-22m')

    return string


class FullAbsPathAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, os.path.abspath(os.path.expanduser(values)))


class ShiftAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        shift = [int(re.sub('[^\d-]', '', x)) if x else 0 for x in re.findall(SHIFT_REGEX, values)[0]]
        setattr(namespace, self.dest, tuple(shift))


def main():
    parser = argparse.ArgumentParser(prog='sereh', description='Sereh Subtitle tools.')
    parser.add_argument('srt', type=str, help='Source subtitle path', action=FullAbsPathAction)
    parser.add_argument('-e', '--output-encoding', type=str, dest='encoding', default='utf-8', choices=['utf-8', 'cp1256'],
                        help='New subtitle encoding')
    parser.add_argument('-s', '--shift', type=shift_validator, dest='shift', action=ShiftAction, default=None, help='Shift subtitle')

    args = parser.parse_args()

    subtitle = Subtitle(args.srt)
    if args.shift is not None:
        subtitle.shift(*args.shift)

    subtitle.save(encoding=args.encoding)
