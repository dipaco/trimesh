"""Parsing functions for Binvox files.

https://www.patrickmin.com/binvox/binvox.html
"""

import numpy as np
import collections
Binvox = collections.namedtuple(
    'Binvox', ['rle_data', 'shape', 'translate', 'scale'])


def _encode(v):
    try:
        return v.encode()
    except ValueError:
        return v


def parse_binvox_header(fp):
    """Read the header from a binvox file.

    Spec at https://www.patrickmin.com/binvox/binvox.html

    Args:
        fp: object providing a `readline` method (e.g. an open file)

    Returns:
        (shape, translate, scale) according to binvox spec

    Raises:
        `IOError` if invalid binvox file.
    """

    line = _encode(fp.readline()).strip()
    if not line.startswith(b'#binvox'):
        raise IOError('Not a binvox file')
    shape = tuple(
        int(s) for s in _encode(fp.readline()).strip().split(b' ')[1:])
    translate = tuple(
        float(s) for s in _encode(fp.readline()).strip().split(b' ')[1:])
    scale = float(_encode(fp.readline()).strip().split(b' ')[1])
    fp.readline()
    return shape, translate, scale


def parse_binvox(fp):
    """Read a binvox file.

    Spec at https://www.patrickmin.com/binvox/binvox.html

    Args:
        fp: object providing a `readline` method (e.g. an open file)

    Returns:
        `Binvox` namedtuple ('rle', 'shape', 'translate', 'scale')
        `rle` is the run length encoding of the values.

    Raises:
        `IOError` if invalid binvox file.
    """
    shape, translate, scale = parse_binvox_header(fp)
    rle_data = np.frombuffer(_encode(fp.read()), dtype=np.uint8)
    return Binvox(rle_data, shape, translate, scale)


def write_binvox(fp, rle_data, shape, translate=(0, 0, 0), scale=1):
    if rle_data.dtype != np.uint8:
        raise ValueError(
            "rle_data.dtype must be np.uint8, got %s" % rle_data.dtype)
    fp.write('#binvox 1\n')
    fp.write('dim ' + ' '.join((str(s) for s in shape)) + '\n')
    fp.write('translate ' + ' '.join((str(t) for t in translate)) + '\n')
    fp.write('scale %s\n' % scale)
    fp.write('data\n')
    fp.write(rle_data.tostring())
