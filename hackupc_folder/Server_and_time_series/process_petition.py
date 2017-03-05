from threading import Timer
import time
import scipy.io
import numpy as np
import scipy.spatial.distance
import matplotlib.pyplot as plt
from operator import itemgetter
from itertools import groupby


def consecutive(data, stepsize=1):
    return np.split(data, np.where(np.diff(data) != stepsize)[0]+1)


eix_temporal = np.zeros(48)
print(eix_temporal)

params=[5,8,0]
params=[6,18,1]
t = time.gmtime().tm_hour +1
if(params[2]) == 0:
    t_start = (params[0] - t)%12
    t_end = (params[1] -t)%12
    print(t)
    print(t_start)
    print(t_end)
    eix_temporal[t_start] = 1
    eix_temporal[t_end] = -1



if(params[2]) == 1:
    charge_time = params[0]
    charge_time_limit = (params[1] -t)%12

    f = scipy.io.loadmat("serie.mat")
    serie = f["serie"]
    serie = serie[t:t+48]
    serie = serie.reshape((1,-1))[0]
    print(serie[0])
    serie_sorted = np.sort(serie, axis=0)
    print(serie_sorted)
    serie_sorted_indexes = np.argsort(serie, axis=0)
    print(serie_sorted_indexes)
    print(serie.size)
    time_axis = np.arange(eix_temporal.size)

    index_bons = serie_sorted_indexes[:charge_time]
    index_bons = np.sort(index_bons)

    print(index_bons)
    ilist = index_bons.tolist()
    index_bons_grouped = consecutive(ilist)

    print(index_bons_grouped)

    plt.plot(time_axis, serie)
    for aux in index_bons_grouped:
        plt.hlines(serie[aux],time_axis[aux[0]],time_axis[aux[-1]] + 1,linewidth=3000, color='#d62728',alpha=0.5)
        eix_temporal[aux[0]] = 1
        eix_temporal[aux[-1]+1] = -1
    plt.xlabel('FPR')
    plt.ylabel('TPR')
    plt.title('ROC curves mean vectors')
    plt.grid(True)
    plt.show()

    plt.savefig("testmean_505.png")
print(eix_temporal)
