# emulator mps3
from tkinter import *
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from time import *
from random import *
import numpy
import math
from threading import Thread
from time import sleep



#TOUT = 1 # s

TSOLW = 250 #ms
Kaks = 1000 # 1 to 1000
TUPD = 1000/Kaks


#
WB = 24
WBR = 80


# class create gui to coil
class SCoil:

    def __init__(self, rc, lc, master, txt):

        # coil parameters
        self.u0 = 0.0
        self.i0 = 0.0
        self.R0 = rc
        self.R = self.R0
        self.L = lc
        self.tau = self.L / self.R0
        self.i_cur = float(0.0)
        self.ti = 0
        self.du = 0
        self.t0 = 0
        self.u_main = 0
        self.i_main = 0
        self.T = 20
        self.T0 = 20

        #self.t_out = TOUT  # period update grafic

        self.t_solw = TSOLW  # period solw ms

        self.t_upd = TUPD

        print('tup = ' + str(self.t_upd) + ' tsol = ' + str(self.t_solw))


        # geometric parameters
        a = 2  # width label
        b = 1  # widht button
        # full width (2*a+b)
        c = (2*a+b)
        self.job = 0 # mark regimes ON j=1 OFF j=0

        self.w = master["width"]
        # label on frame with TXT parameter
        self.f = LabelFrame(master, text=txt, bd=5)
        # create label of current I and V
        self.ic = Label(self.f, width=int(self.w*(a/c)), fg='red', font=("Arial", 14, "bold"), justify='right')
        self.uc = Label(self.f, width=int(self.w*(a/c)), fg='blue', font=("Arial", 14, "bold"), justify='right')


        # plasement gui interfase
        self.ic.grid(row=0, column=0, sticky=W, pady=10, padx=10)
        self.uc.grid(row=0, column=1, sticky=W, pady=10, padx=10)


        # init station off
        self.ic["text"] = str(self.i_cur) + ' A'
        self.uc["text"] = str(self.u_main) + ' V'

        self.f.pack()

        # animation
        self.fig = plt.Figure()

        self.ax = self.fig.add_subplot(111)
        self.fig.subplots_adjust(bottom=0.25)

        self.gi = [0]   # graf i main
        self.gt = [0]   # graf t
        self.gu = [0]   # graf v main
        self.guCoil = [0]   # graf V coil
        self.gR = [0]   # graf R

        self.grf, = self.ax.plot(self.gt, self.gi, 'r')
        self.ax.set_ylabel("I, A", color='r')

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.f)
        self.canvas.get_tk_widget().grid(column=0, row=1, columnspan=3)

        # Second plot
        self.axU = self.ax.twinx()
        self.grfU, = self.axU.plot(self.gt, self.gu, "b")
        self.grfUCoil, = self.axU.plot(self.gt, self.guCoil, "b--")
        self.axU.set_ylabel("U, V", color='b')

        #
        self.fLeads = IntVar()
        self.leads = Checkbutton(self.f, text='leads', variable=self.fLeads)
        self.leads.grid(column=0, row=2, padx=10, pady=10, sticky='nsew')
        self.fLeads.set(1)




    def set_u(self, unew):
        self.u_main = float(unew)
        self.i0 = self.i_cur
        self.u0 = self.i_cur * self.R
        self.du = self.u_main - self.u0
        #self.t0 = self.ti


    def cur(self):
        if (self.job==1):
            self.update_current()

            if (round(self.ti)*1000 % 1000) == 0:
                self.guCoil.append(self.u_main - self.i_cur * self.R)
                self.gi.append(self.i_cur)
                self.gt.append(self.ti)
                self.gu.append(self.u_main)
                self.gR.append(self.R/self.R0*100)

                self.ic["text"] = str(self.i_cur) + ' A'
                #self.uc["text"] = str(self.u_main) + ' V'
                self.uc["text"] = str(self.R/self.R0*100) + ' %'

                # grafic
                #if (round(self.ti) % self.t_out == 0):
                self.grf.set_data(self.gt, self.gi)


                # Update axis
                ax = self.canvas.figure.axes[0]
                ax.set_xlim(min(self.gt), self.ti)
                ax.set_ylim(min(self.gi)-50, max(self.gi)+50)
                #self.axU.set_ylim(min(self.gu)-1, max(self.gu)+1)
                self.axU.set_ylim(min(self.gR) - 1, max(self.gR) + 1)


                self.grfU.set_data(self.gt, self.gR)
                self.grfUCoil.set_data(self.gt, self.guCoil)

                self.canvas.draw()
                print(self.R)

            # periodic update
            root.after(int(self.t_upd), self.cur)


    def update_current(self):
        kn = 70 / 740 / 740
        ko = 0.005
        alf = 0.004
        dt = self.t_solw/1000

        if self.fLeads.get() == True:

            self.i_cur = float((self.du / self.R) * (1 - math.exp(-(self.t_solw/1000) / self.tau))) + self.i_cur
            self.tl = self.ti
            self.Rl = self.R
        else:

            self.i_cur = 0

        Tn = self.i_cur * self.i_cur * self.R * kn * dt
        if self.T > 20:
            To = (self.T - 20) * ko * dt
        else:
            To = 0

        self.T = self.T + Tn - To
        dR = alf * self.R * (self.T - 20)

        self.R = self.R0 + dR


        self.ti = self.ti + dt


    def ch_mode(self, j):
        if self.job != j:
            if j == 1:
                self.job = 1
                # if ON start get current value I and U
                self.ti = 0
                self.i_cur = 0
                # self.u_main = 0
                self.i0 = self.i_cur
                self.u0 = self.i_cur * self.R
                self.du = self.u_main - self.u0
                self.t0 = self.ti
                self.cur()

            elif j == 0:
                self.ic["text"] = "" + ' A'
                self.uc["text"] = "" + ' V'
                self.job = 0
                self.gt = [0]
                self.gi = [0]
                self.gu = [0]
                self.guCoil = [0]
                self.grf.set_data(self.gt, self.gi)
                self.grfU.set_data(self.gt, self.gu)
                self.grfUCoil.set_data(self.gt, self.guCoil)
                # Update axis
                ax = self.canvas.figure.axes[0]
                ax.set_xlim(min(self.gt), self.ti)
                ax.set_ylim(min(self.gi) - 1, max(self.gi) + 1)
                self.axU.set_ylim(min(self.gu) - 1, max(self.gu) + 1)
                self.canvas.draw()



