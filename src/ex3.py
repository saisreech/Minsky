
#Developed by Sai Sree Laya Chukkapalli

from netCDF4 import Dataset
import netCDF4
import pandas as pd
import csv
import os
import sys
import math
#import matplotlib.pyplot as plt
#plt.switch_backend('agg')
import numpy as np
from os import path
import sys, getopt
from os.path import basename
import datetime

# variables
inputFolderPath = ''
outputFolderPath = ''
fileArr = [];

def transferCheck():
        global fileArr;
        for f in range(0,len(fileArr)):
		try:
			transferData(fileArr[f])
		except Exception as ex:
                    template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                    message = template.format(type(ex).__name__, ex.args)
                    print message
		    print("Exception in file " + fileArr[f])


def transferData(fileName):
		f = fileName
		print(f)
		fWithoutExt = f.split(".cdf")[0]
		print(fWithoutExt)
		#fpath = path.join(inputFolderPath,f)
		nc = Dataset(f, mode='r')
		nc.variables.keys()
	        #warn_level=nc.variables['warn_level'][:]
        	#if warn_level[:] > 13:
                time_var=nc.variables['base_time']
                dtime = netCDF4.num2date(time_var[:],time_var.units)
                day=nc.variables['time_offset'][:]
                minutes=((day%3600)/60)
                hour=(day/3600).astype(int)
                finaldtime = []
                for index in range(len(hour)):
                   stime = ""
                   if hour[index] >= 0 and hour[index]<= 9:  
                      stime = stime + ('0'+str(hour[index]))
                   else:
                      stime = stime+(str( hour[index]))
                   stime = stime + ":"
                   if minutes[index]>= 0 and minutes[index]<=9: 
                      stime = stime + ('0'+str(minutes[index]))
                   else:
                      stime = stime + str(minutes[index])
                   finaldtime.append(str(dtime)[0:10]+" "+stime)
                latitude = nc.variables['lat'][:]
                longitude = nc.variables['lon'][:]
                co2flux= nc.variables['fc_corr'][:]
                co2= nc.variables['mean_c'][:]
                varianceco2flux=nc.variables['var_c'][:]
                h2o=nc.variables['mean_q'][:]
                h2ovariance=nc.variables['var_q'][:]
                temperature=nc.variables['mean_t'][:]+273.15
                pressure=nc.variables['mean_p'][:]
                horizontalwinddirection=nc.variables['wdir'][:]
                sensibleheatflux=nc.variables['h'][:]
                latentheatflux=nc.variables['le'][:]
                frictionvelocity=nc.variables['ustar'][:]
                #datetime.fromisoformat(finaldtime).timestamp()
                result = []
                for index in range(len(hour)):
		   #print "I m here"
		   #print index
                   result.append(get_co2_in_ppm(co2[index], varianceco2flux[index], pressure[index], temperature[index]))
		   #print result
		#print "outside"
                print latitude
                print longitude
		ppmDf = pd.DataFrame(result)
		#print ppmDf
                #print warn_level
                df=pd.DataFrame({'date(yyyy/M/d H:mm)':finaldtime,'latitude':latitude,'longitude':longitude,'co2flux(umol m^2 s^1)':co2flux,'co2':co2,'co2inPPM':ppmDf[0],'varianceco2((mmol m^3)^2)':varianceco2flux,'h2o(mmol m^3)':h2o,'h2ovariance((mmol m^3)^2)':h2ovariance,'temperature(degree)':temperature,'pressure(kPa)':pressure,'horizontalwinddirection':horizontalwinddirection,'sensibleheatflux(W m^2)':sensibleheatflux,'latentheatflux(W m^2)':latentheatflux, 'frictionvelocity(m s^1)':frictionvelocity})
                #df = df[df.warn_level > 13]
                #dff=pd.DataFrame(np.random.rand(50,2), columns=[datetime.fromisoformat(finaldtime).timestamp(),'co2inPPM'])
                #ax=df.plot(kind='scatter',x=datetime.fromisoformat(finaldtime).timestamp(),y='co2inPPM')
                #plt.savefig('/home/saisree1/sgp/sgp4m/sgp4m/scatter2.pdf')
                #plt.show()
		print df
                df = df[['date(yyyy/M/d H:mm)','latitude','longitude','co2flux(umol m^2 s^1)','co2','co2inPPM','varianceco2((mmol m^3)^2)','h2o(mmol m^3)','h2ovariance((mmol m^3)^2)','temperature(degree)','pressure(kPa)','horizontalwinddirection','sensibleheatflux(W m^2)','latentheatflux(W m^2)','frictionvelocity(m s^1)']]
		print df
                df.to_csv(outputFolderPath+fWithoutExt+ '.csv', sep='\t')
CO2_MOLAR_MASS = 44.01
H2O_MOLAR_MASS = 18.01
R_GAS_LAW = 8.314
RV_GAS_LAW = 461.51
KELVIN_CONST = 273.15
def get_co2_in_ppm(co2, varianceco2flux, pressure, temperature):
       result = 0
       if temperature == 0:
          result = 0
       else:
          result = ((co2 * R_GAS_LAW * temperature)/(pressure))
       return result

def getFiles():
        global fileArr;
        fileArr = [f for f in os.listdir(inputFolderPath) if f.endswith(".cdf")]
        print(len(fileArr))

def main(argv):
   global inputFolderPath;
   global outputFolderPath;
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifolder=","ofolder="])
   except getopt.GetoptError:
      print 'test.py -i <inputFolderPath> -o <outputFolderPath>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'test.py -i <inputFolderPath> -o <outputFolderPath>'
         sys.exit()
      elif opt in ("-i", "--ifolder"):
         inputFolderPath = arg
      elif opt in ("-o", "--ofolder"):
         outputFolderPath = arg
   print 'Input file is "', inputFolderPath
   print 'Output file is "', outputFolderPath

if __name__ == "__main__":
   main(sys.argv[1:])
   getFiles()
   transferCheck()
   #transferData()

#python ex3.py -i "/home/saisree1/200197sgp/" --ofolder "/home/saisree1/200197sgp/result3/"


