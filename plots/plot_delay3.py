#! /usr/bin/env python
import numpy as n 
import pylab as p
import sys, csv
import aipy as a
import pd

def fromcsv(filename):
    print 'Reading', filename
    d = csv.reader(open(filename,'r'), delimiter=',')
    x = n.array(list(d)[18:-1], dtype=n.float)
    return x[:,0]/1e9, x[:,1]

def fromcsvdaisy(filename):
    ''' Returns delay(ps), power(dB) '''
    print 'Reading Daisy file ', filename
    d = csv.reader(open(filename, 'r'), delimiter=',')
    x = n.array(list(d)[12:-1], dtype=n.float)
    print x
    return x[:,0]*1e-3, 20.0*n.log10(x[:,1])

def take_delay(db, ph, fq, window='blackman-harris'):
    '''Take reflectometry data in dB and phase to return delay transform.
       Returns windowed and non windowed delay spectra for input spectrum.'''
    d = 10**(db/20) * n.exp(2j*n.pi*ph/360)
    tau = n.fft.fftfreq(fq.size, fq[1]-fq[0])
    window = a.dsp.gen_window(fq.size, window)
    _d = n.fft.ifft(d)
    _dw = n.fft.ifft(d*window) / window.mean() #compensate for window amplitude
    
    if True:
    #if False:
        _dw *= n.abs(_dw[0])  # these should be changed to the dc bin of the windowed data.
        _d *= n.abs(_d[0]) 

    return n.fft.fftshift(_dw), n.fft.fftshift(_d), n.fft.fftshift(tau)


colors = n.array([(31,119,180), (255,127,14), (44,160,44), (214,39,40), (127,127,127), (148,103,189)])/255.

#file_base = sys.argv[1]
file_base = '../alldata/NC41_12'
amp = '_DB.csv'
phs = '_P.csv'
dfile = 'Time/set1/TXT102.csv'
fq, amps = fromcsv(file_base + amp)
fq, phs= fromcsv(file_base + phs)
dns, ddb = fromcsvdaisy(dfile)

valids = {
          '50 - 250 MHz'  : n.where(n.logical_and(fq>.05 ,fq<.25)), 
          '100 - 200 MHz' : n.where(n.logical_and(fq>.1 ,fq<.2)), 
          '140 - 160 MHz' : n.where(n.logical_and(fq>.140 ,fq<.160)),
          '100 - 200 MHz Old' : None
#          'second' : n.where(n.logical_and(fq>.250 ,fq<.500))
         }

#fig, axes = p.subplots(3,1,figsize=(5.4,9))
##fig2, axes2 = p.subplots(3,1,figsize=(10,8))
#for i,v in enumerate(valids.keys()):
#    dw, d, tau = take_delay(amps[valids[v]], phs[valids[v]], fq[valids[v]])
#    print v
#    axes[i].plot(tau, 10*n.log10(n.abs(dw)**2), linewidth=3, label='%s'%v)
#    axes[i].set_xlim(-30,350) 
#    axes[i].set_ylim(-100, 1)
#    axes[i].vlines(60, -100,2, linestyle='--', linewidth=3)
#    axes[i].hlines(-60,-100 ,500, linestyle='--', linewidth=3)
#    axes[i].set_xlabel('delay (ns)')
#    axes[i].set_ylabel('return loss (dB)')
#    axes[i].grid(1)
#    axes[i].legend() 

for i,v in enumerate(valids.keys()):
    print v
    if v == '100 - 200 MHz Old':
        p.plot(dns, ddb, linewidth=2, label='%s'%v, color=colors[i])    
        print dns,ddb
    else:
        dw, d, tau = take_delay(amps[valids[v]], phs[valids[v]], fq[valids[v]], window='hamming')
        p.plot(tau, 10*n.log10(n.abs(dw)**2), linewidth=2, label='%s'%v, color=colors[i])
p.xlim(-30,350) 
p.ylim(-100, 1)
p.vlines(60, -100,100, linestyle='--', linewidth=2)
p.hlines(-60,-100 ,500, linestyle='--', linewidth=2)
p.xlabel('delay (ns)')
p.ylabel('return loss (dB)')
p.grid(1)
p.legend() 

p.show()
