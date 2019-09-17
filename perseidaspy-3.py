import modules.paralax as paralax
import modules.chart as chart
import modules.areaMinimizer as areaMinimizer
import modules.gmaps as gmaps

import json
import numpy as np

#Google Maps also shows altitude (METERS)
#gps1 corresponds to samples/1
gps1 = {'lat':31.207140,'lng':-7.858049,'alt':2591.0} #degrees, degrees, meters
gps2 = {'lat':31.206204,'lng':-7.866356,'alt':2724.0} #degrees, degrees, meters

#https://aa.usno.navy.mil/data/docs/JulianDate.php
time = 2458708.678935 #Julian date

sample = 13
img_sample = 2
k = 0.99
rangi = [0.1,0.55]

px_error = 1 #pixels
astrometry_error = 5 #min
k_error = 0.03 #frames

x1 = np.load('data/npy/'+str(sample)+'/x1.npy')
x2 = np.load('data/npy/'+str(sample)+'/x2.npy')
posX1 = np.load('data/npy/'+str(sample)+'/posX1.npy')
posX2 = np.load('data/npy/'+str(sample)+'/posX2.npy')
posY1 = np.load('data/npy/'+str(sample)+'/posY1.npy')
posY2 = np.load('data/npy/'+str(sample)+'/posY2.npy')
br1 = np.load('data/npy/'+str(sample)+'/br1_B.npy')
br2 = np.load('data/npy/'+str(sample)+'/br2_B.npy')

extrapolate_k = 1
nan,posX1 = areaMinimizer.extrapolate(x1,posX1,k=extrapolate_k); nan,posY1 = areaMinimizer.extrapolate(x1,posY1,k=extrapolate_k); nan,posX2 = areaMinimizer.extrapolate(x2,posX2,k=extrapolate_k); nan,posY2 = areaMinimizer.extrapolate(x2,posY2,k=extrapolate_k); x1,br1 = areaMinimizer.extrapolate(x1,br1,k=extrapolate_k); x2,br2 = areaMinimizer.extrapolate(x2,br2,k=extrapolate_k);

ra1,dec1,ra2,dec2,alt,distance,lat,lng = paralax.resolve(posX1,posY1,posX2,posY2,k,gps1,gps2,time,img_sample,br=br1,rangi=rangi)

time = np.array(range(len(alt)))*(3.333e-4)
alt = np.array(alt)/1000 #Convert to km
chart.draw_regressionline(time,alt,name="Altitude",xlabel="Time (s)",ylabel="Altitude (km)")
vertical_speed, intercept = areaMinimizer.regression_line(time,alt)

time = np.array(range(len(distance)))*(50*3.333e-4)
chart.draw_regressionline(time,distance,name="Distance",xlabel="Time (s)",ylabel="Distance (km)")

speed, intercept = areaMinimizer.regression_line(time,distance)
incidence_angle = np.degrees(np.arcsin(np.absolute(vertical_speed/speed)))
#print(speed, vertical_speed,incidence_angle)
