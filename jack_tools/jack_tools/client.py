#!/usr/bin/env python3
#
#  client.py
#
"""Query JACK status from a client perspective."""

import argparse
import string
import sys
import json
import jack


def main(args=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        '-c', '--client-name',
        metavar='NAME',
        default='jack_client',
        help="JACK client name (default: %(default)s)")
    ap.add_argument(
        'command',
        nargs='?',
        default='query',
        choices=['query', 'port-info'],
        help="Transport command")

    args = ap.parse_args(args)

    try:
        client = jack.Client(args.client_name)
    except jack.JackError as exc:
        return "Could not create JACK client: {}".format(exc)

    result = 0
    if args.command == 'check':
        # If we get this far we are connected to jack.
        print("running")
        result = 0
    if args.command == 'query':
        res = {
            "status": "running",
            "cpu_load": client.cpu_load(),
            "block_size": client.blocksize,
            "realtime": client.realtime,
            "sample_rate": client.samplerate,
        }
        json.dump(res, sys.stdout, indent=2)
        result = 0
    if args.command == 'port-info':
        all_ports = client.get_ports('')
        res = {
            'all': [],
            'audio': {
                'playback': [],
                'capture': [],
            },
            'midi': {
                'playback': [],
                'capture': [],
            },
            # 'terminal': {
            #     'playback': [],
            #     'capture': [],
            # }
        }
        for port in all_ports:
            res['all'].append(port.name)
            p_direction = "playback" if port.is_input else 'capture'

            p_type = ""
            if port.is_audio:
                p_type = "audio"
            elif port.is_midi:
                p_type = "midi"
            # elif port.is_terminal:
            #     p_type = "terminal"
            res[p_type][p_direction].append(port.name)
            # print(port.name)

        json.dump(res, sys.stdout, indent=2)
    client.close()
    return result


if __name__ == '__main__':
    sys.exit(main() or 0)
