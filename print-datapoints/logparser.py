#!/usr/bin/env python3

import re

batch_measurements = {
    '######## batch mid-points:': 'b-midpoints',
    '######## batch intervals:': 'b-interval',
    '######## batch latencies:': 'b-avg',
    '######## batch get latencies:': 'b-GET',
    '######## batch update latencies:' :'b-UPDATE',
}

measurements = {
    '######## update stats:': 'UPDATE',
    '######## get stats:': 'GET',
}


tiles = ['0.1', '25', '50', '75', '90', '95', '99', '99.9']

def parse(path):
    out = {}
    with open(path) as f:
        measurement = ""
        for line in f:
            l = line.lower()
            if l[:-1] == '################ batch stats:':
                break
            elif l[:-1] == '################ main stats:':
                break
        if l[:-1] == '################ batch stats:':
            for line in f:
                l = line.lower()
                if l[:-1] == '################ main stats:':
                    break
                elif l[:-1] in batch_measurements:
                    measurement = batch_measurements[l[:-1]]
                    assert(measurement not in out)
                    if(measurement == "b-midpoints"):
                        out[measurement] = []
                    else:
                        out[measurement + '-sums'] = []
                        out[measurement + '-counts'] = []

                elif 'ns' in l:
                    if 'ops' in l:
                        data = re.findall("^(\d+)ns / (\d+)ops\n?$", l)
                        for x in data:
                            out[measurement + "-sums"].append(float(x[0]))
                            out[measurement + "-counts"].append(int(x[1]))
                    else:
                        data = re.findall("^(\d+)ns\n?$", l)
                        for x in data:
                            value = float(x)
                            out[measurement].append(value)
        measurement = ""        
        for line in f:
            l = line.lower()
            if l[:-1] in measurements:
                measurement = measurements[l[:-1]]
                assert(measurement not in out)
                out[measurement] = {}
                out[measurement]['pcount'] = 0
                out[measurement]['psum'] = 0
            elif "local tput" in l:
                measurement = ""
                assert("local tput" not in out)
                # data = re.findall("local tput: (\d+)kops", l)
                data = re.findall("local tput: (\d+)kpos", l)
                assert len(data) == 1, l
                out["local tput"] = int(data[0])
            elif "aggregated tput" in l:
                measurement = ""
                assert("aggregated tput" not in out)
                data = re.findall("aggregated tput: (\d+)kops", l)
                assert(len(data) == 1)
                out["aggregated tput"] = int(data[0])
            elif measurement != "":
                if l.startswith("average"):
                    assert("avg" not in out[measurement])
                    data = re.findall("average latency: (\d+)ns", l)
                    assert(len(data) == 1)
                    out[measurement]["avg"] = int(data[0]) / 1000
                elif "%:" in l:
                    data = re.findall("([0-9\.]+)%: (\d+)ns[\.,]", l)
                    # print(data)
                    # assert(len(data) == 4)
                    for x in data:
                        perc = float(x[0])
                        assert(perc not in out[measurement])
                        out[measurement][perc] = int(x[1]) / 1000
                        if(perc > 0.5):
                            out[measurement]['pcount'] += 1
                            out[measurement]['psum'] += int(x[1]) / 1000
    return out
