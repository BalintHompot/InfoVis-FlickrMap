#!/usr/bin/env python

import sys
import json

arg=sys.argv
f1 = open("demo_df.csv",'r')

d={}
for row in f1:
	r = row.strip().split(";")
	tags = r[3].split(" ")
	if r[1] not in d:
		d[r[1]] = {}
	if r[2] not in d[r[1]]:
		d[r[1]][r[2]] = {}
	for each in tags:
		if each in d[r[1]][r[2]]:
			d[r[1]][r[2]][each] += 1
		else:
			d[r[1]][r[2]][each] = 1
#print(d)
print(max(d[r[1]][r[2]], key=d[r[1]][r[2]].get))

with open('result.json', 'w') as fp:
    json.dump(d, fp)
