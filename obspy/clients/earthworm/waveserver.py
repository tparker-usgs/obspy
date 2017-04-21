# -*- coding: utf-8 -*-
"""
Low-level Earthworm Wave Server tools.

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

from array import array
import socket
import struct
import sys

import numpy as np

from obspy import Stream, Trace, UTCDateTime
from obspy.core import Stats


RETURNFLAG_KEY = {
    'F': 'success',
    'FR': 'requested data right (later) than tank contents',
    'FL': 'requested data left (earlier) than tank contents',
    'FG': 'requested data lie in tank gap',
    'FB': 'syntax error in request',
    'FC': 'data tank corrupt',
    'FN': 'requested tank not found',
    'FU': 'unknown error'
}

DATATYPE_KEY = {
    b't4': '>f4', b't8': '>f8',
    b's4': '>i4', b's2': '>i2',
    b'f4': '<f4', b'f8': '<f8',
    b'i4': '<i4', b'i2': '<i2'
}


def get_numpy_type(tpstr):
    """
    given a TraceBuf2 type string from header,
    return appropriate numpy.dtype object
    """
    dtypestr = DATATYPE_KEY[tpstr]
    tp = np.dtype(native_str(dtypestr))
    return tp


class TraceBuf2(object):
    """
    """
    byteswap = False
    ndata = 0           # number of samples in instance
    inputType = None    # NumPy data type

    def read_tb2(self, tb2):
        """
        Reads single TraceBuf2 packet from beginning of input byte array tb.
        returns number of bytes read or 0 on read fail.
        """
        if len(tb2) < 64:
            return 0   # not enough array to hold header
        head = tb2[:64]
        self.parse_header(head)
        nbytes = 64 + self.ndata * self.inputType.itemsize
        if len(tb2) < nbytes:
            return 0   # not enough array to hold data specified in header
        dat = tb2[64:nbytes]
        self.parse_data(dat)
        return nbytes

    def parse_header(self, head):
        """
        Parse tracebuf header into class variables
        """
        pack_str = b'2i3d7s9s4s3s2s3s2s2s'
        dtype = head[-7:-5]
        if dtype[0:1] in b'ts':
            endian = b'>'
        elif dtype[0:1] in b'if':
            endian = b'<'
        else:
            raise ValueError
        self.inputType = get_numpy_type(dtype)
        (self.pinno, self.ndata, ts, te, self.rate, self.sta, self.net,
         self.chan, self.loc, self.version, tp, self.qual, _pad) = \
            struct.unpack(endian + pack_str, head)
        if not tp.startswith(dtype):
            msg = 'Error parsing header: %s!=%s'
            print(msg % (dtype, tp), file=sys.stderr)
        self.start = UTCDateTime(ts)
        self.end = UTCDateTime(te)
        return

    def parse_data(self, dat):
        """
        Parse tracebuf char array data into self.data
        """

        self.data = np.empty(0)
        self.append_data(dat)

        return

    def append_data(self, dat, head=None):
        """
        Append char array data to self.data
        """

        if head == None:
            head = self

        new_data = np.fromstring(dat, head.inputType)
        ndat = len(new_data)
        if ndat != head.ndata:
            msg = 'data count in header (%d) != data count (%d)'
            print(msg % (head.ndata, ndat), file=sys.stderr)

        self.data = np.concatenate((self.data, new_data))
        self.ndata = len(self.data)
        self.end = head.end

        return

    def parse_list(self, tbs):
        self.data = np.concatenate(tbs)
        #self.data.dtype = self.inputType
        self.ndata = len(self.data)

    def get_obspy_trace(self):
        """
        Return class contents as obspy.Trace object
        """
        stat = Stats()
        stat.network = self.net.split(b'\x00')[0].decode()
        stat.station = self.sta.split(b'\x00')[0].decode()
        location = self.loc.split(b'\x00')[0].decode()
        if location == '--':
            stat.location = ''
        else:
            stat.location = location
        stat.channel = self.chan.split(b'\x00')[0].decode()
        stat.starttime = UTCDateTime(self.start)
        stat.sampling_rate = self.rate
        stat.npts = len(self.data)
        return Trace(data=self.data, header=stat)


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
<<<<<<< HEAD
        sent = s.send(full_req[totalsent:])
=======
        sent = s.send(full_req[totalsend:])
>>>>>>> 1a7a872f68db9677aa5ed5b315dcbd958751ee8e
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
            # see https://github.com/obspy/obspy/issues/383
            # indat = sock.recv(8192)
            indat = sock.recv(1)
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
    Return list of tanks on server
    """
    rid = 'get_menu'
    if scnl:
        # only works on regular waveservers (not winston)
        getstr = 'MENUSCNL: %s %s %s %s %s\n' % (
            rid, scnl[0], scnl[1], scnl[2], scnl[3])
    else:
        # added SCNL not documented but required
        getstr = 'MENU: %s SCNL\n' % rid
    sock = send_sock_req(server, port, getstr.encode('ascii', 'strict'),
                         timeout=timeout)
    r = get_sock_char_line(sock, timeout=timeout)
    sock.close()
    if r:
        # XXX: we got here from bytes to utf-8 to keep the remaining code
        # intact
        tokens = str(r.decode()).split()
        if tokens[0] == rid:
            tokens = tokens[1:]
        flag = tokens[-1]
        if flag in ['FN', 'FC', 'FU']:
            msg = 'request returned %s - %s'
            print(msg % (flag, RETURNFLAG_KEY[flag]), file=sys.stderr)
            return []
        if tokens[7].encode() in DATATYPE_KEY:
            elen = 8  # length of return entry if location included
        elif tokens[6].encode() in DATATYPE_KEY:
            elen = 7  # length of return entry if location omitted
        else:
            print('no type token found in get_menu', file=sys.stderr)
            return []
        outlist = []
        for p in range(0, len(tokens), elen):
            l = tokens[p:p + elen]
            if elen == 8:
                outlist.append((int(l[0]), l[1], l[2], l[3], l[4],
                                float(l[5]), float(l[6]), l[7]))
            else:
                outlist.append((int(l[0]), l[1], l[2], l[3], '--',
                                float(l[4]), float(l[5]), l[6]))
        return outlist
    return []

