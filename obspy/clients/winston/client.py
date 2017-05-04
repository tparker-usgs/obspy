# -*- coding: utf-8 -*-
"""
Winston wave server client for ObsPy.

:copyright:
    The ObsPy Development Team (devs@obspy.org)
:license:
    GNU Lesser General Public License, Version 3
    (https://www.gnu.org/copyleft/lesser.html)

.. seealso:: http://volcanoes.usgs.gov/software/winston
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from obspy import Stream, UTCDateTime
from .waveserver import get_wave, get_heli


class Client(object):
    """
    Winston wave server client for waveform data

    :type host: str
    :param host: The IP address or DNS name of the server
    :type port: int, optional
    :param port: The port of the wave server (default is ``16022``)
    :type timeout: int, optional
    :param timeout: Wait this much time before timeout is raised
        (default is ``30``)

    .. rubric:: Example

    >>> from obspy.clients.winston import Client
    >>> client = Client("puavo1.wr.usgs.gov")
    >>> now = UTCDateTime()
    >>> st = client.get_waveforms("net", "sta", "loc", "ch?", now - 60 * 60, now)
    >>> print(st)  # doctest: +ELLIPSIS
    """

    def __init__(self, host, port=16022, timeout=30):
        """
        Initializes access to a Winston wave server
        """
        self.host = host
        self.port = port
        self.timeout = timeout

    def get_waveforms(self, network, station, location, channel, starttime,
                      endtime):
        """
        Retrieves waveform data from a Winston wave server and returns an ObsPy
        Stream object.

        :type filename: str
        :param filename: Name of the output file.
        :type network: str
        :param network: Network code, e.g. ``'UW'``.
        :type station: str
        :param station: Station code, e.g. ``'TUCA'``.
        :type location: str
        :param location: Location code, e.g. ``'--'``.
        :type channel: str
        :param channel: Channel code, e.g. ``'BHZ'``. Last character (i.e.
            component) can be a wildcard ('?' or '*') to fetch `Z`, `N` and
            `E` component.
        :type starttime: :class:`~obspy.core.utcdatetime.UTCDateTime`
        :param starttime: Start date and time.
        :type endtime: :class:`~obspy.core.utcdatetime.UTCDateTime`
        :param endtime: End date and time.
        :return: ObsPy :class:`~obspy.core.stream.Stream` object.
        :type cleanup: bool
        :param cleanup: Specifies whether perfectly aligned traces should be
            merged or not. See :meth:`obspy.core.stream.Stream.merge` for
            ``method=-1``.

        .. rubric:: Example

        >>> from obspy.clients.winston import Client
        >>> client = Client("pubavo1.wr.usgs.gov", 16022)
        >>> now = UTCDateTime()
        >>> st = client.get_waveforms('AV', 'ACH', '', 'EHE', now - 60 * 60, now)
        >>> st.plot()  # doctest: +SKIP
        >>> st = client.get_waveforms('AV', 'ACH', '', 'EH*', now - 60 * 60, now)
        >>> st.plot()  # doctest: +SKIP

        """

        if location == '':
            location = '--'

        stream = Stream()
        if channel[-1] in "?*":
            for comp in ("Z", "N", "E"):
                channel_new = channel[:-1] + comp
                scnl = (station, channel_new, network, location)
                trace = get_wave(self.host, self.port, scnl, starttime,
                                 endtime, timeout=self.timeout)
                stream.append(trace)

        else:
            scnl = (station, channel, network, location)
            trace = get_wave(self.host, self.port, scnl, starttime,
                             endtime, timeout=self.timeout)
            stream.append(trace)

        return stream

    def get_heli(self, network, station, location, channel, starttime,
                      endtime):
        """
        Retrieves waveform data from a Winston wave server and returns an ObsPy
        Stream object.

        :type filename: str
        :param filename: Name of the output file.
        :type network: str
        :param network: Network code, e.g. ``'UW'``.
        :type station: str
        :param station: Station code, e.g. ``'TUCA'``.
        :type location: str
        :param location: Location code, e.g. ``'--'``.
        :type channel: str
        :param channel: Channel code, e.g. ``'BHZ'``. Last character (i.e.
            component) can be a wildcard ('?' or '*') to fetch `Z`, `N` and
            `E` component.
        :type starttime: :class:`~obspy.core.utcdatetime.UTCDateTime`
        :param starttime: Start date and time.
        :type endtime: :class:`~obspy.core.utcdatetime.UTCDateTime`
        :param endtime: End date and time.
        :return: ObsPy :class:`~obspy.core.stream.Stream` object.
        :type cleanup: bool
        :param cleanup: Specifies whether perfectly aligned traces should be
            merged or not. See :meth:`obspy.core.stream.Stream.merge` for
            ``method=-1``.

        .. rubric:: Example

        >>> from obspy.clients.winston import Client
        >>> client = Client("pubavo1.wr.usgs.gov", 16022)
        >>> now = UTCDateTime()
        >>> st = client.get_heli('AV', 'ACH', '', 'EHE', now - 60 * 60, now)
        >>> st.plot()  # doctest: +SKIP
        >>> st = client.get_heli('AV', 'ACH', '', 'EH*', now - 60 * 60, now)
        >>> st.plot()  # doctest: +SKIP

        """

        if location == '':
            location = '--'

        stream = Stream()
        if channel[-1] in "?*":
            for comp in ("Z", "N", "E"):
                channel_new = channel[:-1] + comp
                scnl = (station, channel_new, network, location)
                trace = get_heli(self.host, self.port, scnl, starttime,
                                 endtime, timeout=self.timeout)
                stream.append(trace)

        else:
            scnl = (station, channel, network, location)
            trace = get_heli(self.host, self.port, scnl, starttime,
                             endtime, timeout=self.timeout)
            stream.append(trace)

        return stream

    def get_rsam(self, network, station, location, channel, starttime,
                      endtime):
        """
        Retrieves waveform data from a Winston wave server and returns an ObsPy
        Stream object.

        :type filename: str
        :param filename: Name of the output file.
        :type network: str
        :param network: Network code, e.g. ``'UW'``.
        :type station: str
        :param station: Station code, e.g. ``'TUCA'``.
        :type location: str
        :param location: Location code, e.g. ``'--'``.
        :type channel: str
        :param channel: Channel code, e.g. ``'BHZ'``. Last character (i.e.
            component) can be a wildcard ('?' or '*') to fetch `Z`, `N` and
            `E` component.
        :type starttime: :class:`~obspy.core.utcdatetime.UTCDateTime`
        :param starttime: Start date and time.
        :type endtime: :class:`~obspy.core.utcdatetime.UTCDateTime`
        :param endtime: End date and time.
        :return: ObsPy :class:`~obspy.core.stream.Stream` object.
        :type cleanup: bool
        :param cleanup: Specifies whether perfectly aligned traces should be
            merged or not. See :meth:`obspy.core.stream.Stream.merge` for
            ``method=-1``.

        .. rubric:: Example

        >>> from obspy.clients.winston import Client
        >>> client = Client("pubavo1.wr.usgs.gov", 16022)
        >>> now = UTCDateTime()
        >>> st = client.get_rsam('AV', 'ACH', '', 'EHE', now - 60 * 60, now)
        >>> st.plot()  # doctest: +SKIP
        >>> st = client.get_rsam('AV', 'ACH', '', 'EH*', now - 60 * 60, now)
        >>> st.plot()  # doctest: +SKIP

        """

        if location == '':
            location = '--'

        stream = Stream()
        if channel[-1] in "?*":
            for comp in ("Z", "N", "E"):
                channel_new = channel[:-1] + comp
                scnl = (station, channel_new, network, location)
                trace = get_rsam(self.host, self.port, scnl, starttime,
                                 endtime, timeout=self.timeout)
                stream.append(trace)

        else:
            scnl = (station, channel, network, location)
            trace = get_rsam(self.host, self.port, scnl, starttime,
                             endtime, timeout=self.timeout)
            stream.append(trace)

        return stream

    def save_waveforms(self, filename, network, station, location, channel,
                       starttime, endtime, format="MSEED"):
        """
        Writes a retrieved waveform directly into a file.

        :type filename: str
        :param filename: Name of the output file.
        :type network: str
        :param network: Network code, e.g. ``'UW'``.
        :type station: str
        :param station: Station code, e.g. ``'TUCA'``.
        :type location: str
        :param location: Location code, e.g. ``''``.
        :type channel: str
        :param channel: Channel code, e.g. ``'BHZ'``. Last character (i.e.
            component) can be a wildcard ('?' or '*') to fetch `Z`, `N` and
            `E` component.
        :type starttime: :class:`~obspy.core.utcdatetime.UTCDateTime`
        :param starttime: Start date and time.
        :type endtime: :class:`~obspy.core.utcdatetime.UTCDateTime`
        :param endtime: End date and time.
        :type format: str, optional
        :param format: Output format. One of ``"MSEED"``, ``"GSE2"``,
            ``"SAC"``, ``"SACXY"``, ``"Q"``, ``"SH_ASC"``, ``"SEGY"``,
            ``"SU"``, ``"WAV"``. See the Supported Formats section in method
            :meth:`~obspy.core.stream.Stream.write` for a full list of
            supported formats. Defaults to ``'MSEED'``.
        :type cleanup: bool
        :param cleanup: Specifies whether perfectly aligned traces should be
            merged or not. See :meth:`~obspy.core.stream.Stream.merge`,
            `method` -1 or :meth:`~obspy.core.stream.Stream._cleanup`.
        :return: None

        .. rubric:: Example

        >>> from obspy.clients.winston import Client
        >>> client = Client("pubavo1.wr.usgs.gov", 16022)
        >>> t = UTCDateTime() - 2000  # now - 2000 seconds
        >>> client.save_waveforms('AV.ACH.--.EHE.mseed',
        ...                       'AV', 'ACH', '', 'EHE',
        ...                       t, t + 10, format='MSEED')  # doctest: +SKIP
        """
        st = self.get_waveforms(network, station, location, channel, starttime,
                                endtime)
        st.write(filename, format=format)


if __name__ == '__main__':
    import doctest

    doctest.testmod(exclude_empty=True)
