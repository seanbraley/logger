#!/usr/bin/env python
__author__ = 'Sean Braley, Meghan Brunner, Jenny Chien, Arthur Margulies'
__copyright__ = "Copyright is held by the author/owner(s)."

__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Sean Braley"
__email__ = "sean.braley@queensu.ca"
__status__ = "Prototype"

from socket import socket
from socket import AF_INET, SOCK_DGRAM

from threading import Thread

clientSocket = socket(AF_INET, SOCK_DGRAM)

class ResponseListener(Thread):
    def __init__(self, ):
        super(ResponseListener, self).__init__()

    def run(self):
        while True:
            modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
            print modifiedMessage

# message = raw_input('Enter String: ')
# listener = ResponseListener()
# listener.start()
last_known = '0.4'
with open('data.txt', 'rb') as f:
    for i, line in enumerate(f):
        if line[-2:-1] == '0' or line[-2:-1] == '1':
            newline = line[:-2]+last_known
        else:
            newline = line
            last_known = line[-3:]
        clientSocket.sendto(newline,('sbraley.ca', 12000))



clientSocket.close()