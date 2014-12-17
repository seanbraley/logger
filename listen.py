#!/usr/bin/env python
__author__ = 'Sean Braley, Meghan Brunner, Jenny Chien, Arthur Margulies'
__copyright__ = "Copyright is held by the author/owner(s)."

__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Sean Braley"
__email__ = "sean.braley@queensu.ca"
__status__ = "Prototype"

from socket import AF_INET, SOCK_DGRAM
from socket import socket


def main():
    print "listening"
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind(('66.228.43.202', 12000))
    while True:
        message, _ = sock.recvfrom(2048)
        print message

if __name__ == "__main__":
    main()