def read_wave_server_v(server, port, scnl, start, end, timeout=None, unify=False):
    """
    Reads data for specified time interval and scnl on specified waveserverV.

    Returns list of TraceBuf2 objects
    """
    a = UTCDateTime()

    rid = 'rwserv'
    scnlstr = '%s %s %s %s' % scnl
    reqstr = 'GETSCNLRAW: %s %s %f %f\n' % (rid, scnlstr, start, end)
    sock = send_sock_req(server, port, reqstr.encode('ascii', 'strict'),
                         timeout=timeout)
    r = get_sock_char_line(sock, timeout=timeout)
    if not r:
        return []
    tokens = str(r.decode()).split()
    flag = tokens[6]
    if flag != 'F':
        msg = 'read_wave_server_v returned flag %s - %s'
        print(msg % (flag, RETURNFLAG_KEY[flag]), file=sys.stderr)
        return []
    nbytes = int(tokens[-1])
    b = UTCDateTime()
    print(":1: " + str(b-a))
    dat = get_sock_bytes(sock, nbytes, timeout=timeout)
    sock.close()
    a = UTCDateTime()
    print(":2: " + str(a-b))

    tbl = []
    bytesread = 1
    p = 0
    current_tb = None

    while bytesread and p < len(dat):
        if not len(dat) > p + 64:
            break # no tracebufs left

        new = TraceBuf2()
        new.parse_header(dat[p:p + 64])
        p += 64
        nbytes = new.ndata * new.inputType.itemsize

        if len(dat) < p + nbytes:
            break   # not enough array to hold data specified in header

        if current_tb is None:
            # new.parse_data(tbd)
            current_tb = new
            period = 1 / current_tb.rate
            bufs = [np.fromstring(dat[p:p + nbytes], current_tb.inputType)]


        elif new.start - current_tb.end == period:
            bufs.append(np.fromstring(dat[p:p + nbytes], current_tb.inputType))
            current_tb.end = new.end

        else:
            current_tb.parse_list(bufs)
            tbl.append(current_tb)
            current_tb = new
            period = 1 / current_tb.rate
            bufs = [np.fromstring(dat[p:p + nbytes], current_tb.inputType)]

        p += nbytes

    current_tb.parse_list(bufs)
    tbl.append(current_tb)

    b = UTCDateTime()
    print(":3: " + str(b-a))
    return tbl


def trace_bufs2obspy_stream(tbuflist):
    """
    Returns obspy.Stream object from input list of TraceBuf2 objects
    """
    if not tbuflist:
        return None
    tlist = []
    for tb in tbuflist:
        tlist.append(tb.get_obspy_trace())
    strm = Stream(tlist)
    return strm

def test():
    tbl = read_wave_server_v('pubavo1.wr.usgs.gov', 16022, ('AKS', 'EHZ', 'AV', '--'), UTCDateTime() - 2000, UTCDateTime())
    end = UTCDateTime()
    print(len(tbl))
    period = 1/tbl[0].rate
    line = ""
    for tb in tbl:
        start = tb.start
        offset = start - end
        if offset != period:
            print(line + str(end))
            line = str(start) + " - "

        end = tb.end

    print(line + str(end))
    print("test")

if __name__ == '__main__':
    from obspy.clients.earthworm import Client
    client = Client("pubavo1.wr.usgs.gov", 16022)
    end = UTCDateTime()# now - 2000 seconds
    start = end - 60 * 10  # now - 2000 seconds


    a = UTCDateTime()
    # st = client.get_waveforms('AV', 'ACH', '', 'EHE', end - 60 * 10, end)
    # print(len(st))
    b = UTCDateTime()
    print(b-a)
    st = client.get_waveforms('AV', 'ACH', '', 'EHE', end - 60 * 60 * 4, end)
    #st = client.get_waveforms('AV', 'KAHG', '', 'EHZ', end - 5, end)
    print(len(st))
    a = UTCDateTime()
    print (a-b)
    st.plot()  # doctest: +SKIP
    #st = client.get_waveforms('AV', 'ACH', '', 'EH*', dt, dt + 10)
    #st.plot()  # doctest: +SKIP
