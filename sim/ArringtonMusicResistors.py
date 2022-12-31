
from matplotlib import pylab as plt
import numpy as np
import scipy.stats

Rvalue6bit = np.array([ 1e9, 1e9, 82500, 40200, 20000, 10000, 4990, 2490])
Rvalue8bit = np.array([ 330000, 160000, 82500, 40200, 20000, 10000, 4990, 2490])
Rname = ['R10','R11','R6','R4','R3','R5','R7','R8']

Rpullup = 220  # R9
Vol = 0.35 # Volts
Vcc = 5.0

# from an 8 resistor set, create x and y values. x = 8 bit value, y = Vout
def CreateValues(R):
    x = []
    y = []
    for v in range(0,256):
        Rdown = 1e9  # Uninitialized
        for bit in range(0,8):
            if ((v >> bit) & 1) == 0:  # pull down active
                #print(f"    bit {bit} low")
                Rdown = Rdown*R[bit]/(Rdown + R[bit])
        # Iup = Idown
        # (Vcc-Vout)/Rpullup = (Vout-Vol)/Rdown
        # Solve for Vout:
        # Vcc/Rpullup + Vol/Rdown = Vout/Rdown + Vout/Rpullup
        # Vcc*Rdown + Vol*Rpullup = Vout*(Rpullup + Rdown)
        # Vout = (Vcc*Rdown + Vol*Rpullup)/(Rpullup + Rdown)
        Vout = (Vcc*Rdown + Vol*Rpullup)/(Rpullup + Rdown)
        print(v,Vout)
        x.append(v)
        y.append(Vout)
    x = np.array(x)
    y = np.array(y)
    return x,y

x,y = CreateValues(Rvalue6bit)
xh,yh = CreateValues(Rvalue8bit*1.01)
xl,yl = CreateValues(Rvalue8bit*0.99)

# offset the points like the AC coupling would
#ymax = y.max()
#ymin = y.min()
#y = y - (ymin+ymax)/2

# create a linear fit
r = scipy.stats.linregress(x, y)
m = r.slope
b = r.intercept

# original data
plt.plot(x,y,'.-')

# regression line
firstx = x[0]
lastx = x[-1]
firsty = m*x[0]+b
lasty = m*x[-1]+b
plt.plot([firstx, lastx], [firsty, lasty],'-')

# high points
plt.plot(xh,yh,'.-')

# low points
plt.plot(xl,yl,'.-')

plt.show()


