#!/usr/bin/env python
__author__ = 'Sean Braley, Meghan Brunner, Jenny Chien, Arthur Margulies'
__copyright__ = "Copyright is held by the author/owner(s)."

__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Sean Braley"
__email__ = "sean.braley@queensu.ca"
__status__ = "Prototype"

with open("sample.txt") as f:
    for line in f:
        # print line[100:]
        for i, x in enumerate(line.split("14178")):
            if i is not 0:
                print "14178" + x