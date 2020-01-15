import argparse

from .texture_binds import run

parser = argparse.ArgumentParser()
inputgroup = parser.add_mutually_exclusive_group()
inputgroup.add_argument(
    '-f',
    dest='file',
    metavar='options.txt',
    nargs=1
)
inputgroup.add_argument(
    '-k',
    dest='keys',
    nargs=9,
    type=str
)
parser.add_argument(
    '--offset',
    nargs=2,
    type=int,
    metavar='int'
)
parser.add_argument(
    '--opacity',
    nargs=1,
    type=float,
    metavar='float'
)
parser.add_argument(
    'jar',
    nargs=1,
    type=str
)
args = parser.parse_args()
run(args)