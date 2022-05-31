#!/usr/bin/python3

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('cmd', nargs='+')
args = parser.parse_args()

import os
import db
db.add(os.getlogin(), args.cmd, 20, -1, -1)
