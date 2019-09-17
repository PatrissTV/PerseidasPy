from PyAstronomy import pyasl
import numpy as np

from time import sleep
import modules.chart as chart
import modules.astrometryClient as astrometryClient



def resolve(posX1,posY1,posX2,posY2,k,gps1,gps2,time,sample,br=False,rangi=False):
    min_i = max(1,int(k*100)+1)
    max_i = min(len(posX1),len(posX2)+int(k*100))

    if rangi != False:
        max_i = int(min_i+rangi[1]*30*100)
        min_i = int(min_i+rangi[0]*30*100)

    R = 6.3781e6 #meters
    vPos1 = [(R+gps1['alt'])*np.cos(np.deg2rad(gps1['lat']))*np.cos(np.deg2rad(gps1['lng'])), (R+gps1['alt'])*np.cos(np.deg2rad(gps1['lat']))*np.sin(np.deg2rad(gps1['lng'])),(R+gps1['alt'])*np.sin(np.deg2rad(gps1['lat']))] #x,y,z
    vPos2 = [(R+gps2['alt'])*np.cos(np.deg2rad(gps2['lat']))*np.cos(np.deg2rad(gps2['lng'])), (R+gps2['alt'])*np.cos(np.deg2rad(gps2['lat']))*np.sin(np.deg2rad(gps2['lng'])),(R+gps2['alt'])*np.sin(np.deg2rad(gps2['lat']))] #x,y,z

    UP1 = unit_vector(vPos1)
    N1 = unit_vector(north_vector(UP1))
    E1 = unit_vector(vectorial_product(N1,UP1))

    UP2 = unit_vector(vPos1)
    N2 = unit_vector(north_vector(UP1))
    E2 = unit_vector(vectorial_product(N1,UP1))

    #calibration1 = astrometryClient.AstrometryNetRequest('data/samples/'+str(sample)+'.1/calibration.jpg')
    #calibration2 = astrometryClient.AstrometryNetRequest('data/samples/'+str(sample)+'.2/calibration.jpg')
    #print(calibration1)
    #print(calibration2)
    #calibration1 = {'parity': 1.0, 'width_arcsec': 143487.27671205258, 'ra': 84.99463938909261, 'pixscale': 99.64394216114762, 'radius': 24.910985540286905, 'dec': 0.6353602540561454, 'height_arcsec': 107615.45753403944, 'orientation': 55.364392882015636, 'Cx': 720.0, 'Cy': 540.0}
    #calibration2 = {'parity': 1.0, 'width_arcsec': 141531.83440799525, 'ra': 84.52932092993754, 'pixscale': 36.85724854374876, 'radius': 22.553638079591526, 'dec': 1.061210980135474, 'height_arcsec': 79611.65685449733, 'orientation': 55.1221077687581, 'Cx': 1920.0, 'Cy': 1080.0}

    calibration1 = {'parity': 1.0, 'width_arcsec': 142927.16531219488, 'ra': 54.251847522031525, 'pixscale': 99.25497591124643, 'radius': 24.81374397781161, 'dec': 10.105257995114991, 'height_arcsec': 107195.37398414615, 'orientation': 40.926212382704875, 'Cx': 720.0, 'Cy': 540.0}
    calibration2 = {'parity': 1.0, 'width_arcsec': 141697.8666260761, 'ra': 56.68239406671234, 'pixscale': 36.900486100540654, 'radius': 22.58009594733422, 'dec': (8.487935734631991+0.12333333), 'height_arcsec': 79705.04997716782, 'orientation': 53.84493218675027, 'Cx': 1920.0, 'Cy': 1080.0}

    c = chart.draw3D()

    ra1 = []
    dec1 = []
    ra2 = []
    dec2 = []
    alt = []
    dir1 = []
    dir2 = []
    dir3 = []
    velocity = []
    v_old = [0,0,0]
    v_old2 = [0,0,0]
    v_first = [0,0,0]
    ap = 50
    v1 = None
    lat = []
    lng = []

    for i in range(min_i,max_i):

        ra, dec = pxToCelestial(calibration1,posX1[i],posY1[i])
        alt1, az1 = celestialToHorizontal(ra,dec,time,gps1)

        ra, dec = pxToCelestial(calibration2,posX2[i-int(k*100)],posY2[i-int(k*100)])
        alt2, az2 = celestialToHorizontal(ra,dec,time,gps2)

        dr1 = altazToDirection(alt1,az1,UP1,N1,E1)
        dr2 = altazToDirection(alt2,az2,UP2,N2,E2)

        v = min_dist_point(vPos1,dr1,vPos2,dr2)
        lat2 = np.degrees(np.arcsin(v[2]/vector_longitude(v)))
        lng2 = np.degrees(np.arctan(v[1]/v[0]))
        lat.append(lat2)
        lng.append(lng2)



        alt.append(vector_longitude(v)-R)
        if i > 1:
            dirr = sum_vector(v,scale_vector(v_old,-1))
            dir1.append(v[0])
            dir2.append(v[1])
            dir3.append(v[2])
        if i == min_i:
            v_first = v
            v_old2 = v

        v_old = v


        if ap >= 50:
            print(str(lng2)+","+str(lat2)+","+str(vector_longitude(v)-R))
            velocity1 = vector_longitude(sum_vector(v,scale_vector(v_first,-1)))/(1000)

            if(velocity1):
                velocity.append(velocity1)
            v_old2 = v

            #v = sum_vector(v,scale_vector([5440156.961338621, -731587.4624189744, 3316989.173343559],-1))

            if isinstance(br, (list, tuple, np.ndarray)):
                color_opacity = br[i]/1000
            else:
                color_opacity = 1

            ap = 0
            c.point(sum_vector(v,scale_vector([5486785.483375918, -708179.7092852602, 3332704.2135316683],-1)),color=(1.0, 0.0, 1, 1))
        else:
            ap = ap + 1

    c.print()
    return ra1,dec1,ra2,dec2,alt,velocity,lat,lng



