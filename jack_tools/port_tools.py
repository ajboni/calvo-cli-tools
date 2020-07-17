
#!/usr/bin/env python3
"""Assorted tools for handling a JACK port"""

import jack
import json
import argparse
from .connect_ports import connect_ports


def clear_port(args):
    """ Removes all incoming/outgoing connections from/to a port

    Arguments:
        port: (string) -- Port name clear.

    Raises:
        ConnectionError: "If JACK client could not connect."
        ValueError: "If no port is found, or the connection was unsuccesfull"
    """

    try:
        client = jack.Client(args.client_name)
    except jack.JackError as exc:
        raise ConnectionError("Could not create JACK client: {}".format(exc))

    try:
        port = client.get_port_by_name(args.port)
        ports = client.get_all_connections(port)

        for cport in ports:
            connect_ports(
                port.name, cport.name, args.client_name, True)

    except jack.JackError as exc:
        raise ValueError("Could not create JACK client: {}".format(exc))


def _connect_ports(args):
    connect_ports(
        args.source, args.destination, args.client_name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    subparses = parser.add_subparsers()

    parser.add_argument(
        '-c', '--client-name',
        default='jack_client',
        help="JACK client name (default: %(default)s)")

    # Clear port
    parser_clear_port = subparses.add_parser(
        'clear', help='Remove all connections from a port')
    parser_clear_port.add_argument('port', help='Port to clear.')
    parser_clear_port.set_defaults(func=clear_port)

    # Connect ports
    parser_connect = subparses.add_parser(
        'connect', help='Connect to another port')

    parser_connect.add_argument('source', help='Source port.')
    parser_connect.add_argument('destination', help='Destination port.')
    parser_connect.set_defaults(func=_connect_ports)

    arguments = parser.parse_args()
    arguments.func(arguments)

# connect.set_defaults(func=connect_ports.connect_ports(
#     args.source, args.destination, "a", False))
