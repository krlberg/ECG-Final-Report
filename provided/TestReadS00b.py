# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 21:44:30 2019

@author: jeroen
"""

import numpy as np
import matplotlib.pyplot as plt
import datetime 

# Used for file prompt:
# datafile=input("What is the name of the data file: ")
datafile='test7.S00' # fix the data file for quick testing ===
fid=open('test7.S00')           # Open the data file, to allow for sequential reading
# ============================ Read Header information from file ==============================
filetype = np.fromfile(fid,dtype=np.dtype([('FID',np.bytes_,32)]),count=1)[0][0]
version = np.fromfile(fid,dtype=np.int16,count=1)[0]
SignalName= np.fromfile(fid,dtype=np.dtype([('signalName',np.bytes_,81)]),count=1)[0][0]
fs = np.fromfile(fid,dtype=np.int16,count=1)[0]
StorageRate = np.fromfile(fid,dtype=np.int16,count=1)[0]
StorageType = np.fromfile(fid,dtype=np.byte,count=1)[0]
NS = np.fromfile(fid,dtype=np.int16,count=1)[0]
NSP = np.fromfile(fid,dtype=np.int32,count=1)[0] 
emptybytes = np.fromfile(fid,dtype=np.dtype([('EmptyBytes',np.bytes_,4)]),count=1)[0][0]
StartMeasurement = np.fromfile(fid,dtype=np.dtype([('StartMeasurement',np.bytes_,14)]),count=1)[0][0]
NSB = np.fromfile(fid,dtype=np.int32,count=1)[0]
SB= np.fromfile(fid,dtype=np.uint16,count=1)[0]
BS = np.fromfile(fid,dtype=np.uint16,count=1)[0]
flagCompress = np.fromfile(fid,dtype=np.int16,count=1)[0]
nzero = np.fromfile(fid,dtype=np.dtype([('trailingZero',np.bytes_,64)]),count=1)[0][0]

# ========================== Read the infromation of the individual signals form file =============

SignalName = []
UnitName = []
UnitLow = []
UnitHigh = []
ADCLow = []
ADCHigh = []
IndexSignal = []
CacheOffset = []

for i in range(NS): 
    SignalName.append(np.fromfile(fid,dtype=np.dtype([('SignalName',np.bytes_,41)]),count=1)[0][0])
    res1 = np.fromfile(fid,dtype=np.dtype([('Reserved',np.bytes_,4)]),count=1)
    UnitName.append(np.fromfile(fid,dtype=np.dtype([('UnitName',np.bytes_,11)]),count=1)[0][0])
    UnitLow.append(np.fromfile(fid,dtype=np.single,count=1))
    UnitHigh.append(np.fromfile(fid,dtype=np.single,count=1))
    ADCLow.append(np.fromfile(fid,dtype=np.single,count=1))
    ADCHigh.append(np.fromfile(fid,dtype=np.single,count=1))
    IndexSignal.append(np.fromfile(fid,dtype=np.int16,count=1))
    CacheOffset.append(np.fromfile(fid,dtype=np.int16,count=1))
    res2 = np.fromfile(fid,dtype=np.dtype([('Reserved2',np.bytes_,60)]),count=1)


# ========================= print some read data to get an impression of the file content 
print('The file identifier is: ', filetype)
print('The version is: ',version)
print('Number of Signals is: ',NS)
print('The range of signal names is: ',SignalName)
print('The number of sample blocks is: ',NSB)
print('The block size is : ',BS)


# ========================= read the various channels from file ====================
pi = []
signalblock = []
sdata = []
for i in range(NSB):
    fid.seek(218+NS*136+i*(86+BS))
    pi.append(np.fromfile(fid, dtype=np.int32,count=1)[0])          # periode index
    np.fromfile(fid,dtype=np.byte,count=4)                          # reserved, not used
    signalblock.append(np.fromfile(fid, dtype=np.int16,count=7))    # dos time
    np.fromfile(fid,dtype=np.byte,count=64)                         # reserved, not used
    sdata.append(np.fromfile(fid,dtype=np.single,count=np.int(BS/4)))    # actual signal data
#
fid.close()     # Close the file  
#
# Here end the reading of the data from file
#

 
# ======================================== short presentation of data ==============
print('read time data is: ',pi)
plt.plot(pi)
plt.show()
#
sdate = str(datetime.datetime(signalblock[:][0][0],signalblock[:][0][1],signalblock[:][0][2],
                              signalblock[:][0][4],signalblock[:][0][5],signalblock[:][0][6]))
print('The mesurement sdate and time is: ',sdate,'\n')
#
print('results: ',sdata[30][17])
y = np.zeros(NSB)
z = np.zeros(NSB)
for i in range(NSB):
    y[i]=sdata[i][17]
    z[i]=signalblock[i][2]
plt.plot(y,'r')
plt.plot(z,'b')
plt.show()

# ========== continue with conversion and preparation of information to user =========
tsdata = np.transpose(sdata)

plt.plot(tsdata[1])
plt.show()
    
ntsdata = np.empty_like(tsdata)
for i in range(NS):
    ntsdata[i] = np.multiply((tsdata[i]-ADCLow[i])/(ADCHigh[i]-ADCLow[i]),(UnitHigh[i]-UnitLow[i])+ UnitLow[i])

plt.plot(ntsdata[17])
plt.show()


# ========================== 

ts = np.size(tsdata[1])/np.float(fs)
th = np.int(np.floor(ts/3600.))
tm = np.int(np.floor(ts/60. - th*60.))
tss = np.int(np.floor(ts - th*3600. -tm*60.))

MeasurementDuration = str(datetime.time(th,tm,tss))

print('The measurement time is: ',MeasurementDuration)