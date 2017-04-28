def test1(hours=1):
    from waveserver import read_wave_server
    from obspy import UTCDateTime

    a = UTCDateTime()
    trace = read_wave_server('pubavo1.wr.usgs.gov', 16022, ('OKFG', 'BHZ', 'AV', '--'), UTCDateTime() - hours * 60 * 60,
                             UTCDateTime())
    print(UTCDateTime() - a)

def test2(hours=1):
    from obspy.clients.earthworm import Client
    from obspy import UTCDateTime

    a = UTCDateTime()
    client = Client("pubavo1.wr.usgs.gov", 16022, timeout=5)
    st = client.get_waveforms('AV', 'OKFG', '', 'BHZ', UTCDateTime() - hours * 60 * 60, UTCDateTime())
    print(UTCDateTime() - a)

def test3(hours=1):
    from obspy.clients.winston import Client
    from obspy import UTCDateTime

    a = UTCDateTime()
    client = Client("pubavo1.wr.usgs.gov", 16022, timeout=5)
    st = client.get_waveforms('AV', 'OKFG', '', 'BHZ', UTCDateTime() - hours * 60 * 60, UTCDateTime())
    print(UTCDateTime() - a)

if __name__ == '__main__':
    test1(24)
    test2(24)
    test3(24)