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
"""List URIs associated with an LV2 plugin."""

import sys
import lilv


if len(sys.argv) < 2:
    sys.exit("Usage: %s <plugin URI>" % sys.argv[0])

w = lilv.World()
w.load_all()
plugins = w.get_all_plugins()
plugin = plugins[w.new_uri(sys.argv[1])]

print("Name: %s" % plugin.get_name())
print("Plugin URI: %s" % plugin.get_uri())
print("Bundle URI: %s" % plugin.get_bundle_uri())
print("Shared library URI: %s" % plugin.get_library_uri())

nodelist = plugin.get_data_uris()
uris = [str(n) for n in nodelist]
print("Data URIs:")
for uri in uris:
    print("-", uri)

nodelist = plugin.get_uis()
uris = [str(n) for n in nodelist]
print("UI URIs:")
for uri in uris:
    print("-", uri)

nodelist = plugin.get_related(None)
uris = [str(n) for n in nodelist]
print("Resource URIs:")
for uri in uris:
    print("-", uri)
