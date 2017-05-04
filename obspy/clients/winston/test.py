def test_waveserver(hours=1):
    from waveserver import read_wave_server
    from obspy import UTCDateTime

    a = UTCDateTime()
    trace = read_wave_server('pubavo1.wr.usgs.gov', 16022, ('OKFG', 'BHZ', 'AV', '--'), UTCDateTime() - hours * 60 * 60,
                             UTCDateTime())
    print(UTCDateTime() - a)

def test_ew(hours=1):
    from obspy.clients.earthworm import Client
    from obspy import UTCDateTime

    a = UTCDateTime()
    client = Client("pubavo1.wr.usgs.gov", 16022, timeout=5)
    st = client.get_waveforms('AV', 'OKFG', '', 'BHZ', UTCDateTime() - hours * 60 * 60, UTCDateTime())
    print(st.traces[0].data.shape)
    print(UTCDateTime() - a)

def test_wws(hours=1):
    from obspy.clients.winston import Client
    from obspy import UTCDateTime

    a = UTCDateTime()
    client = Client("pubavo1.wr.usgs.gov", 16022, timeout=5)
    st = client.get_waveforms('AV', 'OKFG', '', 'BHZ', UTCDateTime() - hours * 60 * 60, UTCDateTime())
    st.plot(type='dayplot')
    print(UTCDateTime() - a)

def test_heli(hours=1):
    from obspy.clients.winston import Client
    from obspy import UTCDateTime

    a = UTCDateTime()
    client = Client("pubavo1.wr.usgs.gov", 16022, timeout=5)
    st = client.get_heli('AV', 'OKFG', '', 'BHZ', UTCDateTime() - hours * 60 * 60, UTCDateTime())
    st.plot(type='dayplot', interval=30)
    print(UTCDateTime() - a)

if __name__ == '__main__':
    #test_ew(1)
    #test_wws(48)
    test_heli(24)
