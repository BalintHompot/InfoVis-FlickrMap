#!/usr/bin/env python

import sys
import json

arg=sys.argv
f1 = open("image_info_geo_2.csv",'r')

d={}
for row in f1:
	r = row.strip().split(";")
	tags = r[10].split(" ")
	if r[6] not in d:
		d[r[6]] = {}
	if r[1] not in d[r[6]]:
		d[r[6]][r[1]] = {}
	for each in tags:
		if each in d[r[6]][r[1]]:
			d[r[6]][r[1]][each] += 1
		else:
			d[r[6]][r[1]][each] = 1

print(max(d[r[6]][r[1]], key=d[r[6]][r[1]].get))

with open('result_fullset.json', 'w') as fp:
    json.dump(d, fp, indent=4)
