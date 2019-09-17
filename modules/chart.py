from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from itertools import product, combinations
from scipy import stats

import glob
import os

class draw3D:
    def __init__(self):
        self.fig = plt.figure()
        self.ax = self.fig.gca(projection='3d')
        self.ax.set_xlim3d(0,1000)
        self.ax.set_ylim3d(0,1000)
        self.ax.set_zlim3d(0,1000)

    def point(self,v,color=(0.0, 0.0, 0.0)):
        self.ax.scatter(v[0], v[1], v[2], color=color, s=100)

    def earth(self):
        # draw sphere
        u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
        x = np.cos(u)*np.sin(v)*6.3781e6
        y = np.sin(u)*np.sin(v)*6.3781e6
        z = np.cos(v)*6.3781e6
        self.ax.plot_surface(x, y, z, color=(0.31, 0.78, 0.84, 0.4))

    def vector(self,vector,center=[0,0,0],color='k'):
        self.ax.quiver(center[0], center[1], center[2], vector[0], vector[1], vector[2],color=color)

    def u_vector_angle(self,lat,lng,color,Ox=0,Oy=0,Oz=0):
        vPos = [np.cos(np.deg2rad(lat))*np.cos(np.deg2rad(lng)), np.cos(np.deg2rad(lat))*np.sin(np.deg2rad(lng)),np.sin(np.deg2rad(lat))] #x,y,z
        self.ax.quiver(Ox, Oy, Oz, vPos[0], vPos[1], vPos[2],color=color)
        print(vPos)
    def print(self):
        plt.show()

def draw1(x1,y1,dots=False,name=False,xlabel=None,ylabel=None,title=None):
    global dir
    if name == False:
        name = save()
    name = dir+name
    plt.figure()
    plt.clf()
    plt.ion()
    plt.plot(x1,y1)
    if dots == True:
        plt.plot(x1,y1,'o')
    if xlabel != None:
        plt.xlabel(xlabel)
    if ylabel != None:
        plt.ylabel(ylabel)
    if title != None:
        plt.title(title)
    plt.savefig(name)

def draw_regressionline(x1,y1,dots=False,name=False,xlabel=None,ylabel=None,title=None,derivative=False):
    global dir
    if name == False:
        name = save()
    name = dir+name
    plt.figure()
    plt.clf()
    plt.ion()
    plt.plot(x1,y1)
    if dots == True:
        plt.plot(x1,y1,'o')
    if xlabel != None:
        plt.xlabel(xlabel)
    if ylabel != None:
        plt.ylabel(ylabel)
    if title != None:
        plt.title(title)
    if derivative == True:
        plt.title(title)
    slope, intercept, r_value, p_value, std_err = stats.linregress(x1,y1)
    plt.plot(x1,intercept + slope*x1,'--',color='k')

    plt.savefig(name)
    return slope

def draw2scales(x1,y1,dots=False,name=False,xlabel=None,ylabel=None,title=None,derivative=False):
    global dir
    if name == False:
        name = save()
    name = dir+name

    t = np.arange(0.01, 10.0, 0.01)
    data1 = np.exp(t)
    data2 = np.sin(2 * np.pi * t)

    fig, ax1 = plt.subplots()
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Distance (km)')
    ax1.plot(x1, y1)
    slope, intercept, r_value, p_value, std_err = stats.linregress(x1,y1)
    ax1.plot(x1,intercept + slope*x1,'--',color='k')
    ax1.tick_params(axis='y')

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = (0.29, 0.0, 0.0)
    ax2.set_ylabel(derivative, color=color)
    a = np.empty(len(x1))
    a.fill(slope)
    ax2.plot(x1, a, ':',color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()
    plt.savefig(name)

def draw2(x1,y1,x2,y2,name=False,xlabel=None,ylabel=None,title=None,dots=False):
    global dir
    if name == False:
        name = save()
    name = dir+name
    plt.figure()
    plt.clf()
    plt.ion()
    line1, = plt.plot(x1,y1,label="Sample 1")
    line2, = plt.plot(x2,y2,label="Sample 2")
    # Create a legend for the first line.
    first_legend = plt.legend(handles=[line1], loc=1)

    # Add the legend manually to the current Axes.
    ax = plt.gca().add_artist(first_legend)

    # Create another legend for the second line.
    plt.legend(handles=[line2], loc=4)
    if dots == True:
        plt.plot(x1,y1,'o')
    if xlabel != None:
        plt.xlabel(xlabel)
    if ylabel != None:
        plt.ylabel(ylabel)
    if title != None:
        plt.title(title)
    plt.savefig(name)

def save():
    i = 0
    for filename in glob.glob(dir):
        i+=1
    name = "plot"+str(i)+".jpg"
    return name

def create_dir():
    i = 1
    for filename in glob.glob('data/results/*'):
        i+=1
    dir = 'data/results/'+str(i)+'/'
    os.mkdir(dir)
    return dir

dir = create_dir()
