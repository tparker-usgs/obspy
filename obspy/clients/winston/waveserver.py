# -*- coding: utf-8 -*-
"""
Winston Wave Server tools.

:copyright:
    The ObsPy Development Team (devs@obspy.org) & Victor Kress
:license:
    GNU Lesser General Public License, Version 3
    (https://www.gnu.org/copyleft/lesser.html)
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from future.builtins import *  # NOQA @UnusedWildImport
from future.utils import native_str

import socket
import struct
import zlib

import numpy as np

from obspy import Trace, UTCDateTime
from obspy.core import Stats

J2K_EPOCH = UTCDateTime(2000, 1, 1, 12)
J2K_OFFSET = 946728000
NO_DATA = -2147483648
HEADER_LEN = 28


def get_numpy_type(tpstr):
    """
    given a TraceBuf2 type string from header,
    return appropriate numpy.dtype object
    """

    if tpstr == 's4':
        dtypestr = '>i4'
    else:
        dtypestr = '<i4'
    tp = np.dtype(native_str(dtypestr))
    return tp


def send_sock_req(server, port, req_str, timeout=None):
    """
    Sets up socket to server and port, sends req_str
    to socket and returns open socket
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    s.connect((server, port))

    full_req = req_str
    if not full_req.endswith(b'\n'):
        full_req += b'\n'

    req_len = len(full_req)
    totalsent = 0

    while totalsent < req_len:
        sent = s.send(full_req[totalsent:])
        if sent == 0:
            raise RuntimeError("socket connection broken")
        totalsent = totalsent + sent
    return s


def get_sock_char_line(sock, timeout=10.):
    """
    Retrieves one newline terminated string from input open socket
    """
    sock.settimeout(timeout)
    chunks = []
    indat = b'^'
    try:
        while indat[-1:] != b'\n':
            indat = sock.recv(4096)
            if not indat:
                break
            chunks.append(indat)
    except socket.timeout:
        print('socket timeout in get_sock_char_line()', file=sys.stderr)
        return None
    if chunks:
        response = b''.join(chunks)
        return response
    else:
        return None


def get_sock_bytes(sock, nbytes, timeout=None):
    """
    Listens for nbytes from open socket.
    Returns byte array as python string or None if timeout
    """
    sock.settimeout(timeout)
    chunks = []
    btoread = nbytes
    try:
        while btoread:
            indat = sock.recv(min(btoread, 8192))
            if not indat:
                break
            btoread -= len(indat)
            chunks.append(indat)
    except socket.timeout:
        print('socket timeout in get_sock_bytes()', file=sys.stderr)
        return None
    if chunks:
        response = b''.join(chunks)
        return response
    else:
        return None


def get_menu(server, port, scnl=None, timeout=None):
    """
    Return list of channels on server
    """
    pass

def to_j2ksec(intime):
    """
    Convert a UTCDateTime into an integer J2kSec
    """
    return intime - J2K_EPOCH


def get_wave(server, port, scnl, start, end, timeout=None, cleanup=False):
    """
    Reads data for specified time interval and scnl on specified waveserverV.

    Returns an ObsPy :class:`~obspy.core.stream.Trace` object, containing integer samples in a masked array.
    """
    scnlstr = '%s %s %s %s' % scnl
    reqstr = 'GETWAVERAW: %s %s %f %f 1\n' % ('GS', scnlstr, to_j2ksec(start), to_j2ksec(end))
    sock = send_sock_req(server, port, reqstr.encode('ascii', 'strict'),
                         timeout=timeout)
    r = get_sock_char_line(sock, timeout=timeout)
    if not r:
        return []
    tokens = str(r.decode()).split()
    nbytes = int(tokens[-1])
    dat = zlib.decompress(get_sock_bytes(sock, nbytes, timeout=timeout))
    sock.close()

    (start, rate, offset, npts) = struct.unpack(">dddi", dat[0:HEADER_LEN])

    stat = Stats()
    stat.network = scnl[2]
    stat.station = scnl[0]
    if scnl == '--':
        stat.location = ''
    else:
        stat.location = scnl[3]

    stat.channel = scnl[1]
    stat.starttime = UTCDateTime(start + J2K_OFFSET)

    stat.sampling_rate = rate
    stat.npts = npts

    print(stat)

    if len(dat) > npts * 4 + HEADER_LEN:
        dtype = get_numpy_type(dat[HEADER_LEN+4*npts:].decode("utf-16-be"))
    else:
        dtype = get_numpy_type("s4")

    data = np.fromstring(dat[HEADER_LEN:HEADER_LEN+4*npts], dtype)
    data = np.ma.masked_equal(data, NO_DATA)
    trace = Trace(data=data, header=stat)
    return trace


if __name__ == '__main__':

    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))