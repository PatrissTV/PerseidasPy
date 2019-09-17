import numpy as np
from scipy.interpolate import UnivariateSpline
from scipy import stats

step = 0.01 #We divide each frame into 100 interpolations

k_rng = int(1/step)*3 #3!!! areaMinimizer moves the functions 3 frames back and forth

def regression_line(x,y):
    slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)

    return slope, intercept

def area(x,y):
    area = 0
    area2 = 0
    for i in range(1,len(x)):
        area += y[i]*step
    return area

def areaDifference(x1,y1,x2,y2,k,h):
    areaDif = 0
    min_i = max(1,k+1)
    max_i = min(len(x1),len(x2)+k)

    for i in range(min_i,max_i):
        areaDif += np.absolute(y1[i]*step - (y2[i-k] + h)*step)
    return areaDif

def extrapolate(x,y,k=1):
    spl = UnivariateSpline(x, y, k=k)
    x_fit = np.arange(min(x), max(x) + step, step) #x_fit = np.linspace(0, max(x), 1000)
    y_fit = spl(x_fit)
    return x_fit, y_fit

def adjust(x1,y1,x2,y2):
    count = 0
    printk = None
    printh = None
    lastarea = 9e25 #very high value
    lastk = None
    lasth = None
    for k in range(-k_rng, k_rng):
        for ih in range(-50, 50):
            h=ih
            area = areaDifference(x1,y1,x2,y2,k,h)
            if area < lastarea:
                print(area,k,h)
                lastk = k
                lasth = h
                lastarea = area
    return lastarea, lastk*step, lasth
