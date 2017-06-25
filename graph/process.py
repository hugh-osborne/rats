import csv
import numpy as np
from itertools import groupby
import matplotlib.pyplot as plt

division_dim = 25
division_size = 1.0/division_dim
rate_minimum = 0.2

def loadSpikes(filename) :
    spikes = []
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            spikes.append(float(row[0]))
    return spikes

def smoothUnitSpikes(spikes, sd_threshold) :
    var = np.var(spikes)
    sd = np.square(var)
    return [1 if s > sd*sd_threshold else 0 for s in spikes]

def compareUnitSpikes(spikes) :
    series = range(0,len(spikes))
    times = range(0,len(spikes[0]))
    ordering = [[s for s in series if spikes[s][t] == 1] for t in times ]
    ordering = [x for x in ordering if len(x) > 0]
    return [x[0] for x in groupby(ordering)]

def compareFields(field1, field2) :
    spikes1 = field1[8:(division_dim*division_dim)+8]
    spikes2 = field2[8:(division_dim*division_dim)+8]
    return np.linalg.norm(np.subtract(spikes2,spikes1))

def getPlaceField(placefields, day, run, unit) :
    for f in placefields :
        if f[1] == day and f[2] == run and f[3] == unit :
            return f

def loadPlaceFieldsFromFile(filename) :
    placefields = []
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0] == 'track':
                continue

            track = row[0]
            day = int(row[1])
            run = int(row[2])
            unit = row[3]

            if track == 'sleep':
                continue

            rates = [float(s) if float(s) > rate_minimum else 0.0 for s in row[4:(division_dim * division_dim) + 4]]
            spike_rates = np.array(rates)
            spike_rates = spike_rates.reshape(division_dim, division_dim)
            x_dims = (np.nonzero(spike_rates))[0]
            y_dims = (np.nonzero(spike_rates))[1]

            if x_dims.any() and y_dims.any():
                min_x_dim = np.ndarray.min(x_dims) * division_size
                max_x_dim = np.ndarray.max(x_dims) * division_size
                min_y_dim = np.ndarray.min(y_dims) * division_size
                max_y_dim = np.ndarray.max(y_dims) * division_size
                placefields.append([track, day, run, unit, min_x_dim, max_x_dim, min_y_dim, max_y_dim] + rates)
    return placefields

def pickSmallFields(fields, size) :
    return [f for f in fields if f[5] - f[4] < size or f[7] - f[6] < size]

placefields = loadPlaceFieldsFromFile('../rats/rats/bon/bon_4/placefields.txt')
print(placefields)
areas = [(f[5]-f[4])*(f[7]-f[6]) for f in pickSmallFields(placefields, 0.4)]
pf_area_mean = np.mean(areas)
pf_area_var = np.var(areas)
print( [pf_area_mean, pf_area_var])

diff1 = compareFields(getPlaceField(placefields,4,2,'11_1'),getPlaceField(placefields,4,4,'11_1'))
diff2 = compareFields(getPlaceField(placefields,4,2,'11_1'),getPlaceField(placefields,4,4,'1_10'))
print([diff1,diff2])

placecell1 = loadSpikes('../rats/rats/bon/bon_4/bon_4_4_run/smoothed/unit_11_1.txt')
placecell2 = loadSpikes('../rats/rats/bon/bon_4/bon_4_4_run/smoothed/unit_13_1.txt')
pc_var = np.var(placecell1)
print(pc_var)

unit_spikes1 = smoothUnitSpikes(placecell1, 3)
unit_spikes2 = smoothUnitSpikes(placecell2, 3)
print(unit_spikes1)
print(unit_spikes2)

overlaps = compareUnitSpikes([unit_spikes1,unit_spikes2])
print(overlaps)

