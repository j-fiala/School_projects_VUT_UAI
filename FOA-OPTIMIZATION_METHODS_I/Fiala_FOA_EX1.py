import numpy as np
import matplotlib.pyplot as plt

def f(x):
    return 0.2 * np.exp(x-2)-x

#Fibonacci search
def fibonacci(a,b,n):
    eps = 0.01
    zltr = (1+np.sqrt(5))/2
    s = (1-np.sqrt(5))/(1+np.sqrt(5))
    ro = (1-s**(n))/(zltr*(1-s**(n+1)))
    d = ro * b + (1- ro) * a
    yd = f(d)

    for i in range(1, n-1) :
        if i is n-1:
            c=eps*a+(1-eps)*d
        else:
            c=ro*a + (1-ro)*b
        yc = f(c)
        if yc < yd:
            b=d
            d=c
            yd=yc
        else:
            a=b
            b=c
        ro = (1-s**(n-i))/(zltr*(1-s**(n-i+1)))
    if a<b:
        return a,b
    else:
        a, b = b, a
        return a , b

#Golden section search

def goldensec(a,b,n):
    zltr = (1+np.sqrt(5))/2
    ro = zltr - 1
    d = ro * b + (1- ro) * a
    yd = f(d)
    for i in range(1, n-1) :
        c=ro*a+(1-ro)*b
        yc = f(c)
        if yc < yd:
            b=d
            d=c
            yd=yc
        else:
            a=b
            b=c
    if a<b:
        return a,b
    else:
        a, b = b, a
        return a,b

#Quadratic fit search

def quadfit(a,c,n):
    b = (np.abs(c)+np.abs(a))/2
    ya = f(a)
    yb = f(b)
    yc = f(c)

    for i in range(1, n):
        x = (1/2)*((ya*((b**2)-(c**2))+yb*((c**2)-(a**2))+yc*((a**2)-(b**2)))/(ya*(b-c)+yb*(c-a)+yc*(a-b)))
        yx = f(x)
        if x > b:
            if yx > yb:
                c=x
                yc=yx
            else:
                a=b
                ya=yb
                b=x
                yb=yx
        else:
            if yx > yb:
                a=x
                ya=yx
            else:
                c=b
                yc=yb
                b=x
                yb=yx
    return a,b,c

if __name__ == "__main__":
    n = 5
    a = -1
    b =5

    fig, axs = plt.subplots(2, 2, figsize=(12,9))
    x = np.arange(a,b,0.1)
    axs[0, 0].plot(x, f(x),'black')
    axs[0, 0].set_title("Function of interest")

    axs[1, 0].plot(x, f(x),'black')
    a2, b2 = fibonacci(a,b,n)
    x2 = np.arange(a2, b2, 0.1)
    axs[1, 0].plot(x2, f(x2),'r')
    axs[1, 0].text(0.4, 0.4, [a2, b2],color='red', fontsize=9)
    axs[1, 0].set_title("Fibonacci search")
    
    axs[1, 0].sharex(axs[0, 0])

    axs[0, 1].plot(x, f(x),'black')
    a3, b3 = goldensec(a,b,n)
    x3 = np.arange(a3, b3, 0.1)
    axs[0, 1].plot(x3, f(x3),'r')
    axs[0, 1].text(0.4, 0.4, [a3, b3],color='red', fontsize=9)
    axs[0, 1].set_title("Golden section search")

    axs[1, 1].plot(x, f(x),'black')
    a4, b4, c4 = quadfit(a,b,n)
    x4 = np.arange(a4, c4, 0.1)
    axs[1, 1].plot(x4, f(x4),'r')
    axs[1, 1].text(0.4, 0.4, [a4, b4, c4],color='red', fontsize=9)
    axs[1, 1].set_title("Quadratic fit search")
    fig.tight_layout()
    plt.show()
