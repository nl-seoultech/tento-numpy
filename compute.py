# -*- coding: utf-8 -*-
import os

from argparse import ArgumentParser
from configparser import ConfigParser

from tento_num.io import read_n_write, dump_mp3
from tento_num.func import diff

parser = ArgumentParser(prog='compute')
sub = parser.add_subparsers(help='do stuff')
write = sub.add_parser('write', help='write a graph png')
write.set_defaults(command='write')
dump = sub.add_parser('dump', help='dump mp3 into json')
dump.set_defaults(command='dump')

diff = sub.add_parser('diff', help='diff mp3')
diff.set_defaults(command='diff')

parser.add_argument('-c', '--config', dest='config')


if __name__ == '__main__':
    args = parser.parse_args()
    config = ConfigParser()
    config.read(args.config)
    if args.command == 'write':
        read_n_write(config['dir']['read'], config['dir']['out'])
    elif args.command == 'dump':
        dump_mp3(config['dir']['mp3'], config['dir']['read'])
    elif args.command == 'diff':
        pass
