import sys, os, math
import matplotlib.pyplot as plt
import matplotlib.transforms as transforms
from matplotlib.font_manager import FontProperties
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

def plot(t, timeseries, canvas = False):
    def r(x):
        return x.read(t, 0.0)
    temp = r(timeseries['temp'])
    dewpt = r(timeseries['dewpt'])
    pop = r(timeseries['pop'])
    wind = r(timeseries['wind'])
    dir = r(timeseries['dir'])
    gust = r(timeseries['gust'])
    clouds = r(timeseries['clouds'])
    humidity = r(timeseries['humidity'])
    flyability = r(timeseries['flyability'])

    fontP = FontProperties()
    fontP.set_size('small')

    fig = plt.figure(1, figsize=(35,9))

    ax = plt.subplot(511)
    plt.plot(t, flyability, 'r', label="flyability")
    plt.ylabel("%")
    plt.ylim(0,110)
    locs, labels = plt.yticks()
    plt.yticks(locs[:-1])
    plt.tick_params(axis='x', which='both', labeltop='on', labelbottom='off')
    ax.legend(loc='best', prop=fontP, fancybox=True, shadow=True)

    ax = plt.subplot(512)
    plt.plot(t, wind, 'r', label="wind speed")
    plt.plot(t, gust, 'b', label="gust speed")
    plt.ylabel("mph")
    locs, labels = plt.yticks()
    plt.yticks(locs[:-1])
    ax.legend(loc='best', prop=fontP, fancybox=True, shadow=True)

    ax = plt.subplot(513)
    X = getXComponents(dir, wind)
    Y = getYComponents(dir, wind)
    plt.xlim(0,len(t)-1)
    plt.ylim(-1,1)
    Q = plt.quiver(range(0,len(t)), [0]*len(t), X,Y, units='height', 
                   scale=4*max(Y), width = 0.02)
    plt.quiverkey(Q, 0.95, 0.9, 10, "wind direction and speed", labelpos="W", 
                  coordinates='axes', fontproperties={'size':'small'})
    ax.get_yaxis().set_visible(False)
    plt.xticks(range(0,len(t),3))

    ax = plt.subplot(514)
    plt.plot(t, temp, 'r', label="temperature")
    plt.plot(t, dewpt, 'b', label="dew point")
    locs, labels = plt.yticks()
    plt.yticks(locs[1:])
    plt.ylabel(u"\u00b0F")
    ax.legend(loc='best', prop=fontP, ncol=2, fancybox=True, shadow=True)

    plt.subplot(515)
    plt.plot(t, clouds, 'g', label = "cloud cover")
    plt.plot(t, humidity, 'r', label = "humidity")
    plt.plot(t, pop, 'b', label="chance of precipitation")
    plt.ylabel("%")
    plt.ylim(0,120)
    locs, labels = plt.yticks()
    plt.yticks(locs[1:-1])
    plt.legend(loc='best', prop=fontP, ncol=3, fancybox=True, shadow=True)

    fig.subplots_adjust(hspace=0)
    for i,ax in enumerate(fig.axes):
        if i != 1:
            ax.xaxis.set_major_locator( DayLocator())
            ax.xaxis.set_major_formatter( DateFormatter('%b %d') )
            ax.xaxis.set_minor_locator( HourLocator(range(3,22,3)) )
            ax.xaxis.set_minor_formatter( DateFormatter('%I%p') )
            ax.grid(True, which='both')
        else:
            ax.grid(True)
        if i != len(fig.axes) - 1 and i != 0:
            ax.set_xticklabels([])
        ax.tick_params(labelsize='small', which='minor')
    
    if canvas:
        canvas = FigureCanvas(fig)
        return canvas
    else:
        plt.show()

def displayHeightToData(ax, d):
    inv = ax.transData.inverted()
    return inv.transform((0, d))[1]

def toX(rad):
    return - math.sin(rad)

def toY(rad):
    return - math.cos(rad)

def getComponents(dirs, speeds, fn):
    outs = []
    for i,d in enumerate(dirs):
        rad = math.radians(float(d))
        out = float(fn(rad))
        out *= float(speeds[i])
        outs.append(out)
    return outs

def getXComponents(dirs, speeds):
    return getComponents(dirs, speeds, toX)

def getYComponents(dirs, speeds):
    return getComponents(dirs, speeds, toY)

