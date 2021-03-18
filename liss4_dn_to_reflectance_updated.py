# -*- coding: utf-8 -*-
"""
Script converts R2A LISS-IV DNs to Radiance and then to Reflectance using 
Lλ = (DN*Lmax)/1024
Rsesnor = (pi*Lλ*d^2)/(ESUNi*COS(z)) where d = (1-0.01672*COS(RADIANS(0.9856*(Julian Day-4))))  
Created on Thu Mar  4 09:50:40 2021
Code Revision: 
    1). 18th March : Puneeth Changed B2_Lmax=52.0000, B3_Lmax=47.0000, B4_Lmax=31.5000. 
    
Scope for Improvement:
    1). To work for GeoRPC product types too. (File name slightly different.)

@author: Shubham
"""

import os
import gdal
from subprocess import Popen,PIPE
import pandas as pd
from astropy.time import Time
import datetime
import math
import matplotlib.pyplot as plt

#Main Directory
main_folder= "C:\\Users\\punee\\Downloads\\211284911\\211284911\\" #6 feb 2020
#"C:\\Users\\punee\\Downloads\\OneDrive_1_3-17-2021\\211088811\\211088811\\"#7jan2021 "D:\\LISS-4-data-new\\211089011\\"

str_expr='python {0} -A {1} --outfile={2} --calc={3} --type=Float32'


ip1='"'+main_folder+'BAND2.tif'+'"'
op1='"'+main_folder+'BAND2_SR.tif'+'"'
expr='(A*52.00)/1024'#see bandmeta for band specific Lmax values 
calc_path='C:\\ProgramData\\Anaconda3\\Lib\\site-packages\\GDAL-2.3.3-py3.7-win-amd64.egg-info\\scripts\\gdal_calc.py'#'C:\\ProgramData\\Anaconda3\\envs\\raster\\Lib\\site-packages\\GDAL-3.1.4-py3.7-win-amd64.egg-info\\scripts\\gdal_calc.py'

calculation =str_expr.format(calc_path,ip1,op1,expr)
process = Popen(calculation,stdout=PIPE,stderr=PIPE)
stdout, stderr = process.communicate()
print(stdout, stderr)



ip2='"'+main_folder+'BAND3.tif'+'"'
op2='"'+main_folder+'BAND3_SR.tif'+'"'
expr='(A*47.00)/1024'

calculation =str_expr.format(calc_path,ip2,op2,expr)
process = Popen(calculation,stdout=PIPE,stderr=PIPE)
stdout, stderr = process.communicate()
print(stdout, stderr)


ip3='"'+main_folder+'BAND4.tif'+'"'
op3='"'+main_folder+'BAND4_SR.tif'+'"'
expr='(A*31.5000)/1024'

calculation =str_expr.format(calc_path,ip3,op3,expr)
process = Popen(calculation,stdout=PIPE,stderr=PIPE)
stdout, stderr = process.communicate()
print(stdout, stderr)


meta=pd.read_csv(main_folder+'BAND_META.txt',sep='([^\=]+$)')#,sep='([^\=]+$)')




datenum = datetime.datetime.strptime(meta.iloc[94,1], "%d-%b-%Y %H:%M:%S.%f")
datestr=datenum.strftime("%Y-%m-%d %H:%M:%S.%f")


julian_day= Time(datestr, format='iso', scale='utc').jd
#Computation of distance between earth and Sun for the perticular acqusition date
dist=1-0.01672*math.cos(math.radians(0.9856*(julian_day-4)))


zen_ang=str(90-float(meta.iloc[65,1]))


#Band 2
rexpr='(3.14159*A*{}*{})/(185.33*cos(radians({})))'.format(dist,dist,zen_ang)


ip4='"'+main_folder+'BAND2_SR.tif'+'"'
op4='"'+main_folder+'BAND2_refl.tif'+'"'

calculation =str_expr.format(calc_path,ip4,op4,rexpr)
process = Popen(calculation,stdout=PIPE,stderr=PIPE)
stdout, stderr = process.communicate()
print(stdout, stderr)


#Band 3
rexpr='(3.14159*A*{}*{})/(157.77*cos(radians({})))'.format(dist,dist,zen_ang)


ip5='"'+main_folder+'BAND3_SR.tif'+'"'
op5='"'+main_folder+'BAND3_refl.tif'+'"'

calculation =str_expr.format(calc_path,ip5,op5,rexpr)
process = Popen(calculation,stdout=PIPE,stderr=PIPE)
stdout, stderr = process.communicate()
print(stdout, stderr)

rexpr='(3.14159*A*{}*{})/(111.36*cos(radians({})))'.format(dist,dist,zen_ang)


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







