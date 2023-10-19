#!/usr/bin/env python

import json
import math

with open("points.json") as file:
    data = json.load(file)

grades = {
    2 : 0.5,
    3 : 0.6,
    4 : 0.75,
    5 : 0.85
}

percent = 0

for k in data.keys():
    if "point" in data[k]:
        if "min" in data[k] and data[k]['min']*data[k]['max'] > data[k]['point']:
            print("Minimum point is not reached (", k ,")!")
        percent += (data[k]['point'] / data[k]['max']) * 0.33

for i in grades.keys():
    need = math.ceil(((grades[i] - percent) / 0.33) * data["zh"]["max"])
    result = ""
    if need < 0:
        result = "Dope"
    elif need > data["zh"]["max"]:
        result = "Nope"
    elif need < data["zh"]["min"] * data["zh"]["max"]:
        result = str(int(data["zh"]["min"] * data["zh"]["max"]))
    else:
        result = str(need)

    print(f"{i}: {result}")