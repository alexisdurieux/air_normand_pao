import numpy as np
import matplotlib.pyplot as plt
import sys

if __name__ == '__main__':
    filename = sys.argv[1]
    data = np.loadtxt(filename)
    plt.figure()
    plt.plot(data[0, :], data[1, :], '+')
    #plt.title('ytest (rouge), ypred (bleu)')
    plt.show()
    