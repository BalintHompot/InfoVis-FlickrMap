#!/usr/bin/env python

import sys
import json
from heapq import nlargest

arg=sys.argv
f1 = open("image_info_geo_2.csv",'r')
next(f1)

ts = "timesteps"
cd = "country_data"
t5 = "most_popular_5"
at = "all_tags"
bu = "buckets_temp"
buck = "buckets"
d={}
d["allTags"] = {}
d[ts] = {}
l = []

for row in f1:
	r = row.strip().split(";")
	tags = r[10].split(" ")
	if r[1] not in d[ts]:
		d[ts][r[1]] = {}
		d[ts][r[1]][cd] = {}
		d[ts][r[1]][cd][bu] = {}
		d[ts][r[1]][cd][buck] = {}
	if r[6] not in d[ts][r[1]][cd][bu]:
		d[ts][r[1]][cd][bu][r[6]] = {}
		d[ts][r[1]][cd][bu][r[6]][t5] = {}
		d[ts][r[1]][cd][bu][r[6]][at] = {}
	for each in tags:
		l.append(each)
		if each in d[ts][r[1]][cd][bu][r[6]][at]:
			d[ts][r[1]][cd][bu][r[6]][at][each] += 1
		else:
			d[ts][r[1]][cd][bu][r[6]][at][each] = 1
 
s = set(l)
l = list(l)
d["allTags"] = l
#print(max(d[r[1]][r[6]], key=d[r[1]][r[6]].get))
for k in d[ts]:
	bl = []
	bl.append(d[ts][k][cd][bu])
	d[ts][k][cd][buck] = bl
	for k2 in d[ts][k][cd][bu]:
		five_largest = nlargest(5, d[ts][k][cd][bu][k2][at], key=d[ts][k][cd][bu][k2][at].get)
		for each in five_largest:
			d[ts][k][cd][bu][k2][t5][each] = d[ts][k][cd][bu][k2][at].get(each)
	del(d[ts][k][cd][bu])

with open('result4_fullset.json', 'w') as fp:
    json.dump(d, fp, indent=4)

