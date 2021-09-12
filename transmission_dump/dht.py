#!/usr/bin/env python3

import bencoder
import sys
import argparse
from os.path import expanduser
from binascii import hexlify
from ipaddress import ip_address

# resume-file (b'peers2' or b'peers2-6')
# each entry is 24 bytes (4 enum, 16 addr, 2 port, 1 flags, 1 padding):
#    https://github.com/transmission/transmission/blob/db3d40d0edfab958b48f3413d2fce442420a65c2/libtransmission/peer-mgr.h
#    le32: 0=IPv4, 1=IPv6
#    uint8_t[16]=address
#    le16: port
#    uint8_t=flags
#    uint8_t=padding

def parse_args(args=None):
    p = argparse.ArgumentParser(description='Parse the dht.dat file from the Transmission BitTorrent client (tested with Transmission 2.84 and 2.92)')
    p.add_argument('dht_file', nargs='?', help='Path to dht.dat (default ~/.config/transmission/dht.dat)',
                   default=expanduser('~/.config/transmission/dht.dat'))
    p.add_argument('-s', '--sort', action='store_true', help='Sort DHT nodes in output')
    args = p.parse_args(args)
    return p, args

def main(args=None):
    p, args = parse_args(args)

    with open(args.dht_file, "rb") as f:
        dht_raw = f.read()
    dht = bencoder.decode(dht_raw)

    # Check file sanity
    if b'id' in dht and (b'nodes' in dht or b'nodes6' in dht):
        extra = set(dht.keys()) - {b'id', b'nodes', b'nodes6'}
        if extra:
            print("WARNING: Transmission DHT file contains unexpected keys: {}\n"
                  "    This may be a newer file format than what we understand (tested with Transmission 2.84 and 2.92)"
                  .format(' '.join(map(repr, extra))), file=sys.stderr)
    else:
        print("ERROR: This does not appear to be a Transmission DHT file (tested with Transmission 2.84 and 2.92)"
              "    Keys it contains: {}".format(' '.join(map(repr, dht.keys()))), file=sys.stderr)

    # Print file ID
    if b'id' in dht:
        print("Transmission DHT file ID is: {}".format(hexlify(dht[b'id']).decode()))

    # Print lists of nodes
    for (k, f, pre, post, l) in (
            (b'nodes', 'IPv4', '', '', 6),
            (b'nodes6', 'IPv6', '[', ']', 18)
    ):
        if k in dht:
            raw = dht[k]
            assert len(raw) % l == 0

            print("Transmission DHT file contains {} {} nodes:".format(len(raw) // l, f))
            address_port = (
                (ip_address(raw[ii: ii + l - 2]), (raw[ii + l - 2] << 8) + raw[ii + l - 1])
                for ii in range(0, len(raw), l)
            )
            if args.sort:
                address_port = sorted(address_port)

            for a, p in address_port:
                print("  tcp://{}{}{}:{}".format(pre, a, post, p))

if __name__ == '__main__':
    main()
