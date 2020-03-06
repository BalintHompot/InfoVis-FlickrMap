#!/usr/bin/env python

import sys
import json
from heapq import nlargest
import random

arg=sys.argv
f1 = open("image_info_geo_3.csv",'r')
#next(f1)

ts = "timesteps"
cd = "country_data"
t5 = "most_popular_5"
at = "all_tags"
ca = "category"
dd = "device_data"
c = "camera"
m = "phone"
o = "Unknown"
uf = "user_freq"
bu = "buckets_temp"
buck = "buckets"
d={}
d["allTags"] = {}
d[ts] = {}
l = []
ca_rand = ["nature","sport","country","people"]
for row in f1:
	r = row.strip().split(";")
	tags = r[12].split(" ")
	if r[1] not in d[ts]:
		d[ts][r[1]] = {}
		d[ts][r[1]][cd] = {}
		d[ts][r[1]][cd][bu] = {}
		d[ts][r[1]][cd][buck] = {}
	if r[8] not in d[ts][r[1]][cd][bu]:
		d[ts][r[1]][cd][bu][r[8]] = {}
		d[ts][r[1]][cd][bu][r[8]]["key"] = r[8]
		d[ts][r[1]][cd][bu][r[8]][t5] = {}
		d[ts][r[1]][cd][bu][r[8]][at] = {}
		d[ts][r[1]][cd][bu][r[8]][ca] = {}
		d[ts][r[1]][cd][bu][r[8]][ca]["nature"] = 0
		d[ts][r[1]][cd][bu][r[8]][ca]["sport"] = 0
		d[ts][r[1]][cd][bu][r[8]][ca]["country"] = 0
		d[ts][r[1]][cd][bu][r[8]][ca]["people"] = 0		
		d[ts][r[1]][cd][bu][r[8]][uf] = 0
		d[ts][r[1]][cd][bu][r[8]][dd] = {}
		d[ts][r[1]][cd][bu][r[8]][dd][c] = {}
		d[ts][r[1]][cd][bu][r[8]][dd][m] = {}
		d[ts][r[1]][cd][bu][r[8]][dd][o] = {}
	if r[10] not in d[ts][r[1]][cd][bu][r[8]][dd][r[11]]:
		d[ts][r[1]][cd][bu][r[8]][dd][r[11]][r[10]] = 0
	if r[10] in d[ts][r[1]][cd][bu][r[8]][dd][r[11]]:
		d[ts][r[1]][cd][bu][r[8]][dd][r[11]][r[10]] += 1	
	for each in tags:
		l.append(each)
		if each in d[ts][r[1]][cd][bu][r[8]][at]:
			d[ts][r[1]][cd][bu][r[8]][at][each] += 1
		else:
			d[ts][r[1]][cd][bu][r[8]][at][each] = 1
	d[ts][r[1]][cd][bu][r[8]][ca][random.choice(ca_rand)] += 1
	d[ts][r[1]][cd][bu][r[8]][uf] += 1
s = set(l)
l = list(l)
d["allTags"] = l

for k in d[ts]:
	for k2 in d[ts][k][cd][bu]:
		five_largest = nlargest(5, d[ts][k][cd][bu][k2][at], key=d[ts][k][cd][bu][k2][at].get)
		for each in five_largest:
			d[ts][k][cd][bu][k2][t5][each] = d[ts][k][cd][bu][k2][at].get(each)
	bl = []
	for country in d[ts][k][cd][bu]:
		bl.append(d[ts][k][cd][bu][country])
		d[ts][k][cd][buck] = bl
	del(d[ts][k][cd][bu])

with open('result6_fullset.json', 'w') as fp:
    json.dump(d, fp, indent=4)

