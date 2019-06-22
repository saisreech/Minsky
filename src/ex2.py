#This code has been Developed by Sai Sree Laya Chukkapalli for running multiple files of any high dimensional format specifically satellite data to csv files for multiple variables.

from netCDF4 import Dataset
import netCDF4
import pandas as pd
import csv
import os
import sys
from os import path
import sys, getopt
from os.path import basename

# variables
inputFolderPath = ''
outputFolderPath = ''
fileArr = [];

def transferCheck():
        global fileArr;
        for f in range(0,len(fileArr)):
		try:
			transferData(fileArr[f])
		except:
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
                meanco2density=nc.variables['mean_c'][:]
                varianceco2density=nc.variables['var_c'][:]
                h2o=nc.variables['mean_q'][:]
                h2ovariance=nc.variables['var_q'][:]
                temperature=nc.variables['mean_t'][:]
                temperaturevariance=nc.variables['var_t'][:]
                pressure=nc.variables['mean_p'][:]
                horizontalwinddirection=nc.variables['wdir'][:]
                rotationtozerowtheta=nc.variables['theta'][:]
                rotationtozerovphi=nc.variables['phi'][:]
                sensibleheatflux=nc.variables['h'][:]
                latentheatflux=nc.variables['le'][:]
                frictionvelocity=nc.variables['ustar'][:]
                print latitude
                print longitude
                #print warn_level
                df = pd.DataFrame({'date(yyyy/M/d H:mm)':finaldtime,'latitude':latitude,'longitude':longitude,'co2flux(umol m^2 s^1)':co2flux,'meanco2density(mmol m^3)':meanco2density,'varianceco2((mmol m^3)^2)':varianceco2density,'h2o(mmol m^3)':h2o,'h2ovariance((mmol m^3)^2)':h2ovariance,'temperature(degree)':temperature,'temperaturevariance':temperaturevariance,'pressure(kPa)':pressure,'horizontalwinddirection':horizontalwinddirection,'rotationtozero w(theta)':rotationtozerowtheta,'rotationtozero v(phi)':rotationtozerovphi,'sensibleheatflux(W m^2)':sensibleheatflux,'latentheatflux(W m^2)':latentheatflux, 'frictionvelocity(m s^1)':frictionvelocity})
                #df = df[df.warn_level > 13]
                df = df[['date(yyyy/M/d H:mm)','latitude','longitude','co2flux(umol m^2 s^1)','meanco2density(mmol m^3)','varianceco2((mmol m^3)^2)','h2o(mmol m^3)','temperature(degree)','temperaturevariance','pressure(kPa)','horizontalwinddirection','rotationtozero w(theta)','rotationtozero v(phi)','sensibleheatflux(W m^2)','latentheatflux(W m^2)','frictionvelocity(m s^1)']]
                df.to_csv(outputFolderPath+fWithoutExt+ '.csv', sep='\t')

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
   transferData()

#python ex2.py -i "/data/s1/saisree1/data-arm/nsa/200198nsa/" --ofolder "/data/s1/saisree1/data-arm/nsa/200198nsa/result/"

                


