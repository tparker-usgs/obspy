# -*- coding: utf-8 -*-
"""
obspy.clients.winston - Winston Wave Server module for ObsPy.

===============================================
The obspy.clients.winston package contains a client for the Winston wave server. Adapted from :class:`~obspy.client.earthworm`


:copyright:
    The ObsPy Development Team (devs@obspy.org)
:license:
    GNU Lesser General Public License, Version 3
    (https://www.gnu.org/copyleft/lesser.html)
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from future.builtins import *  # NOQA

from .client import Client  # NOQA


if __name__ == '__main__':
    import doctest
    doctest.testmod(exclude_empty=True)
