import matplotlib.pyplot as plt
import math
import random

# parameters coil
Im = 500
Um = 15
Pm = 3000
R0 = 2.5/740
L = 9.5
tau = L/R0
print('Um = ' + str(Um) + '\tPm = ' + str(Pm) + '\tR = ' + str(R0) + '\tL = ' + str(L)+ '\ttau = ' + str(tau))

dt = 0.1
kp = 0.25
ki = 0.0000095
kd = 500
P = 0
D = 0
I = 0
err = 0
p_err = 0


# init
ia = 0
ua = 0
u0 = 0
ta = 0
ti = 0

# for T
alf = 0.004
kn = 70/740/740
ko = 0.005
T0 = 20
T = T0

R = R0

gi = []
gt = []
guMain = []
guCoil = []
gT = []



job = True
while job:

    #calc i
    i = ua / R * (1 - math.exp(-(dt) / tau)) + ia

    Tn = ia * ia * R * kn * dt
    if T > T0:
        To = (T - T0) * ko * dt
    else:
        To = 0

    T = T + Tn - To
    dR = alf * R * (T - T0)

    R = R0 + dR




    gt.append(ti)
    gi.append(i)
    guMain.append(u0)
    gT.append(T)


    #pid

    err = Im - i
    P = err*kp
    I = I + err*dt
    D = (err-p_err)*dt
    p_err = err
    out = P*kp + I*ki + D*kd

    u0 = out

    if u0 > Um :
        u0=Um
    if u0*i > Pm:
        u0 = Pm/i

    guCoil.append(u0-i*R)

    # update
    ua = u0 - i*R
    ta = ti
    ia = i

    ti = ti + dt

    if i > 0.98 * Im:
        Im = 740
        #kp = 0.2
        #ki = 0.00002
        #kd = 0.5

    if ti > 3*tau:
        job = False
        print('Irm = ', max(gi), 'If = ', i)





#plt.plot(gt, gi, 'r', gt, gup, 'r--')
plt.plot(gt, gi, 'r', gt, gT, 'r--')
plt.ylabel('i, A')

grU = plt.twinx()
grU.plot(gt, guMain, "b", gt, guCoil, "b--")

plt.show()
