#!/usr/bin/env python

import sys
import json
from heapq import nlargest

arg=sys.argv
f1 = open("image_info_geo_2.csv",'r')
next(f1)
d={}
for row in f1:
	r = row.strip().split(";")
	tags = r[10].split(" ")
	if r[1] not in d:
		d[r[1]] = {}
	if r[6] not in d[r[1]]:
		d[r[1]][r[6]] = {}
		d[r[1]][r[6]]["top5"] = {}
		d[r[1]][r[6]]["all"] = {}
	for each in tags:
		if each in d[r[1]][r[6]]["all"]:
			d[r[1]][r[6]]["all"][each] += 1
		else:
			d[r[1]][r[6]]["all"][each] = 1

#print(max(d[r[1]][r[6]], key=d[r[1]][r[6]].get))
for k in d:
	for k2 in d[k]:
		five_largest = nlargest(5, d[k][k2]["all"], key=d[k][k2]["all"].get)
		for each in five_largest:
			d[k][k2]["top5"][each] = d[k][k2]["all"].get(each)
#			print((d[r[1]][r[6]]["all"][each], key=d[r[1]][r[6]]["all"][each]), d[r[1]][r[6]]["all"].get(each,""))
#			print(each,d[r[1]][r[6]]["all"].get(each,""))
#		print(five_largest)
#five_largest = nlargest(5, d["DZA"]["2007_12"], key=d["DZA"]["2007_12"].get)
#print(five_largest)

with open('result3_fullset.json', 'w') as fp:
    json.dump(d, fp, indent=4)

