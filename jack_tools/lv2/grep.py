# MIT License

# Copyright (c) 2019 Christopher Arndt, 2020 Alexis Boni

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
"""Print URIs of all installed LV2 plugins matching given regular expression.
"""

import argparse
import json
import re
import sys

import lilv


def main(args=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('-c', '--categories', action="store_true",
                    help="Add list of categories for each plugin (requires -j)")
    ap.add_argument('-i', '--ignore-case', action="store_true",
                    help="Ignore case")
    ap.add_argument('-j', '--json', action="store_true",
                    help="Print output as list of objects in JSON format")
    ap.add_argument('pattern', nargs='?', help="LV2 plugin URI pattern")
    args = ap.parse_args(args)

    if args.pattern:
        rx = re.compile(args.pattern, re.I if args.ignore_case else 0)

    world = lilv.World()
    world.load_all()

    results = []
    for node in world.get_all_plugins():
        uri = str(node.get_uri())

        if not args.pattern or rx.search(uri):
            if args.json:
                # load all resources in bundle
                world.load_resource(uri)
                name = node.get_name()
                plugin_data = {
                    'name': str(name) if name is not None else None,
                    'uri': uri
                }

                if args.categories:
                    categories = []
                    for cat in node.get_value(world.ns.rdf.type):
                        cat = str(cat)
                        formatted_category = re.search("#(.+)Plugin$", cat)
                        if cat is not None:
                            if formatted_category:
                                categories.append(formatted_category.group(1))

                    plugin_data['categories'] = categories

                results.append(plugin_data)
            else:
                print(uri)

    if args.json:
        json.dump(results, sys.stdout, indent=2)


if __name__ == '__main__':
    sys.exit(main() or 0)
