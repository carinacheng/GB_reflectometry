#! /usr/bin/env python

import numpy as n
import pylab as p
import sys, csv
import aipy as a

def fromcsv(filename):
    print 'Reading', filename
    d = csv.reader(open(filename,'r'), delimiter=',')
    x = n.array(list(d)[18:-1], dtype=n.float)
    return x[:,0]/1e9, x[:,1]

def take_delay(db, ph, fq, window='blackman-harris'):
    '''Take reflectometry data in dB and phase to return delay transform.
       Returns windowed and non windowed delay spectra for input spectrum.'''
    d = 10**(db/20) * n.exp(2j*n.pi*ph/360)
    tau = n.fft.fftfreq(fq.size, fq[1]-fq[0])
    window = a.dsp.gen_window(fq.size, window)
    _d = n.fft.ifft(d)
    _dw = n.fft.ifft(d*window) / window.mean() #compensate for window amplitude

    if True:
        _dw *= n.abs(_d[0])
        _d *= n.abs(_d[0])

    return n.fft.fftshift(_dw), n.fft.fftshift(_d), n.fft.fftshift(tau)

#file_base = sys.argv[1]
file_base = '../alldata/NC41_'
amp_end = '_DB.csv'
phs_end = '_P.csv'

valids = [6,9,12,15]

for i,v in enumerate(valids):
    fq,amps = fromcsv(file_base + str(v) + amp_end)
    fq,phs = fromcsv(file_base + str(v) + phs_end)
    bandwidth = n.where(n.logical_and(fq>.05 ,fq<.25)) #HERA bandwidth
    dw, d, tau = take_delay(amps[bandwidth], phs[bandwidth], fq[bandwidth])
    p.plot(tau, 10*n.log10(n.abs(dw)**2), linewidth=2, label=('%s'%v)+'ft')
p.xlim(-30,350)
p.ylim(-100, 1)
p.vlines(60, -100,100, linestyle='--', linewidth=2)
p.hlines(-60,-100 ,500, linestyle='--', linewidth=2)
p.xlabel('delay (ns)')
p.ylabel('return loss (dB)')
p.grid(1)
p.legend()

p.show()
