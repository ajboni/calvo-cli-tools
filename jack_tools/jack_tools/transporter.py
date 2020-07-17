#!/usr/bin/env python3
#
#  transporter.py
#
# MIT License

# Copyright (c) 2019 Christopher Arndt

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""Query or change the JACK transport state."""

import argparse
import string
import sys
import json
import jack


STATE_LABELS = {
    jack.ROLLING: "rolling",
    jack.STOPPED: "stopped",
    jack.STARTING: "starting",
    jack.NETSTARTING: "waiting for network sync",
}


def main(args=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        '-c', '--client-name',
        metavar='NAME',
        default='transporter',
        help="JACK client name (default: %(default)s)")
    ap.add_argument(
        '-v', '--verbose',
        action='store_true',
        help="Verbose mode (default: %(default)s)")
    ap.add_argument(
        'command',
        nargs='?',
        default='status',
        choices=['query', 'rewind', 'start',
                 'status', 'stop', 'toggle'],
        help="Transport command")

    args = ap.parse_args(args)

    try:
        client = jack.Client(args.client_name)
    except jack.JackError as exc:
        return "Could not create JACK client: {}".format(exc)

    state = client.transport_state
    result = 0

    if args.command == 'status':
        if args.verbose:
            print("JACK transport is {}.".format(STATE_LABELS[state]))
        else:
            print(STATE_LABELS[state])
      #   result = 1 if state == jack.STOPPED else 0
        result = 0
    elif args.command == 'query':
        res = {
            "state": STATE_LABELS[state],
        }
        #   print("State: {}".format(STATE_LABELS[state]))
        info = client.transport_query()[1]
        for field in sorted(info):
            res[field] = info[field]
        json.dump(res, sys.stdout, indent=2)
      #   result = 1 if state == jack.STOPPED else 0
        result = 0
    elif args.command == 'start':
        if state == jack.STOPPED:
            client.transport_start()
    elif args.command == 'stop':
        if state != jack.STOPPED:
            client.transport_stop()
    elif args.command == 'toggle':
        if state == jack.STOPPED:
            client.transport_start()
        else:
            client.transport_stop()
    elif args.command == 'rewind':
        client.transport_frame = 0

    client.close()
    return result


if __name__ == '__main__':
    sys.exit(main() or 0)
