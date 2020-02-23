# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 12:31:59 2020

@author: PathwaysData_1
"""

s = 'sunny'
o = 'overcast'
r = 'rain'
h = 'hot'
m = 'mild'
c = 'cool'
hi = 'high'
n = 'normal'
w = 'weak'
st = 'strong'

outlook = [s,s,o,r,r,r,o,s,s,r,s,o,o,r]
temp = [h,h,h,m,c,c,c,m,c,m,m,m,h,m]
humidity = [hi,hi,hi,hi,n,n,n,hi,n,n,n,hi,n,hi]
wind = [w,st,w,w,w,st,st,w,w,w,st,st,w,st]
play_gulf = [0,0,1,1,1,0,1,0,1,1,1,1,1,0]

n_attr_outlook = 3
n_attr_temp = 3
n_attr_hum = 2
n_attr_wind = 2

nyes = len([x for x in play_gulf if x==1])
nno = len([x for x in play_gulf if x==0])
total = len(play_gulf)

infoP = -(nyes/total)