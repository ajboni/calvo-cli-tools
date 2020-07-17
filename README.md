# jack-audio-tools

A collection of utilities and tools for the [JACK] audio ecosystem.
This repo is a fork of [jack-audio-tools](https://github.com/SpotlightKid/jack-audio-tools) by [SpotlightKid](https://github.com/SpotlightKid) which was immensely helpful for me to initiate with JACK and python.

# JACK 

## client
### `query`
Get several information about JACK instance.

```bash
python3 client.py query
```

```JSON
{
  "status": "running",
  "cpu_load": 2.081221580505371,
  "block_size": 256,
  "realtime": true,
  "sample_rate": 44100
}⏎                         
```

###  `port-info`
Gets the available jack ports.

```bash
python3 py/jack-audio-tools/jack/client.py port-info
```

```JSON
{
  "all": [
    "system:capture_1",
    "system:capture_2",
    "system:playback_1",
    "system:playback_2",
    "system:midi_capture_1",
    "system:midi_playback_1",
    "system:midi_capture_2",
    "system:midi_playback_2",
    "PulseAudio JACK Sink:front-left",
    "PulseAudio JACK Sink:front-right",
    "a2j:Midi Through [14] (capture): Midi Through Port-0",
    "a2j:Midi Through [14] (playback): Midi Through Port-0",
    "a2j:STUDIO 2 [20] (capture): STUDIO 2 MIDI 1",
    "a2j:STUDIO 2 [20] (playback): STUDIO 2 MIDI 1",
    "PulseAudio JACK Source:front-left",
    "PulseAudio JACK Source:front-right",
    "mod-host:midi_in"
  ],
  "audio": {
    "input": [
      "system:playback_1",
      "system:playback_2",
      "PulseAudio JACK Source:front-left",
      "PulseAudio JACK Source:front-right"
    ],
    "output": [
      "system:capture_1",
      "system:capture_2",
      "PulseAudio JACK Sink:front-left",
      "PulseAudio JACK Sink:front-right"
    ]
  },
  "midi": {
    "input": [
      "system:midi_playback_1",
      "system:midi_playback_2",
      "a2j:Midi Through [14] (playback): Midi Through Port-0",
      "a2j:STUDIO 2 [20] (playback): STUDIO 2 MIDI 1",
      "mod-host:midi_in"
    ],
    "output": [
      "system:midi_capture_1",
      "system:midi_capture_2",
      "a2j:Midi Through [14] (capture): Midi Through Port-0",
      "a2j:STUDIO 2 [20] (capture): STUDIO 2 MIDI 1"
    ]
  },
  "terminal": {
    "input": [],
    "output": []
  }
}⏎                                                
```

## List Ports
```
usage: list_ports.py [-h] [-c CLIENT_NAME] [-p PATTERN] [-a] [-m] [-i] [-o] [-ph] [-mo] [-t]

List all JACK ports.

optional arguments:
  -h, --help            show this help message and exit
  -c CLIENT_NAME, --client-name CLIENT_NAME
                        JACK client name (default: jack_client)
  -p PATTERN, --pattern PATTERN
                        A regular expression used to select ports by name. If empty, no selection based on name will be carried out.
  -a, --is-audio        Select audio/MIDI ports. If neither of them is True, both types of ports are selected. (default: False)
  -m, --is-midi         Select audio/MIDI ports. If neither of them is True, both types of ports are selected.
  -i, --is-input        is_input, is_output, is_physical. Select ports by their flags. If none of them are True, no selection based on flags will be carried out.
  -o, --is-output       is_input, is_output, is_physical, is_terminal, can_monitor Select ports by their flags. If none of them are True, no selection based on flags will
                        be carried out.
  -ph, --is-physical    is_input, is_output, is_physical, is_terminal, can_monitor Select ports by their flags. If none of them are True, no selection based on flags will
                        be carried out.
  -mo, --can-monitor    is_input, is_output, is_physical, is_terminal, can_monitor. Select ports by their flags. If none of them are True, no selection based on flags
                        will be carried out.
  -t, --is-terminal     is_input, is_output, is_physical, is_terminal, can_monitor Select ports by their flags. If none of them are True, no selection based on flags will
                        be carried out.
```						

## Connect Ports
```
usage: connect_ports.py [-h] [-c CLIENT_NAME] [-rm] source destination

Connects/Disconnects two JACK ports.

positional arguments:
  source                Source port. It must be an output port. It must be same type (audio/midi) as dst)
  destination           Destination port. It must be an input port. It must be same type (audio/midi) as src

optional arguments:
  -h, --help            show this help message and exit
  -c CLIENT_NAME, --client-name CLIENT_NAME
                        JACK client name (default: jack_client)
  -rm, --disconnect, --remove, --rm
                        Disconnect both ports.
```

## JACK Transport

The scripts in the `jackaudiotools.transport` package query or manipulate the
JACK transport state.

They require the [JACK-Client] package to be installed, which will be installed
automatically, when you install the `jack-audio-tools` distribution via `pip`:

    pip install jack-audio-tools


### `jack-midi-to-transport`

JACK client which allows to control transport state via MIDI.

The client provides a MIDI input and converts received MIDI system real-time
and MIDI machine control (MMC) messages into JACK transport commands.

The following MIDI messages, when received, start the JACK transport:

* `START` (System Real-time)
* `CONTINUE` (System Real-time)
* `PLAY` (MMC)
* `DEFERRED PLAY` (MMC)

These messages stop the transport:

* `STOP` (System Real-time)
* `STOP` (MMC)
* `PAUSE` (MMC)
* `RESET` (MMC)

And these rewind the transport to frame zero:

* `REWIND` (MMC)
* `RESET` (MMC)

MMC messages are ignored, if the device number in the MMC System Exclusive
message does not match the client's device number (set with the -d command
line option).

