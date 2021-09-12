# transmission-dump

Command-line tools to dump the contents of state files used by the
[Transmission BitTorrent client](https://transmissionbt.com)
(specifically its `dht.dat` and `*.resume` files).

Tested with Transmission 2.84 and 2.92.

## Install

Requires Python 3, `pip3`, and [`bencoder`](https://github.com/utdemir/bencoder) (which will be auto-installed by `pip3`):

```sh
$ pip3 install https://github.com/dlenski/transmission-dump/archive/master.zip
```

## Dump Transmission's `dht.dat`

```sh
$ transmission-dump-dht ~/.config/transmission/dht.dat
Transmission DHT file ID is: da39a3ee5e6b4b0d3255bfef95601890afd80709
Transmission DHT file contains 3 IPv4 nodes:
  tcp://1.2.3.4:42260
  tcp://5.6.7.8:6888
  tcp://9.0.1.2:6881
Transmission DHT file contains 2 IPv6 nodes:
  tcp://[2001:dead:beef::1]:6881
  tcp://[2001:f00f:cafe::2]:6882
```

## Dump Transmission's `*.resume`

```sh
$ transmission-dump-dht ~/.config/transmission/resume/torrent.dat
name = b'Blah_blah_blah.bin'
...
Transmission resume file contains 5 IPv4 peers:
  tcp://1.2.3.4:42260
  tcp://5.6.7.8:6888 (ENCRYPTION, UTP)
  tcp://9.0.1.2:6881 (CONNECTABLE, UTP)
Transmission resume file contains 2 IPv6 peers:
  tcp://[2001:dead:beef::1]:6881
  tcp://[2001:f00f:cafe::2]:6882
```

# License

GPL v3 or later
