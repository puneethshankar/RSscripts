# -*- coding: utf-8 -*-

"""
Script converts Cartosat 3 DNs to Radiance and then to Reflectance using 
Lλ = (DN*Lmax)/(2^b) where b=no. of bits(radiometric resolution)
Rsesnor = (pi*Lλ*d^2)/(ESUNi*COS(z)) where d = (1-0.01672*COS(RADIANS(0.9856*(Julian Day-4))))  
Created on Thu Mar  4 09:50:40 2021
Code Revision: 
    1). 23rd July : Puneeth Changed header
    
Scope for Improvement:
    1). Auto grab files within folder for batch processing
@author: Sai Venkat 
"""

import os
import gdal
from subprocess import Popen,PIPE
import pandas as pd
from astropy.time import Time
import datetime
import math
import matplotlib.pyplot as plt



# I. DN to RADIANCE

#Main Directory
main_folder= "C:\\xyz\\Cartosat3_sample_data\\" #6 feb 2020

str_expr='python {0} -A {1} --outfile={2} --calc={3} --type=Float32'
calc_path='C:\\Users\\...\\Anaconda3\\Lib\\site-packages\\GDAL-3.0.2-py3.8-win-amd64.egg-info\\scripts\\gdal_calc.py'


# DN to Radiance B1
ip1='"'+main_folder+'BAND1.tif'+'"'
op1='"'+main_folder+'BAND1_SR.tif'+'"'
#expr='(A*52.00)/1024' # for liss4
expr='(A*51.300)/2048'#for catosat-3 # see bandmeta for band specific Lmax values 
calculation =str_expr.format(calc_path,ip1,op1,expr)
process = Popen(calculation,stdout=PIPE,stderr=PIPE)
stdout, stderr = process.communicate()
print(stdout, stderr)


# DN to Radiance B2
ip1='"'+main_folder+'BAND2.tif'+'"'
op1='"'+main_folder+'BAND2_SR.tif'+'"'
#expr='(A*52.00)/1024' # for liss4
expr='(A*30.200)/2048'#for catosat-3 # see bandmeta for band specific Lmax values 
calculation =str_expr.format(calc_path,ip1,op1,expr)
process = Popen(calculation,stdout=PIPE,stderr=PIPE)
stdout, stderr = process.communicate()
print(stdout, stderr)


# DN to Radiance B3
ip2='"'+main_folder+'BAND3.tif'+'"'
op2='"'+main_folder+'BAND3_SR.tif'+'"'
#expr=  '(A*47.00)/1024' #'(A*47.00)/1024' for liss4
expr=  '(A*36.700)/2048'
calculation =str_expr.format(calc_path,ip2,op2,expr)
process = Popen(calculation,stdout=PIPE,stderr=PIPE)
stdout, stderr = process.communicate()
print(stdout, stderr)

# DN to Radiance B4
ip3='"'+main_folder+'BAND4.tif'+'"'
op3='"'+main_folder+'BAND4_SR.tif'+'"'
expr='(A*46.200)/2048'
calculation =str_expr.format(calc_path,ip3,op3,expr)
process = Popen(calculation,stdout=PIPE,stderr=PIPE)
stdout, stderr = process.communicate()
print(stdout, stderr)




# II. Radiance to Reflectance at sensor

#meta=pd.read_csv(main_folder+'BAND_META.txt',sep='([^\=]+$)')#,sep='([^\=]+$)')
meta=pd.read_csv(main_folder+'BAND_META.txt', sep='=') #,sep='([^\=]+$)')#,sep='([^\=]+$)')

datenum = datetime.datetime.strptime(meta.iloc[108,1], "%d-%b-%Y %H:%M:%S")
datestr=datenum.strftime("%Y-%m-%d %H:%M:%S.%f")

julian_day= Time(datestr, format='iso', scale='utc').jd
#Computation of distance between earth and Sun for the perticular acqusition date
dist=1-0.01672*math.cos(math.radians(0.9856*(julian_day-4)))

# Solar zenith angle
# https://www.programmersought.com/article/32775060816/
# h+z+90=360, here h=sun elevation angle i.e.,47.32590 or meta.iloc[61,1]
zen_ang=str(90-float(meta.iloc[61,1])) # changed from zen_ang=str(90-float(meta.iloc[61,1]))



#Band 1 # Radiance to Reflectance at sensor
rexpr='(3.14159*A*{}*{})/(196.78*cos(radians({})))'.format(dist,dist,zen_ang)
ip4='"'+main_folder+'BAND2_SR.tif'+'"'
op4='"'+main_folder+'BAND2_refl.tif'+'"'
calculation =str_expr.format(calc_path,ip4,op4,rexpr)
process = Popen(calculation,stdout=PIPE,stderr=PIPE)
stdout, stderr = process.communicate()
print(stdout, stderr)


#Band 2 # Radiance to Reflectance at sensor
rexpr='(3.14159*A*{}*{})/(182.01*cos(radians({})))'.format(dist,dist,zen_ang)
ip4='"'+main_folder+'BAND2_SR.tif'+'"'
op4='"'+main_folder+'BAND2_refl.tif'+'"'
calculation =str_expr.format(calc_path,ip4,op4,rexpr)
process = Popen(calculation,stdout=PIPE,stderr=PIPE)
stdout, stderr = process.communicate()
print(stdout, stderr)


#Band 3 # Radiance to Reflectance at sensor
rexpr='(3.14159*A*{}*{})/(157.54*cos(radians({})))'.format(dist,dist,zen_ang)
ip5='"'+main_folder+'BAND3_SR.tif'+'"'
op5='"'+main_folder+'BAND3_refl.tif'+'"'
calculation =str_expr.format(calc_path,ip5,op5,rexpr)
process = Popen(calculation,stdout=PIPE,stderr=PIPE)
stdout, stderr = process.communicate()
print(stdout, stderr)



#Band 4 # Radiance to Reflectance at sensor

rexpr='(3.14159*A*{}*{})/(110.86*cos(radians({})))'.format(dist,dist,zen_ang)
ip6='"'+main_folder+'BAND4_SR.tif'+'"'
op6='"'+main_folder+'BAND4_refl.tif'+'"'
calculation =str_expr.format(calc_path,ip6,op6,rexpr)
process = Popen(calculation,stdout=PIPE,stderr=PIPE)
stdout, stderr = process.communicate()
print(stdout, stderr)


#Remove spectral radiance
os.remove(main_folder+'BAND2_SR.tif')
os.remove(main_folder+'BAND3_SR.tif')
os.remove(main_folder+'BAND4_SR.tif')
