#!/usr/bin/env python

import sys
import json
from heapq import nlargest

arg=sys.argv
f1 = open("image_info_all_9.csv",'r')
next(f1)

# dictionary key names
ts = "timesteps"
cd = "country_data"
t5 = "top_5"
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
ca_rand = ["animal","citylife","nature","people","sports","unknown"]

# create dictionary
d={}
d[ts] = {}
d["allCategories"] = ca_rand

# go true the input file and make embedded dictionaries with the right structure for the json output.
for row in f1:
	r = row.strip().split(";")
	tags = r[4].split(" ")
	timestep = r[3]
	country = r[6]
	maker = r[5]
	device = r[7].lower()
	category = r[10]
	if timestep not in d[ts]:
		d[ts][timestep] = {}
		d[ts][timestep][cd] = {}
		d[ts][timestep][cd][bu] = {}
		d[ts][timestep][cd][buck] = {}
	if country not in d[ts][timestep][cd][bu]:
		d[ts][timestep][cd][bu][country] = {}
		d[ts][timestep][cd][bu][country]["key"] = country
		d[ts][timestep][cd][bu][country][cs] = {}
		d[ts][timestep][cd][bu][country][ca] = {}		
		d[ts][timestep][cd][bu][country][uf] = 0
		d[ts][timestep][cd][bu][country][mpc] = {}
		d[ts][timestep][cd][bu][country][dd] = {}
		d[ts][timestep][cd][bu][country][dd][c] = {}
		d[ts][timestep][cd][bu][country][dd][m] = {}
		d[ts][timestep][cd][bu][country][dd][o] = {}
		for group in ca_rand:
			d[ts][timestep][cd][bu][country][cs][group] = 0		
	if maker in d[ts][timestep][cd][bu][country][dd][device]:
		d[ts][timestep][cd][bu][country][dd][device][maker] += 1
	if maker not in d[ts][timestep][cd][bu][country][dd][device]:
		d[ts][timestep][cd][bu][country][dd][device][maker] = 0
	if category not in d[ts][timestep][cd][bu][country][ca]:
		d[ts][timestep][cd][bu][country][ca][category] = {}
		d[ts][timestep][cd][bu][country][ca][category][at] = {}
		d[ts][timestep][cd][bu][country][ca][category][t5] = {}
	for each in tags:
		if each in d[ts][timestep][cd][bu][country][ca][category][at]:
			d[ts][timestep][cd][bu][country][ca][category][at][each] += 1
		else:
			d[ts][timestep][cd][bu][country][ca][category][at][each] = 1
	d[ts][timestep][cd][bu][country][cs][category] += 1
	d[ts][timestep][cd][bu][country][uf] += 1

# get the most used category and the top 5 tags from each category
for k in d[ts]:
	for k2 in d[ts][k][cd][bu]:
		largest_cat = nlargest(1, d[ts][k][cd][bu][k2][cs], key=d[ts][k][cd][bu][k2][cs].get)
		for largest in largest_cat:
			d[ts][k][cd][bu][k2][mpc] = largest
		for k3 in d[ts][k][cd][bu][k2][ca]:
			five_largest = nlargest(5, d[ts][k][cd][bu][k2][ca][k3][at], key=d[ts][k][cd][bu][k2][ca][k3][at].get)
			for each in five_largest:
				d[ts][k][cd][bu][k2][ca][k3][t5][each] = d[ts][k][cd][bu][k2][ca][k3][at].get(each)
	bl = []
	for country in d[ts][k][cd][bu]:
		bl.append(d[ts][k][cd][bu][country])
		d[ts][k][cd][buck] = bl
	del(d[ts][k][cd][bu])

# convert the dictonary to json
with open('result9_fullset.json', 'w') as fp:
    json.dump(d, fp, indent=4)

