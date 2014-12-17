#!/usr/bin/env python
__author__ = 'Sean Braley, Meghan Brunner, Jenny Chien, Arthur Margulies'
__copyright__ = "Copyright is held by the author/owner(s)."

__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Sean Braley"
__email__ = "sean.braley@queensu.ca"
__status__ = "Prototype"

from socket import AF_INET, SOCK_STREAM, SOCK_DGRAM
from socket import socket

from sklearn.cluster import KMeans, MiniBatchKMeans
from sklearn import preprocessing, metrics
import numpy as np
from scipy import stats
from datetime import datetime


def main():
    serv = socket(AF_INET, SOCK_DGRAM)
    serv.bind(('66.228.43.202', 12000))
    # serv.listen(100)
    counter = 0
    min_max_scaler = preprocessing.MinMaxScaler()
    kmeans_obj = MiniBatchKMeans(n_clusters=14)
    big_ol_array = np.empty((25, 100))
    tmp = [] # Hold 100 items in "buffer" for numpy array
    prev = -1
    while True:
        counter += 1
        message, clientAddress = serv.recvfrom(2048)
        with open("sample.txt", 'a') as f:
            f.write(message.strip())
        item = message.strip().split(',')
        timestamp = item[0]
        fapp = item[-1]
        item[-1] = abs(hash(fapp)) % (10 ** 8)
        tmp.append(np.array([float(x) for x in item[1:]]))
        if counter is 100:
            min_max_scaler.fit(np.array(tmp))
        elif counter % 100 is 0 and counter is not 0:
            print datetime.now(),
            # fit kmeans
            squashed = min_max_scaler.transform(tmp)
            kmeans_obj.partial_fit(squashed)
            a = kmeans_obj.predict(squashed)
            mode, num = stats.mode(a)
            if num[0] >= 18:
                print mode, num
                # output.append(mode[0])
                prev = mode[0]
            else:
                print prev
                # output.append(prev)
            tmp = []
            
        # elif counter%10==0:
        #    x = mmmk.predict(rest)
            # print x
        #    serv.sendto(str(x), clientAddress)
        # else:
        #    mmmk.transform(rest)

        # print message
        # modifiedMessage = message.upper()
        # serv.sendto(modifiedMessage, clientAddress)

if __name__=="__main__":
    main()