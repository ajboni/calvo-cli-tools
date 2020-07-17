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

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""List all presets of an LV2 plugin with the given URI."""

import sys
import lilv


NS_PRESETS = 'http://lv2plug.in/ns/ext/presets#'


def get_presets(world, plugin):
    ns_presets = lilv.Namespace(world, NS_PRESETS)
    presets = plugin.get_related(ns_presets.Preset)
    preset_list = []

    for preset in presets:
        world.load_resource(preset)
        labels = world.find_nodes(preset, world.ns.rdfs.label, None)

        if labels:
            label = str(labels[0])
        else:
            label = None

        preset_list.append((label, str(preset)))

    return preset_list


def main(args=None):
    args = sys.argv[1:] if args is None else args

    if args:
        uri = args[0]
    else:
        return "Usage: lv2_list_plugin_presets <plugin URI>"

    world = lilv.World()
    world.load_all()
    plugins = world.get_all_plugins()

    try:
        plugin = plugins[uri]
    except KeyError as exc:
        return "error: no plugin with URI '%s' found." % uri
    except ValueError as exc:
        return "error: %s" % exc

    presets = get_presets(world, plugin)
    for label, preset_uri in sorted(presets, key=lambda x: x[0] or ''):
        if label is None:
            print("Preset '%s' has no rdfs:label" % preset, file=sys.stderr)

        print("Label: %s" % label or "")
        print("URI: %s\n" % preset_uri)


if __name__ == '__main__':
    sys.exit(main() or 0)