class Interfase:

    def __init__(self, master, sCoil):
        a = 2  # width label
        b = 1  # widht button
        # full width (2*a+b)
        c = (2*a + 2*b)

        # class main coil
        self.Coil = sCoil

        self.j = 0 # mark regimes ON j=1 OFF j=0
        #self.t_out = TOUT

        # current walue
        self.uu = 0

        self.w = master["width"]
        # label on frame with TXT parameter
        self.f = LabelFrame(master, text='Interfase', bd=5)
        # create entry of I V with set
        self.mode = Entry(self.f, width=int(self.w * (a / c)))
        self.i = Entry(self.f, width=int(self.w * (a/c)))
        self.u = Entry(self.f, width=int(self.w * (a/c)))
        # create label of I and V
        self.ic = Label(self.f, width=int(self.w*((b/c))), fg='red', font=("Arial", 14, "bold"), justify='right')
        self.uc = Label(self.f, width=int(self.w*(b/c)), fg='blue', font=("Arial", 14, "bold"), justify='right')
        # create button
        self.smode = Button(self.f, text="mode", width=int(self.w * (b / c)))
        self.si = Button(self.f, text="set", width=int(self.w * (b/c)))
        self.su = Button(self.f, text="set", width=int(self.w * (b/c)))

        # create label of current Imax and Vmax
        self.gmode = Label(self.f, width=int(self.w * (a / c)), fg='red', font=("Arial", 14, "bold"), justify='right')
        self.im = Label(self.f, width=int(self.w * (a/c)), fg='red', font=("Arial", 14, "bold"), justify='right')
        self.um = Label(self.f, width=int(self.w * (a/c)), fg='blue', font=("Arial", 14, "bold"), justify='right')

        # plasement gui interfase
        # row 0
        self.mode.grid(row=0, column=0, sticky=W, pady=10, padx=10)
        self.smode.grid(row=0, column=1, sticky=W, pady=10, padx=10)
        self.gmode.grid(row=0, column=2, sticky=W, pady=10, padx=10)
        # row 1 (i main)
        self.i.grid(row=1, column=0, sticky=W, pady=10, padx=10)
        self.ic.grid(row=1, column=1, sticky=W, pady=10, padx=10)
        self.si.grid(row=1, column=2, sticky=W, pady=10, padx=10)
        self.im.grid(row=1, column=3, sticky=W, pady=10, padx=10)
        # row 2 (u main)
        self.u.grid(row=2, column=0, sticky=W, pady=10, padx=10)
        self.uc.grid(row=2, column=1, sticky=W, pady=10, padx=10)
        self.su.grid(row=2, column=2, sticky=W, pady=10, padx=10)
        self.um.grid(row=2, column=3, sticky=W, pady=10, padx=10)

        # init station off
        self.i["state"] = NORMAL
        self.si["state"] = NORMAL
        self.u["state"] = NORMAL
        self.su["state"] = NORMAL
        self.ic["text"] = ' A'
        self.uc["text"] = ' V'

        # function button on
        self.smode['command'] = self.set_mode
        self.su['command'] = self.set_um
        self.si['command'] = self.set_im

        self.mode.insert(END, '1')
        self.i.insert(END, '')
        self.u.insert(END, '10')
        self.um["text"] = str(self.Coil.u_main) + " V"
        self.im["text"] = str(self.Coil.i_main) + " A"
        self.gmode["text"] = str(self.Coil.job)

        self.f.pack()


    def set_um(self):
        print(self.u.get())
        if (self.u.get() != ''):
            self.uu = float(self.u.get())
            if self.uu <= 15:
                self.Coil.set_u(self.uu)
        print(self.Coil.u_main)
        self.um["text"] = str(self.Coil.u_main) + " V"



    def set_im(self):
        print(self.i.get())
        if self.i.get() != '':
            self.im = float(self.i.get())


    def set_mode(self):
        self.Coil.ch_mode(int(self.mode.get()))
        self.gmode["text"] = str(self.Coil.job)


