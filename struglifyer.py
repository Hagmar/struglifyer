#!/usr/bin/env python3

import argparse
import logging
import random
import re


class Struglifyer:
    def __init__(self, args):
        config = parse_config(args.config)
        self.token = config['token']
        self.uglifyers = config['uglifyers']


    def run(self, s, initial=False, iters=1):
        if initial:
            s = '"{}"'.format(s)

        for _ in range(iters):
            uf = random.choice(self.uglifyers)
            if uf['esc']:
                s = re.sub(r'(\\|")', r'\\\1', s)

            format_dict = { 's': s }
            s = uf['uglifyer'].format(**format_dict)
            print(s)


def parse_config(config_file):
    return {
        'token': '@x',
        'uglifyers': [
            {
                'uglifyer': '"%s" % {s}',
                'esc': False
            },
            {
                'uglifyer': '"{{}}".format({s})',
                'esc': False
            },
            {
                'uglifyer': '{s}[:]',
                'esc': False
            },
            {
                'uglifyer': '{s}[::-1][::-1]',
                'esc': False
            },
            {
                'uglifyer': '"%%%s"%"s"%{s}',
                'esc': False
            },
            {
                'uglifyer': '"".join(c for c in {s})',
                'esc': False
            },
            {
                'uglifyer': 'eval("{s}")',
                'esc': True
            }
        ]
    }


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--string', default='Hello, World!', help='The string')
    parser.add_argument('--config', help='Configuration file')
    parser.add_argument('--iters', type=int, default=1, help='Number of iterations')

    return parser.parse_args()


def main():
    args = parse_args()
    su = Struglifyer(args)
    su.run(args.string, initial=True, iters=args.iters)


if __name__ == '__main__':
    main()
