#!/usr/bin/env python

import sys
import json
from heapq import nlargest
import random

arg=sys.argv
f1 = open("image_info_all_7.csv",'r')
next(f1)

ts = "timesteps"
cd = "country_data"
t5 = "most_popular_5"
at = "all_tags"
cs = "categories_sum"
ca = "categories"
dd = "device_data"
c = "camera"
m = "phone"
o = "unknown"
uf = "user_freq"
bu = "buckets_temp"
buck = "buckets"
mpc = "most_popular_category"
d={}
d["allTags"] = {}
d[ts] = {}
l = []
ca_rand = ["nature","sport","country","people"]
for row in f1:
	r = row.strip().split(";")
	tags = r[7].split(" ")
	if r[2] not in d[ts]:
		d[ts][r[2]] = {}
		d[ts][r[2]][cd] = {}
		d[ts][r[2]][cd][bu] = {}
		d[ts][r[2]][cd][buck] = {}
	if r[5] not in d[ts][r[2]][cd][bu]:
		d[ts][r[2]][cd][bu][r[5]] = {}
		d[ts][r[2]][cd][bu][r[5]]["key"] = r[5]
		d[ts][r[2]][cd][bu][r[5]][t5] = {}
		d[ts][r[2]][cd][bu][r[5]][at] = {}
		d[ts][r[2]][cd][bu][r[5]][cs] = {}
		d[ts][r[2]][cd][bu][r[5]][cs]["nature"] = 0
		d[ts][r[2]][cd][bu][r[5]][cs]["sport"] = 0
		d[ts][r[2]][cd][bu][r[5]][cs]["country"] = 0
		d[ts][r[2]][cd][bu][r[5]][cs]["people"] = 0
		d[ts][r[2]][cd][bu][r[5]][ca] = {}		
		d[ts][r[2]][cd][bu][r[5]][uf] = 0
		d[ts][r[2]][cd][bu][r[5]][mpc] = {}
		d[ts][r[2]][cd][bu][r[5]][dd] = {}
		d[ts][r[2]][cd][bu][r[5]][dd][c] = {}
		d[ts][r[2]][cd][bu][r[5]][dd][m] = {}
		d[ts][r[2]][cd][bu][r[5]][dd][o] = {}
	if r[4] not in d[ts][r[2]][cd][bu][r[5]][dd][r[6].lower()]:
		d[ts][r[2]][cd][bu][r[5]][dd][r[6].lower()][r[4]] = 0
	if r[4] in d[ts][r[2]][cd][bu][r[5]][dd][r[6].lower()]:
		d[ts][r[2]][cd][bu][r[5]][dd][r[6].lower()][r[4]] += 1
	cat = random.choice(ca_rand)
	if cat not in d[ts][r[2]][cd][bu][r[5]][ca]:
		d[ts][r[2]][cd][bu][r[5]][ca][cat] = {}
	for each in tags:
#		l.append(each) 
		if each in d[ts][r[2]][cd][bu][r[5]][ca][cat]:
			d[ts][r[2]][cd][bu][r[5]][ca][cat][each] += 1
		else:
			d[ts][r[2]][cd][bu][r[5]][ca][cat][each] = 1
	d[ts][r[2]][cd][bu][r[5]][cs][cat] += 1
	d[ts][r[2]][cd][bu][r[5]][uf] += 1
#s = set(l)
#l = list(l)
#d["allTags"] = l
d["allCategories"] = ca_rand
for k in d[ts]:
	for k2 in d[ts][k][cd][bu]:
		five_largest = nlargest(5, d[ts][k][cd][bu][k2][at], key=d[ts][k][cd][bu][k2][at].get)
		largest_cat = nlargest(1, d[ts][k][cd][bu][k2][cs], key=d[ts][k][cd][bu][k2][cs].get)
		for largest in largest_cat:
			d[ts][k][cd][bu][k2][mpc] = largest
		for each in five_largest:
			d[ts][k][cd][bu][k2][t5][each] = d[ts][k][cd][bu][k2][at].get(each)
	bl = []
	for country in d[ts][k][cd][bu]:
		bl.append(d[ts][k][cd][bu][country])
		d[ts][k][cd][buck] = bl
	del(d[ts][k][cd][bu])


with open('result7_fullset.json', 'w') as fp:
    json.dump(d, fp, indent=4)