# start windows
root = Tk()

# create tabs
note=ttk.Notebook(root)
note.pack(side=TOP,fill=X)
f1=Frame(note, height=400)
f2=Frame(note, height=400)
note.add(f1, text="main coil")
note.add(f2, text="shim")

# function of sheck current tab
def find(event):
    if event.widget.index("current") == 0:
       print("--> One")
    elif event.widget.index("current") == 1:
       print("--> Two")

    #print(note.tabs().index(note.select()))

note.bind("<<NotebookTabChanged>>", find)


# status bar
bar=Button(root,text="off",bg="light grey", command=find)
bar.pack(side=TOP,fill=X)

# organize tab 1
frameR=Frame(f1, bd=5, width=WBR)
frameR.pack(side=TOP)
# organize tab 2
frame1=Frame(f2, bd=5, width = WB)
frame2=Frame(f2, bd=5, width = WB)
frame1.pack(side=LEFT)
frame2.pack(side=LEFT)

# global
U = 5
R = 2.5/740
#R = 2
L = 9.5
T = 3000
print('tau = ' + str(L/R))


# add panel to tabs 1
blockR = SCoil(R, L, frameR, 'RAMP')
nlockG = Interfase(frameR, blockR)

# add panel to tab 2
blockA = [i for i in range(6)]
blockB = [i for i in range(6)]
for i in range(6):
    blockA[i] = SCoil(R, L, frame1, 'A' + str(i))
    blockB[i] = SCoil(R, L, frame2, 'T' + str(i))



root.mainloop()

