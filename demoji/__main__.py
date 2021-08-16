import io
import sys

from . import replace_with_desc


def demojify(fp: io.IOBase):
    for line in fp:
        print(replace_with_desc(line), end='')


if len(sys.argv) > 1:
    files = sys.argv
else:
    files = ['-']

for filename in files:
    if filename == '-':
        fp = sys.stdin
        demojify(fp)
    else:
        with open(filename) as fp:
            demojify(fp)
