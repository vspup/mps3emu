import matplotlib.pyplot as plt
import math
import random

# parameters coil
Im = 740
Um = 10
Pm = 3000
R = 2.5/740
L = 9.5
tau = L/R
print('Um = ' + str(Um) + '\tPm = ' + str(Pm) + '\tR = ' + str(R) + '\tL = ' + str(L)+ '\ttau = ' + str(tau))

dt = 0.1
kp = 0.2
ki = 0.00000483
kd = 100
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


gi = []
gt = []
gu = []
gup = []


job = True
while job:
    i = ua/R * (1 - math.exp(-(ti - ta) / tau)) + ia
    gt.append(ti)
    gi.append(i)
    gu.append(u0)


    #pid
    ii = (ua/R * (1 - math.exp(-(ti - ta) / tau)) + ia) * (random.randrange(99, 101, 10)/100)
    err = Im - ii
    P = err*kp
    I = I + err*dt
    D = (err-p_err)*dt
    p_err = err
    out = P*kp + I*ki + D*kd

    u0 = out

    if u0 > Um :
        u0=Um
    if u0*ii > Pm:
        u0 = Pm/ii

    gup.append(Pm / u0)

    # update
    ua = u0 - i*R
    ta = ti
    ia = i

    ti = ti + dt

    if ti > 3*tau:
        job = False
        print('Irm = ', max(gi), 'If = ', i)

#plt.plot(gt, gi, 'r', gt, gup, 'r--')
plt.plot(gt, gi, 'r')
plt.ylabel('i, A')

grU = plt.twinx()
grU.plot(gt, gu, "b")

plt.show()
