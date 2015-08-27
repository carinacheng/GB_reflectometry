#! /usr/bin/env python
import numpy as n 
import pylab as p
import sys, csv

def fromcsv(filename):
    print 'Reading', filename
    d = csv.reader(open(filename,'r'), delimiter=',')
    x = n.array(list(d)[18:-1], dtype=n.float)
    return x[:,0]/1e9, x[:,1]


#file_base = sys.argv[1]
file_base = '../alldata/NC41_12'
amp = '_DB.csv'
phs = '_P.csv'
freqs, amps = fromcsv(file_base + amp)
freqs, phase= fromcsv(file_base + phs)

rloss = amps * n.exp(2j*n.pi*phase/360.)
p.figure(figsize=(10,5))
p.plot(freqs, rloss.real, linewidth=3, label='real')
p.plot(freqs, rloss.imag, linewidth=3, label='imag')
p.xlabel('Frequency (GHz)' )
p.ylabel('Return Loss (dB)')
p.grid(1)
p.xlim(.05,.250)
p.ylim(-25,25)
p.vlines(.1, -100, 100, linestyle='--', linewidth=2)
p.vlines(.2, -100, 100, linestyle='--', linewidth=2)
p.legend()


fig, (ax1,ax2) = p.subplots(2,1, figsize=(10,5), sharex=True)
ax1.plot(freqs, amps, linewidth=3, label='Amplitude')
ax1.set_ylabel('Return Loss (dB)')
ax1.grid(1)
ax1.set_xlim(.05,.250)
ax1.set_ylim(-25,25)
#p.setp(axes[0].get_xticklabels(), visible=False)
ax1.vlines(.1, -100, 100, linestyle='--', linewidth=2)
ax1.vlines(.2, -100, 100, linestyle='--', linewidth=2)
ax1.legend()

ax2.plot(freqs, phase*n.pi/180., linewidth=3, label='Phase')
ax2.set_xlabel('Frequency (GHz)' )
ax2.set_ylabel('Return Loss (dB)')
ax2.grid(1)
ax2.set_xlim(.05,.250)
ax2.set_ylim(-n.pi, n.pi)
ax2.vlines(.1, -100, 100, linestyle='--', linewidth=2)
ax2.vlines(.2, -100, 100, linestyle='--', linewidth=2)
ax2.legend()




p.show()
