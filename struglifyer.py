#!/usr/bin/env python3

from collections import defaultdict
import argparse
import logging
import random
import re
import string


class Struglifyer:
    def __init__(self, args):
        config = parse_config(args.config)
        self.uglifyers = config['uglifyers']

    def run(self, s, initial=False, iters=1):
        if initial:
            s = '"{}"'.format(s)

        for _ in range(iters):
            uf = random.choice(self.uglifyers)
            if uf.get('esc'):
                s = re.sub(r'(\\|")', r'\\\1', s)

            format_dict = {'s': s}

            for requirement in uf.get('requires', []):
                if requirement['type'] == str:
                    value = ''.join(
                            random.choice(string.ascii_letters)
                            for _ in range(requirement['len']))
                format_dict[requirement['name']] = value

            s = uf['uglifyer'].format(**format_dict)
            print(s)


def parse_config(config_file):
    return {
        'uglifyers': [
            {'uglifyer': '"%s" % {s}'},
            {'uglifyer': '"{{}}".format({s})'},
            {'uglifyer': '{s}[:]'},
            {'uglifyer': '{s}[::-1][::-1]'},
            {'uglifyer': '"%%%s"%"s"%{s}'},
            {'uglifyer': '"".join(c for c in {s})'},
            {
                'uglifyer': 'eval("{s}")',
                'esc': True
            },
            {
                'uglifyer': '"{{{x}}}".format(**{{"{x}":{s}}})',
                'requires': [
                    {
                        'name': 'x',
                        'type': str,
                        'len': 1
                    }
                ]
            },
            {
                'uglifyer': '(lambda {x}: {x})({s})',
                'requires': [
                    {
                        'name': 'x',
                        'type': str,
                        'len': 1
                    }
                ]
            }
        ]
    }


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--string', default='Hello, World!',
                        help='The string')
    parser.add_argument('--config', help='Configuration file')
    parser.add_argument('--iters', type=int, default=1,
                        help='Number of iterations')

    return parser.parse_args()


def main():
    args = parse_args()
    su = Struglifyer(args)
    su.run(args.string, initial=True, iters=args.iters)


if __name__ == '__main__':
    main()
