#!/usr/bin/env python3

import bencoder
import sys
import argparse
import pprint
from datetime import datetime, timezone
from enum import IntEnum
from struct import unpack_from
from binascii import hexlify
from ipaddress import ip_address

def parse_args(args=None):
    p = argparse.ArgumentParser(description='Parse a resume file from the Transmission BitTorrent client (tested with Transmission 2.92)')
    p.add_argument('resume_file', help='Path to the resume file (normally these live in ~/.config/transmission/resume)')
    p.add_argument('-s', '--sort', action='store_true', help='Sort peer nodes in output')
    args = p.parse_args()
    return p, args

def main(args=None):
    p, args = parse_args(args)

    with open(args.resume_file, "rb") as f:
        resume_raw = f.read()
    resume = bencoder.decode(resume_raw)

    # https://github.com/transmission/transmission/blob/db3d40d0edfab958b48f3413d2fce442420a65c2/libtransmission/peer-mgr.h#L36-L50
    class PeerFlags(IntEnum):
        ENCRYPTION = 1
        SEED = 2
        UTP = 4
        HOLEPUNCH = 8
        CONNECTABLE = 16
        @classmethod
        def from_int(cls, ii):
            return set(val for val in cls if (ii & val.value))


    keys = sorted(resume, key=lambda k: (
        (0 if k == b'name' else 2 if k.startswith(b'peers2') else 1), k
    ))
    for k in keys:
        if k in (b'peers2', b'peers2-6'):
            raw = resume[k]
            assert len(raw) % 24 == 0

            # https://github.com/transmission/transmission/blob/db3d40d0edfab958b48f3413d2fce442420a65c2/libtransmission/peer-mgr.h
            address_port_flags = (
                (ip_address(_a if _af==1 else _a[:4]), port, PeerFlags.from_int(flags))
                for _af, _a, port, flags in (
                    unpack_from('<l 16s H B x', raw, ii)
                    for ii in range(0, len(raw), 24)
                )
            )

            print("Transmission resume file contains {} {} peers:".format(
                len(raw) // 24, ("IPv6" if k == b'peers2-6' else "IPv4")))
            if args.sort:
                address_port_flags = sorted(address_port_flags)
            for a, p, f in address_port_flags:
                flags = ', '.join(ff.name for ff in f)
                if flags:
                    flags = ' ({})'.format(flags)
                pre, post = ('[]') if a.version == 6 else ('', '')
                print("  tcp://{}{}{}:{}{}".format(pre, a, post, p, flags))

        elif k in (b'progress', b'priority', b'dnd'):
            v = resume[k][b'blocks'] if k == b'progress' else resume[k]
            print("{} = present (len {})".format(k.decode(), len(v)))

        elif k.endswith(b'-date'):
            print('{} = {}'.format(k.decode(), datetime.fromtimestamp(resume[k], timezone.utc).isoformat()))

        else:
            print('{} = {}'.format(k.decode(), pprint.pformat(resume[k])))
