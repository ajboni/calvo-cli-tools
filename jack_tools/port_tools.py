#!/usr/bin/python3
"""Assorted tools for handling a JACK port"""

import jack
import sys
import argparse


def clear_port(port, client_name="jack_client", **kwarg):
    """ Removes all incoming/outgoing connections from/to a port

    Arguments:
        port: (string) -- Port name to clear.

    Raises:
        ConnectionError: "If JACK client could not connect."
        ValueError: "If no port is found, or the connection was unsuccesfull"
    """

    try:
        client = jack.Client(client_name)
    except jack.JackError as exc:
        raise ConnectionError("Could not create JACK client: {}".format(exc))

    src_ports_names = port.split(',')

    for src_port_name in src_ports_names:
        try:
            jack_port = client.get_port_by_name(src_port_name)
            jack_ports = client.get_all_connections(jack_port)

            for cport in jack_ports:
                if jack_port.is_output:
                    connect_ports(
                        src_port_name, cport.name, client_name, True)
                elif jack_port.is_input:
                    connect_ports(
                        cport.name, src_port_name, client_name, True)

        except jack.JackError as exc:
            raise ValueError("Could not clear port: {}".format(exc))


def connect_ports(source, destination, client_name, disconnect=False, quiet=False, **kwarg):
    """ Connects/Disconnects two JACK ports.

    Parameters
    ----------
    src: [string]
        Source port name.
    dst: [string]
        Destination port name.
    client_name: [string]
        JACK Client name.
    disconnect: bool, optional
        Perform a disconnection instead, by default False
    quiet: bool, optional
        Do not raise exception is the connection cannot be made due to (non)exisiting connections between the ports, by default False.

    Raises
    ------
    ConnectionError
        Could not create JACK client:
    ValueError
        Port names not found.
    TypeError
        Port types are not compatible.
    """

    try:
        client = jack.Client(client_name)
    except jack.JackError as exc:
        raise ConnectionError("Could not create JACK client: {}".format(exc))

    try:
        src_port = client.get_port_by_name(source)
        dst_port = client.get_port_by_name(destination)
        src_connections = client.get_all_connections(src_port)

    except jack.JackError as exc:
        raise ValueError("Could not get JACK port: {}".format(exc))

    # Check for src=output
    if not dst_port.is_input:
        raise TypeError(
            f'Error connecting ports: {destination} is not an INPUT port!')

    # Check for dst=input
    if not src_port.is_output:
        raise TypeError(
            f'Error connecting ports: {source} is not an OUTPUT port!')

    # Check both port to be audio
    if src_port.is_audio and not dst_port.is_audio or dst_port.is_audio and not dst_port.is_audio:
        raise TypeError(
            'Error connecting ports: Both ports are expected to be the same type.')

    # Check both midi ports
    if src_port.is_midi and not dst_port.is_midi or dst_port.is_midi and not dst_port.is_midi:
        raise TypeError(
            'Error connecting ports: Both ports are expected to be the same type.')

    if not disconnect:
        try:
            client.connect(src_port, dst_port)
        except jack.JackError as exc:
            raise ValueError(
                f'Could not make the connection between {source} => {destination} : {exc}')
    else:
        existingConnection = False
        for port in src_connections:
            if port == dst_port:
                existingConnection = True
                break
        if existingConnection:
            client.disconnect(src_port, dst_port)
        else:
            if not quiet:
                raise ValueError(
                    f'Could not make the connection between {source} => {destination} : {exc}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    subparses = parser.add_subparsers()

    parser.add_argument(
        '-c', '--client-name',
        default='jack_client',
        help="JACK client name (default: %(default)s)")

    # Clear port
    parser_clear_port = subparses.add_parser(
        'clear', help='Remove all connections from a port or a comma separated lists of ports')
    parser_clear_port.add_argument(
        'port', help='Port or comma separated list of ports to clear.')
    parser_clear_port.set_defaults(func=clear_port)

    # Connect ports
    parser_connect = subparses.add_parser(
        'connect', help='Connect to another port')

    parser_connect.add_argument(
        'source',
        help="Source port. It must be an output port. It must be same type (audio/midi) as dst)")
    parser_connect.add_argument(
        'destination',
        help="Destination port. It must be an input port. It must be same type (audio/midi) as src")
    parser_connect.add_argument(
        '-rm', '--disconnect', '--remove', '--rm',
        action='store_true',
        default=False,
        help="Disconnect both ports.")
    parser_connect.add_argument(
        '-q', '--quiet',
        action='store_true',
        default=False,
        help="Do not raise exception is the connection cannot be made due to (non)exisiting connections between the ports")

    parser_connect.set_defaults(func=connect_ports)

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    arguments = parser.parse_args()
    arguments.func(**vars(arguments))
