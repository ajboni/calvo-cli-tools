#!/usr/bin/python3
"""List all JACK ports."""

import argparse
import sys
import json
import jack


def list_jack_ports(pattern='', is_audio=False, is_midi=False, is_input=False, is_output=False, is_physical=False, can_monitor=False, is_terminal=False):
    """list of Port/MidiPort/OwnPort/OwnMidiPort
    All ports that satisfy the given conditions."""
    try:
        client = jack.Client(args.client_name)
    except jack.JackError as exc:
        return "Could not create JACK client: {}".format(exc)

    try:
        ports = client.get_ports(
            pattern, is_audio, is_midi, is_input, is_output, is_physical, can_monitor, is_terminal)

        port_names = []
        for port in ports:
            port_names.append(port.name)
        json.dump(port_names, sys.stdout, indent=2)
    except jack.JackError as exc:
        return "Error trying to get port: {}".format(exc)


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        '-c', '--client-name',
        default='jack_client',
        help="JACK client name (default: %(default)s)")

    ap.add_argument(
        '-p', '--pattern',
        default='',
        help="A regular expression used to select ports by name.  If empty, no selection based on name will be carried out."
    )
    ap.add_argument(
        '-a', '--is-audio',
        default=False,
        action='store_true',
        help="Select audio/MIDI ports.  If neither of them is True, both types of ports are selected.  (default: %(default)s)"
    )
    ap.add_argument(
        '-m', '--is-midi',
        default=False,
        action='store_true',
        help="Select audio/MIDI ports.  If neither of them is True, both types of ports are selected."
    )
    ap.add_argument(
        '-i', '--is-input',
        default=False,
        action='store_true',
        help="is_input, is_output, is_physical. Select ports by their flags.  If none of them are True, no selection based on flags will be carried out."
    )
    ap.add_argument(
        '-o', '--is-output',
        default=False,
        action='store_true',
        help="is_input, is_output, is_physical, is_terminal, can_monitor Select ports by their flags.  If none of them are True, no selection based on flags will be carried out."
    )
    ap.add_argument(
        '-ph', '--is-physical',
        default=False,
        action='store_true',
        help="is_input, is_output, is_physical, is_terminal, can_monitor Select ports by their flags.  If none of them are True, no selection based on flags will be carried out."
    )
    ap.add_argument(
        '-mo', '--can-monitor',
        default=False,
        action='store_true',
        help="is_input, is_output, is_physical, is_terminal, can_monitor. Select ports by their flags.  If none of them are True, no selection based on flags will be carried out."
    )
    ap.add_argument(
        '-t', '--is-terminal',
        default=False,
        action='store_true',
        help="is_input, is_output, is_physical, is_terminal, can_monitor Select ports by their flags.  If none of them are True, no selection based on flags will be carried out."
    )

    args = ap.parse_args()
    sys.exit(list_jack_ports(pattern=args.pattern,
                             is_audio=args.is_audio, is_midi=args.is_midi, is_input=args.is_input, is_output=args.is_output, is_physical=args.is_physical, can_monitor=args.can_monitor, is_terminal=args.is_terminal) or 0)
