import modules.PerseidasManualSelection as pms
import modules.areaMinimizer as areaMinimizer
import modules.chart as chart
import modules.paralax as paralax

import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import UnivariateSpline
import json

sample = 12

x1 = np.load('data/npy/'+str(sample)+'/x1.npy')
x2 = np.load('data/npy/'+str(sample)+'/x2.npy')
posX1 = np.load('data/npy/'+str(sample)+'/posX1.npy')
posX2 = np.load('data/npy/'+str(sample)+'/posX2.npy')
posY1 = np.load('data/npy/'+str(sample)+'/posY1.npy')
posY2 = np.load('data/npy/'+str(sample)+'/posY2.npy')
br1_R = np.load('data/npy/'+str(sample)+'/br1_R.npy')
br2_R = np.load('data/npy/'+str(sample)+'/br2_R.npy')
br1_G = np.load('data/npy/'+str(sample)+'/br1_G.npy')
br2_G = np.load('data/npy/'+str(sample)+'/br2_G.npy')
br1_B = np.load('data/npy/'+str(sample)+'/br1_B.npy')
br2_B = np.load('data/npy/'+str(sample)+'/br2_B.npy')

br1 = []
br2 = []

for i in range(len(br1_R)):
    br1.append((br1_R[i] + br1_G[i] + br1_B[i])*1.130718954248366)

for i in range(len(br2_R)):
    br2.append((br2_R[i] + br2_G[i] + br2_B[i])*1.130718954248366)


#areaMinimizer, returns k
extrapolate_k = 1
nan,posX1 = areaMinimizer.extrapolate(x1,posX1,k=extrapolate_k); nan,posY1 = areaMinimizer.extrapolate(x1,posY1,k=extrapolate_k); nan,posX2 = areaMinimizer.extrapolate(x2,posX2,k=extrapolate_k); nan,posY2 = areaMinimizer.extrapolate(x2,posY2,k=extrapolate_k); x1,br1 = areaMinimizer.extrapolate(x1,br1,k=extrapolate_k); x2,br2 = areaMinimizer.extrapolate(x2,br2,k=extrapolate_k);

chart.draw2(x1,br1,x2,br2,name='Relative luminance.jpg',xlabel='Frame',ylabel='Relative luminance (0-1000)')
area, k, h = areaMinimizer.adjust(x1,br1,x2,br2)
error = area/(min(len(x1),len(x2)+k)-max(1,k+1))
print('error='+str(error))

#Prints brightness-frame
x2 = np.array(x2) + k
br2 = np.array(br2) + h

print("k="+str(k))

chart.draw2(x1,br1,x2,br2,name='Relative luminance (adjusted).jpg',xlabel='Frame',ylabel='Relative luminance (0-1000)')
