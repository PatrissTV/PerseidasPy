import modules.PerseidasManualSelection as pms
import numpy as np
import json
import os
import glob

#Init script
#PMS, returns br and posXY

sample = 2
x1,posX1,posY1,br1_R,br1_G,br1_B,x2,posX2,posY2,br2_R,br2_G,br2_B = pms.init(sample)



def create_dir():
    i = 1
    for filename in glob.glob('data/npy/*'):
        i+=1
    dir = 'data/npy/'+str(i)+'/'
    os.mkdir(dir)
    return dir

dir = create_dir()
np.save(dir+'x1',x1)
np.save(dir+'x2',x2)
np.save(dir+'br1_R',br1_R)
np.save(dir+'br1_G',br1_G)
np.save(dir+'br1_B',br1_B)
np.save(dir+'br2_R',br2_R)
np.save(dir+'br2_G',br2_G)
np.save(dir+'br2_B',br2_B)
np.save(dir+'posX1',posX1)
np.save(dir+'posY1',posY1)
np.save(dir+'posX2',posX2)
np.save(dir+'posY2',posY2)
