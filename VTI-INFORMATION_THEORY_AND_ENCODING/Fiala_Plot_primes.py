#Program VTI, Jan Fiala, 217141
import numpy as np
from math import log
import matplotlib.pyplot as plt, numpy as np
import matplotlib.animation as animation

import mpl_toolkits.axes_grid1
import matplotlib.widgets

from timeit import default_timer

#funkce na generovani prvocisel
def primes_method(n):
    if n < 6:
        out = list([2,3,5,7,11])
        out = out[:n]
    else:
        n = int(n * (log(n) + log(log(n))))
        out = list()
        sieve = [True] * (n+1)
        for p in range(2, n+1):
            if (sieve[p] and sieve[p]%2==1):
                out.append(p)
                for i in range(p, n+1, p):
                    sieve[i] = False
    return out
    
# Vykresleni grafu a animace natoceni, widgety pro spousteni
class Player():

    # Vstup: nums = list
    def __init__ (self, nums, timevalue):
        self.nums = nums
        self.create_plot(nums, timevalue)

    def create_plot(self, nums, timevalue):
        bg_color = '#000000'
        figsize = 8

        self.x = nums*np.cos(nums)
        self.y = nums*np.sin(nums)
        self.z = nums
        
        fig = plt.figure(figsize=(figsize, figsize))
        fig.patch.set_facecolor(bg_color)

        self.ax = fig.add_subplot(projection='3d')
        self.ax.set_facecolor(bg_color)
        
        plt.axis('off')
        plt.grid(visible=False)  
        
        self.points = self.ax.scatter(self.x,self.y,self.z, s=1)
        
        #Pozice tlacitek a textboxu
        self.ax.text2D(0.00, 1.02, 'Počet zobrazených prvočísel: {}'.format(len(nums)), color='white', transform=self.ax.transAxes)
        self.ax.text2D(0.00, 0.985, 'Doba hledání prvočísel: {} s'.format(timevalue), color='white', transform=self.ax.transAxes)
        sax = plt.axes([0.125, 0.92, 0.74, 0.04])
        sax2=mpl_toolkits.axes_grid1.make_axes_locatable(sax)
        fax = sax2.append_axes("right", size="100%", pad=0.05)
        button_stop = matplotlib.widgets.Button(sax, label='$\u25A0$', color = 'white')
        button_forward = matplotlib.widgets.Button(fax, label='$\u25B6$', color = 'white')
        button_stop.on_clicked(self.stop)
        button_forward.on_clicked(self.start)
        self.anim = animation.FuncAnimation(fig, self.update, frames=np.arange(0,362,2),interval=50)

        plt.show()

    def start(self, event=None):
        self.runs=True
        self.anim.event_source.start()

    def stop(self, event=None):
        self.runs = False
        self.anim.event_source.stop() 

    #natoceni souradnicoveho systemu
    def update(self, i):
        color = plt.cm.gist_rainbow(i)
        self.points.set_color(color)
        self.ax.view_init(azim=i)

    #vykresleni 2D grafu pri poctu cisel vetsim jak 10000
def polar_plot(primes, timesvalue):
    bg_color = '#000000'
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='polar')
    ax.set_yticklabels([])
    ax.grid(False)
    ax.set_facecolor(bg_color)
    fig.patch.set_facecolor(bg_color)
    ax.text(0.00, 1.02, 'Počet zobrazených prvočísel: {}'.format(len(primes)), color='white', transform=ax.transAxes)
    ax.text(0.00, 0.985, 'Doba hledání prvočísel: {} s'.format(timevalue), color='white', transform=ax.transAxes)
    ax.scatter(primes, primes, s=0.3, c= "orange" )
    plt.show()

# zadani pocatecnych hodnot a mereni casu 
if __name__ == "__main__":
    out = 0
    print("Zadej pocet prvocisel co hledame:")
    n = int(input())
    if n < 0:
        print("Zadej cislo vetsi nez 0!")
        exit()

    start = default_timer()
    primes = primes_method(n)
    numbers = len(primes)-n
    primes = primes[:len(primes)-numbers]
    timevalue = default_timer()-start

    #podminka vykresleni\
    if n > 10000:
        print(timevalue)
        polar_plot(primes, timevalue)
    else:
        Player(primes, timevalue)