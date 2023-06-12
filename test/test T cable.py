import matplotlib.pyplot as plt
import math
import random

# parameters coil
Im = 740
Um = 10
Pm = 3000
R0 = 2.5/740
#R0 = 0.1
L = 9.5
T0 = 20 # temp initial C


dt = 1

# init
ia = Im
ti = 0
T = T0
Tn = 0
To = 0
R = R0

alf = 0.004

tau = L/R


kn = 70/Im/Im
ko = 0.005

print('R0 = ' + str(R0) + '\tkn = ' + str(kn) +  '\tko = ' + str(ko) + '\ttau = ' + str(tau))

gi = []
gt = []
gT = []
gTn = []
gTo = []
gR = []
i=0

job = True
while job:
    # calc

    Tn = ia*ia*R*kn*dt
    if T > T0:
        To = (T-T0)*ko*dt
    else:
        To = 0

    T = T + Tn - To
    dR = alf*R*(T-T0)

    R = R0 + dR

    gt.append(ti/60)
    gi.append(i)
    gT.append(T)
    gTn.append(Tn)
    gTo.append(-To)
    gR.append(R)

    # update
    ti = ti + dt
    i = i+1

    if ti > 1*tau:
        job = False
        print('Irm = ', max(gR), 'If = ', i)



plt.plot(gt, gT, 'r', gt, gTn, "r--", gt, gTo, "b--")
plt.ylabel('T, C')

grU = plt.twinx()
grU.plot(gt, gR, "b")

plt.show()