If the client's device number is set to 127 (the default), it matches all
MMC message device numbers.


### `jack-rtmidi-to-transport`

JACK client which allows to control transport state via MIDI.

A variant of `midi_to_transport`, which uses the [python-rtmidi] package
as a MIDI backend instead of JACK-Cleint, which is slightly more efficient,
because MIDI input processing is happening in a C++ thread instead of a
Python callback.

To use it, specify the `rtmidi` extra dependency when installing the
`jack-audio-tools` distribution via `pip`:

    pip install "jack-audio-tools[rtmidi]"


### `jack-timebase-master`

A simple JACK timebase master, which provides  musical timing related
information (i.e. currents bar, beats per bar, beat denominator, BPM etc.)
to other JACK clients.


### `jack-transporter`

Query or change the JACK transport state.


## LV2

The scripts in the `jackaudiotools.lv2` package help with querying information
from the [LV2] plugins installed on the system.

They require the [lilv] Python bindings to be installed. Unfortunately, these
can not be installed from the Python Package Index. Instead, install a recent
version of the `lilv` library, either from your distribution's package
repository or from source.


### `lv2-grep`

Print URIs of all installed LV2 plugins matching the given regular expression.

Can optionally output the list of matching plugins in JSON format, where each
list item is an object with the plugin name and uri and optionally the list of
categories the plugin belongs to, as properties.


### `lv2-plugin-uris`

Print a list of all URIs associated with an LV2 plugin.


### `lv2-list-plugin-presets`

List all presets of an LV2 plugin with the given URI.


### `lv2-plugin-info`

Generate a JSON document with information about a single or all installed LV2
plugins. This allows plugin meta data to be loaded quickly in other programs.

Depending on the number of plugins installed on your system, this script may
run for several seconds or even minutes and produce an output file of several
megabytes in size.


## Carla

The scripts in the `jackaudiotools.carla` package manipulate or query [Carla]
project files.


### `carxp2lv2presets`

Export plugin settings from a Carla project file (.carxp) as LV2 preset bundles.

This script requires the [rdflib] package to be installed. To install it,
specify the `rdflib` extra dependency when installing the `jack-audio-tools`
distribution via `pip`:

    pip install "jack-audio-tools[rdflib]"


## License

This software is distributed under the MIT License.

See the file [LICENSE](./LICENSE) for more information.


## Author
This software was originally written by *Christopher Arndt*.
Modifications done by *Alexis Boni*


[carla]: https://kx.studio/Applications:Carla
[jack-client]: https://pypi.org/project/JACK-Client
[jack]: https://jackaudio.org/
[lilv]: http://drobilla.net/software/lilv
[lv2]: http://lv2plug.in/
[python-rtmidi]: https://pypi.org/project/python-rtmidi
[rdflib]: https://pypi.org/project/rdflib
