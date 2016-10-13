#!/usr/local/bin/python3.5

import re
from sys import argv

isFn = lambda fn: hasattr(fn, '__call__')

def call(val, args=None):
    return val(args) if isFn(val) else val

def getNextVersion(args):
  release = args[-2]
  version = APPDATA['version'].split('.')

  if release == 'patch':
    nnext = str(int(version[-1]) + 1)
    version[-1] = nnext

  if release == 'minor':
    version[-2] = str(int(version[-2]) + 1)
    version[-1] = '0'

  if release == 'major':
    version[-3] = str(int(version[-3]) + 1)
    version[-2] = '0'
    version[-1] = '0'

  return '.'.join(version)

def trace(argv):
  print(argv)

def update(args):
  version = args[-2]
  filename = args[-3]
  with open(filename, 'r') as f:
    content = f.read()
    
    if filename == 'setup.py':
      content = re.sub(r"version = '\d+\.\d+\.\d+'", "version = '{}'".format(version), content)
      content = re.sub(r"v\d+\.\d+\.\d+", "v{}".format(version), content)

    if filename == 'lib.py':
      content = re.sub(r"'version': '\d+\.\d+\.\d+'", "'version': '{}'".format(version), content)

    return content

APPDATA = {
  'version': '0.1.1',
  'next-version': getNextVersion,
  'trace': trace,
  'update': update
}

print(call(APPDATA[argv[-1]], argv))




