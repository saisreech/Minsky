import netCDF4
import pandas as pd
import csv
import numpy as np
import datetime 
precip_nc_file = 'sgp30co2flx4mC1.b1.20150719.000000.cdf'
nc = netCDF4.Dataset(precip_nc_file, mode='r')
nc.variables.keys()
#warn_level=nc.variables['warn_level'][:]
#if warn_level[:] > 13:
#time_var = nc.variables['yyyydddhhmmss'][:]
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
#print warn_level
df = pd.DataFrame({'time':finaldtime,'day':day,'latitude':latitude,'longitude':longitude,'co2flux(umol m^2 s^1)':co2flux,'meanco2density(mmol m^3)':meanco2density,'varianceco2((mmol m^3)^2)':varianceco2density,'h2o(mmol m^3)':h2o,'h2ovariance((mmol m^3)^2)':h2ovariance,'temperature(degree)':temperature,'temperaturevariance':temperaturevariance,'pressure(kPa)':pressure,'horizontalwinddirection':horizontalwinddirection,'rotationtozero w(theta)':rotationtozerowtheta,'rotationtozero v(phi)':rotationtozerovphi,'sensibleheatflux(W m^2)':sensibleheatflux,'latentheatflux(W m^2)':latentheatflux, 'frictionvelocity(m s^1)':frictionvelocity})
#df = df[df.warn_level > 13]
df = df[['time','day','latitude','longitude','co2flux(umol m^2 s^1)','meanco2density(mmol m^3)','varianceco2((mmol m^3)^2)','h2o(mmol m^3)','temperature(degree)','temperaturevariance','pressure(kPa)','horizontalwinddirection','rotationtozero w(theta)','rotationtozero v(phi)','sensibleheatflux(W m^2)','latentheatflux(W m^2)','frictionvelocity(m s^1)']]
print df.head()
df.to_csv('testing.csv', sep='\t')
print latitude.min()
print longitude.min()
