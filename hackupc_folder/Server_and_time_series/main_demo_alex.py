from threading import Timer
import time
import scipy.io
import numpy as np
import scipy.spatial.distance
import time
import matplotlib.pyplot as plt
from operator import itemgetter
from itertools import groupby
import random
def consecutive(data, stepsize=1):
    return np.split(data, np.where(np.diff(data) != stepsize)[0]+1)
def timeout():
    global eix_temporal
    global serie
    print("Timeout executed!")
    if(eix_temporal[0]==1):
        print("CHARGER ON")
    if(eix_temporal[0]==-1):
        print("CHARGER OFF")

    eix_temporal = np.roll(eix_temporal,-1)
    eix_temporal[-1] = 0
    print(eix_temporal)
    print(serie)
    t = Timer(2, timeout)
    t.start()

def timeout2():
    print("Timeout2 executed!")
    data_recived()
    t2 = Timer(random.randint(48, 60), timeout2)
    t2.start()


def data_recived():
    params = [0,1,2]
    print(params)


    t_time = time.gmtime().tm_hour +1
    if(params[2]) == 0:
        t_start = params[0]
        t_end = params[1]
        if(t_start<t_time):
            t_start = t_start+24
        if(t_start>t_end):
            t_end=t_end+24
        print("Time processed: now: ", t_time , " start: ", t_start, " end: ", t_end)
        eix_temporal[t_start-t_time] = 1
        eix_temporal[t_end-t_time] = -1

    if(params[2]) == 1:
        charge_time = params[0]
        charge_time_limit = params[1]
        if(charge_time_limit<t_time):
            charge_time_limit = charge_time_limit+24
        if(charge_time_limit<t_time+charge_time):
            charge_time_limit = charge_time_limit +24

        serie = np.loadtxt("forecast.txt")
        serie = serie[t_time:t_time+48]
        serie_sorted_indexes = np.argsort(serie, axis=0)
        index_bons = serie_sorted_indexes[:charge_time]
        index_bons = np.sort(index_bons)
        ilist = index_bons.tolist()
        index_bons_grouped = consecutive(ilist)

        for aux in index_bons_grouped:
            eix_temporal[aux[0]] = 1
            eix_temporal[aux[-1]+1] = -1
    print(eix_temporal)

eix_temporal = np.zeros(48)

t_time = time.gmtime().tm_hour +1
serie = np.loadtxt("forecast.txt")
#serie = np.log(serie)
time_axis = np.arange(48)
plt.plot(time_axis, serie)
plt.show()
serie = serie[t_time:t_time+48]


t = Timer(1, timeout)
t.start()
time.sleep(1.5)
t2 = Timer(1, timeout2)
t2.start()



t_time = time.gmtime().tm_hour +1
time_axis = np.arange(48)
f = scipy.io.loadmat("serie.mat")
serie = f["serie"]
serie = serie[t_time:t_time+48]
serie = serie.reshape((1,-1))[0]
serie_sorted = np.sort(serie, axis=0)
serie_sorted_indexes = np.argsort(serie, axis=0)
while True:
    input("Press Enter to continue...")
    print("Capturnig Plot!")

    plt.plot(time_axis, serie,'ro')

    indices_one = np.where(eix_temporal == 1)[0]
    indices_eno = np.where(eix_temporal == -1)[0]

    number_ones = np.count_nonzero(eix_temporal==1)
    number_enos = np.count_nonzero(eix_temporal==-1)
    print("Number ones: ",number_ones)
    print("Number enos: ",number_enos)
    i = 0
    if( number_enos>number_ones):
        plt.hlines(20,time_axis[0],time_axis[indices_eno[i]],linewidth=3000, color='#d62728',alpha=0.5)
        indices_eno[i] = 0
        print("Dibuixant linea de ", 0, " a ", time_axis[indices_eno[i]])

    for i in range(0,number_ones):
        plt.hlines(20,time_axis[indices_one[i]],time_axis[indices_eno[i]],linewidth=3000, color='#d62728',alpha=0.5)
        print("Dibuixant linea de ", time_axis[indices_one[i]], " a ", time_axis[indices_eno[i]])
    plt.xlabel('FPR')
    plt.ylabel('TPR')
    plt.title('ROC curves mean vectors')
    plt.grid(True)
    plt.show()
    plt.savefig("testmean_505.png")