#Trigonometry
def pxToCelestial(calibration,x,y): #convert posX[i] and posY[i] to Ra, Dec
    vX, vY = (x-calibration['Cx']),(y-calibration['Cy'])
    vLen = np.sqrt(np.square(vX) + np.square(vY))
    if vY == 0:
        alpha = 90
    else:
        alpha = np.degrees(np.arctan(vX/vY)) #angle from Up to Right
    alpha = angleTo360(alpha, vX, vY )#Convets Up to Left and always alpha > 0
    pixscale = calibration['pixscale']/3600
    ra = pixscale*vLen*np.sin(np.deg2rad(360 + alpha - calibration['orientation'])) + calibration['ra']
    dec = pixscale*vLen*np.cos(np.deg2rad(360 + alpha - calibration['orientation'])) + calibration['dec']
    return ra, dec

def celestialToHorizontal(ra, dec, time, gps):
    v = pyasl.eq2hor(time, ra, dec, lon=gps['lng'], lat=gps['lat'], alt=0)
    return v[0][0], v[1][0]

def angleTo360(angle, vX, vY):
    if vX <= 0 and vY <= 0:
        return angle
    if vX > 0 and vY < 0:
        return (360 - np.absolute(angle))
    if vX >= 0 and vY >= 0:
        return (np.absolute(angle)+180)
    if vX < 0 and vY > 0:
        return (180 - np.absolute(angle))

#Vectors
def scalar_product(u,v):
    return u[0]*v[0] + u[1]*v[1] + u[2]*v[2]

def vectorial_product(u,v):
    x = u[1]*v[2] - u[2]*v[1]
    y = - u[0]*v[2] + u[2]*v[0]
    z = u[0]*v[1] - u[1]*v[0]
    return [x,y,z]

def vector_longitude(v):
    k = np.sqrt(np.square(v[0]) + np.square(v[1]) + np.square(v[2]))
    return k

def unit_vector(v):
    k = np.sqrt(np.square(v[0]) + np.square(v[1]) + np.square(v[2]))
    return [v[0]/k,v[1]/k,v[2]/k]

def north_vector(n):
    y = (-n[2])/(np.square(n[0])/n[1]+n[1])
    x = n[0]/n[1]*y
    return[x,y,1]

def altazToDirection(alt,az,UP,N,E):
    x = UP[0]*np.sin(np.deg2rad(alt))+N[0]*np.cos(np.deg2rad(alt))*np.cos(np.deg2rad(az))+E[0]*np.cos(np.deg2rad(alt))*np.sin(np.deg2rad(az))
    y = UP[1]*np.sin(np.deg2rad(alt))+N[1]*np.cos(np.deg2rad(alt))*np.cos(np.deg2rad(az))+E[1]*np.cos(np.deg2rad(alt))*np.sin(np.deg2rad(az))
    z = UP[2]*np.sin(np.deg2rad(alt))+N[2]*np.cos(np.deg2rad(alt))*np.cos(np.deg2rad(az))+E[2]*np.cos(np.deg2rad(alt))*np.sin(np.deg2rad(az))
    return x,y,z

def scale_vector(v,k):
    return [v[0]*k,v[1]*k,v[2]*k]

def min_dist_point(vPos1,dr1,vPos2,dr2):
    v = vectorial_product(dr1,dr2)

    a = np.array([[v[0]*dr1[1]-v[1]*dr1[0], v[1]*dr2[0]-v[0]*dr2[1]], [v[1]*dr1[2]-v[2]*dr1[1], v[2]*dr2[1]-v[1]*dr2[2]]])
    b = np.array([v[0]*vPos2[1]+v[1]*vPos1[0]-v[0]*vPos1[1]-v[1]*vPos2[0], v[1]*vPos2[2]+v[2]*vPos1[1]-v[1]*vPos1[2]-v[2]*vPos2[1]])
    result = np.linalg.solve(a,b)

    k1 = result[0]
    k2 = result[1]

    p1 = sum_vector(vPos1,scale_vector(dr1,k1))
    p2 = sum_vector(vPos2,scale_vector(dr2,k2))
    p_error = vector_longitude(sum_vector(p1,scale_vector(p2,-1)))
    print(p_error)
    p_middle = scale_vector(sum_vector(p1,p2),0.5)
    return p_middle

def sum_vector(u,v):
    return [u[0]+v[0],u[1]+v[1],u[2]+v[2]]

def sample():

    return sample
