#!/usr/bin/env python
#
# LaunchBar Action Script
#
import io
import os
import sys
import random
import string

try:
    mode = sys.argv[1]
except IndexError:
    mode = 'simple'

# placeholder in templates
# n: number
# c: character
# C: upper character
# s: special character (e.g. '% @ _ #')
templates = {
    'simple': 'nncccccccc',
    'number': 'nnnnnnnnnn',
    'char': 'cccccccccc',
    'strong': 'nCsccccccccc'
}


class CharGenerator(object):

    def _gen_c(self):
        return random.choice(string.ascii_lowercase)

    def _gen_C(self):
        return random.choice(string.ascii_uppercase)

    def _gen_n(self):
        return random.choice(string.digits)

    def _gen_s(self):
        return random.choice('!@#$%&_')

    def __call__(self, c):
        assert c in ['c', 'C', 'n', 's']
        return getattr(self, '_gen_' + c)()


cg = CharGenerator()


chars = [cg(c) for c in templates[mode]]
random.shuffle(chars)
output = ''.join(chars)

try:
    fd = os.open('/tmp/launchbar-latest-random', 
                 os.O_WRONLY | os.O_CREAT, 0o222)
except:
    pass
else:
    with io.open(fd, 'wb') as f:
        f.write(output + os.linesep)

print(''.join(chars))
