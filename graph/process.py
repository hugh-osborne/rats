import csv
import numpy as np
from itertools import groupby
import matplotlib.pyplot as plt
import matplotlib.patches as pch
from os import listdir

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

def displayAddFields(fields, track_name, size_type) :
    rates = np.zeros(division_dim*division_dim)
    for f in fields :
        rates += np.array(f[8:(division_dim*division_dim)+8])
    rates = np.array([r if r < 1 else 1 for r in rates])
    rates = rates.reshape(division_dim, division_dim)
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)
    ax1.set_title('Heatmap of Normalised Place Cell Activity\nAcross the ' + track_name + ' ( ' + size_type + ' )\n')
    ax1.yaxis.set_visible(False)
    ax1.xaxis.set_visible(False)
    #plt.imshow(f, cmap='hot', interpolation='nearest')
    plt.pcolor(rates.transpose(),cmap=plt.cm.Reds)
    plt.colorbar()
    plt.show()

def displayCoverage() :
    placefields = loadPlaceFieldsFromFile('../rats/rats/bon/bon_4/placefields.txt')
    placefields = [p for p in placefields if p[1] == 4 and p[2] == 2]
    displayAddFields(pickSmallFields(placefields,1.0),'W Track', 'All PFs')
    placefields = loadPlaceFieldsFromFile('../rats/rats/bon/bon_4/placefields.txt')
    placefields = [p for p in placefields if p[1] == 4 and p[2] == 2]
    displayAddFields(pickSmallFields(placefields,0.4),'W Track', 'PFs < 0.4 of track')
    placefields = loadPlaceFieldsFromFile('../rats/rats/bon/bon_4/placefields.txt')
    placefields = [p for p in placefields if p[1] == 4 and p[2] == 6]
    displayAddFields(pickSmallFields(placefields,1.0),'W Track', 'All PFs')
    placefields = loadPlaceFieldsFromFile('../rats/rats/bon/bon_4/placefields.txt')
    placefields = [p for p in placefields if p[1] == 4 and p[2] == 6]
    displayAddFields(pickSmallFields(placefields,0.4),'W Track', 'PFs < 0.4 of track')
    placefields = loadPlaceFieldsFromFile('../rats/rats/i01_maze06_MS.002/placefields.txt')
    displayAddFields(pickSmallFields(placefields,1.0),'Figure 8 Track', 'All PFs')
    placefields = loadPlaceFieldsFromFile('../rats/rats/i01_maze06_MS.002/placefields.txt')
    displayAddFields(pickSmallFields(placefields,0.5),'Figure 8 Track', 'PFs < 0.4 of track')

def compareFields(field1, field2) :
    spikes1 = field1[8:(division_dim*division_dim)+8]
    spikes2 = field2[8:(division_dim*division_dim)+8]
    #return np.linalg.norm(np.subtract(spikes2,spikes1))
    coefs = np.corrcoef([spikes1,spikes2])
    return coefs[0][1]

def getPlaceFields(placefields, track, unit) :
    return [f for f in placefields if f[0] == track and f[3] == unit]

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

            if track == 'sleep' or track == 'unknown':
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

def displayPlaceField(field) :
    f = np.array(field[8:(division_dim*division_dim)+8])
    f = f.reshape(division_dim, division_dim)
    fig1 = plt.figure()
    #plt.imshow(f, cmap='hot', interpolation='nearest')
    plt.pcolor(f.transpose(),cmap=plt.cm.Reds)
    plt.colorbar()
    plt.show()

def getNumberOfCells(filename) :
    epochs = {}
    with open(filename) as csvfile:
        csvfile.readline() # skip line 1
        csvfile.readline() # skip line 2
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0]+row[1]+row[2] in epochs :
                epochs[row[0]+row[1]+row[2]] += 1
            else :
                epochs[row[0]+row[1]+row[2]] = 1

    return epochs.values()

def placeWTrackFieldAreaStats() :
    placefields = loadPlaceFieldsFromFile('../rats/rats/bon/bon_4/placefields.txt')
    placefields.extend(loadPlaceFieldsFromFile('../rats/rats/bon/bon_3/placefields.txt'))
    placefields.extend(loadPlaceFieldsFromFile('../rats/rats/bon/bon_5/placefields.txt'))
    placefields.extend(loadPlaceFieldsFromFile('../rats/rats/bon/bon_6/placefields.txt'))
    placefields.extend(loadPlaceFieldsFromFile('../rats/rats/bon/bon_7/placefields.txt'))
    placefields.extend(loadPlaceFieldsFromFile('../rats/rats/bon/bon_8/placefields.txt'))
    placefields.extend(loadPlaceFieldsFromFile('../rats/rats/bon/bon_9/placefields.txt'))
    placefields.extend(loadPlaceFieldsFromFile('../rats/rats/bon/bon_10/placefields.txt'))
    placefields.extend(loadPlaceFieldsFromFile('../rats/rats/Cor/Cor_1/placefields.txt'))
    placefields.extend(loadPlaceFieldsFromFile('../rats/rats/Cor/Cor_2/placefields.txt'))
    placefields.extend(loadPlaceFieldsFromFile('../rats/rats/Cor/Cor_3/placefields.txt'))
    placefields.extend(loadPlaceFieldsFromFile('../rats/rats/Cor/Cor_4/placefields.txt'))
    placefields.extend(loadPlaceFieldsFromFile('../rats/rats/Cor/Cor_5/placefields.txt'))
    placefields.extend(loadPlaceFieldsFromFile('../rats/rats/Cor/Cor_6/placefields.txt'))
    placefields.extend(loadPlaceFieldsFromFile('../rats/rats/Cor/Cor_7/placefields.txt'))
    placefields.extend(loadPlaceFieldsFromFile('../rats/rats/Cor/Cor_8/placefields.txt'))
    placefields.extend(loadPlaceFieldsFromFile('../rats/rats/Cor/Cor_9/placefields.txt'))
    placefields.extend(loadPlaceFieldsFromFile('../rats/rats/_con/_con_1/placefields.txt'))
    placefields.extend(loadPlaceFieldsFromFile('../rats/rats/_con/_con_2/placefields.txt'))
    placefields.extend(loadPlaceFieldsFromFile('../rats/rats/_con/_con_3/placefields.txt'))
    placefields.extend(loadPlaceFieldsFromFile('../rats/rats/_con/_con_4/placefields.txt'))
    placefields.extend(loadPlaceFieldsFromFile('../rats/rats/_con/_con_5/placefields.txt'))
    placefields.extend(loadPlaceFieldsFromFile('../rats/rats/_con/_con_6/placefields.txt'))
    areas = [(f[5]-f[4])*(f[7]-f[6]) for f in placefields]
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)
    ax1.set_title('Histogram of Place Field Area (W Track)')
    ax1.set_xlabel('place field size (proportion of the area of the track)')
    ax1.set_ylabel('frequency')
    ax1.hist(areas, 50, range=[0.0,1.0], histtype='bar',rwidth=0.9)
    plt.show()
    pf_area_mean = np.mean(areas)
    pf_area_var = np.std(areas)
    print( ['mean and variance:', pf_area_mean, pf_area_var])

def placeF8TrackFieldAreaStats() :
    placefields = loadPlaceFieldsFromFile('../rats/rats/figure8/placefields.txt')
    areas = [(f[5]-f[4])*(f[7]-f[6]) for f in placefields]
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)
    ax1.set_title('Histogram of Place Field Area (Figure 8 Track)')
    ax1.set_xlabel('place field size (proportion of the area of the track)')
    ax1.set_ylabel('frequency')
    ax1.hist(areas, 50, range=[0.0,1.0], histtype='bar',rwidth=0.9)
    plt.show()
    pf_area_mean = np.mean(areas)
    pf_area_var = np.std(areas)
    print( ['mean and variance:', pf_area_mean, pf_area_var])

def trackAllPlaceFieldShifts() :
    averages = np.zeros(7)
    counts = np.ones(7)
    with open('../rats/rats/bon/bon_3/process_input.txt') as csvfile:
        csvfile.readline() # skip line 1
        csvfile.readline() # skip line 2
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0] == 'TrackA' and row[2] == '6':
                print(['TrackA', row[3]])
                diffs = trackPlaceFieldShiftBon('TrackA', row[3])
                for i in range(0,len(diffs)) :
                    averages[i] += diffs[i]
                    counts[i] += 1
    with open('../rats/rats/Cor/Cor_1/process_input.txt') as csvfile:
        csvfile.readline() # skip line 1
        csvfile.readline() # skip line 2
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0] == 'TrackA' and row[2] == '4':
                print(['TrackA', row[3]])
                diffs = trackPlaceFieldShiftCor('TrackA', row[3])
                for i in range(0,len(diffs)) :
                    averages[i] += diffs[i]
                    counts[i] += 1
    with open('../rats/rats/Cor/Cor_1/process_input.txt') as csvfile:
        csvfile.readline() # skip line 1
        csvfile.readline() # skip line 2
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0] == 'TrackA' and row[2] == '2':
                print(['TrackA', row[3]])
                diffs = trackPlaceFieldShiftCor('TrackA', row[3])
                for i in range(0,len(diffs)) :
                    averages[i] += diffs[i]
                    counts[i] += 1
    with open('../rats/rats/_con/_con_1/process_input.txt') as csvfile:
        csvfile.readline() # skip line 1
        csvfile.readline() # skip line 2
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0] == 'TrackA' and row[2] == '2':
                print(['TrackA', row[3]])
                diffs = trackPlaceFieldShiftCon('TrackA', row[3])
                for i in range(0,len(diffs)) :
                    averages[i] += diffs[i]
                    counts[i] += 1
    with open('../rats/rats/_con/_con_1/process_input.txt') as csvfile:
        csvfile.readline() # skip line 1
        csvfile.readline() # skip line 2
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0] == 'TrackA' and row[2] == '4':
                print(['TrackA', row[3]])
                diffs = trackPlaceFieldShiftCon('TrackA', row[3])
                for i in range(0,len(diffs)) :
                    averages[i] += diffs[i]
                    counts[i] += 1

    for i in range(0,6) :
        averages[i] /= counts[i]
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)
    ax1.set_title('Average Correlation Coefficient between the \nFirst Epoch and Subsequent Epochs')
    ax1.set_xlabel('Epoch Order')
    ax1.set_ylabel('Correlation Coefficient')
    ax1.plot(averages)
    plt.show()

def trackPlaceFieldShiftBon(track, unit) :
    placefields = loadPlaceFieldsFromFile('../rats/rats/bon/bon_3/placefields.txt')
    placefields.extend(loadPlaceFieldsFromFile('../rats/rats/bon/bon_4/placefields.txt'))
    placefields.extend(loadPlaceFieldsFromFile('../rats/rats/bon/bon_5/placefields.txt'))
    placefields.extend(loadPlaceFieldsFromFile('../rats/rats/bon/bon_6/placefields.txt'))
    placefields.extend(loadPlaceFieldsFromFile('../rats/rats/bon/bon_7/placefields.txt'))
    placefields.extend(loadPlaceFieldsFromFile('../rats/rats/bon/bon_8/placefields.txt'))
    placefields.extend(loadPlaceFieldsFromFile('../rats/rats/bon/bon_9/placefields.txt'))
    placefields.extend(loadPlaceFieldsFromFile('../rats/rats/bon/bon_10/placefields.txt'))
    unit_placefields = getPlaceFields(placefields, track, unit)
    diffs = []
    test_unit = unit_placefields[0]
    for p in range(1,len(unit_placefields)) :
        diffs.append(compareFields(unit_placefields[p], test_unit))
    #print(diffs)
    return diffs

def trackPlaceFieldShiftCon(track, unit) :
    placefields = loadPlaceFieldsFromFile('../rats/rats/_con/_con_1/placefields.txt')
    placefields.extend(loadPlaceFieldsFromFile('../rats/rats/_con/_con_2/placefields.txt'))
    placefields.extend(loadPlaceFieldsFromFile('../rats/rats/_con/_con_3/placefields.txt'))
    placefields.extend(loadPlaceFieldsFromFile('../rats/rats/_con/_con_4/placefields.txt'))
    placefields.extend(loadPlaceFieldsFromFile('../rats/rats/_con/_con_5/placefields.txt'))
    placefields.extend(loadPlaceFieldsFromFile('../rats/rats/_con/_con_6/placefields.txt'))
    unit_placefields = getPlaceFields(placefields, track, unit)
    diffs = []
    test_unit = unit_placefields[0]
    for p in range(1,len(unit_placefields)) :
        diffs.append(compareFields(unit_placefields[p], test_unit))
    #print(diffs)
    return diffs

def trackPlaceFieldShiftCor(track, unit) :
    placefields = loadPlaceFieldsFromFile('../rats/rats/Cor/Cor_1/placefields.txt')
    placefields.extend(loadPlaceFieldsFromFile('../rats/rats/Cor/Cor_2/placefields.txt'))
    placefields.extend(loadPlaceFieldsFromFile('../rats/rats/Cor/Cor_3/placefields.txt'))
    placefields.extend(loadPlaceFieldsFromFile('../rats/rats/Cor/Cor_4/placefields.txt'))
    placefields.extend(loadPlaceFieldsFromFile('../rats/rats/Cor/Cor_5/placefields.txt'))
    placefields.extend(loadPlaceFieldsFromFile('../rats/rats/Cor/Cor_6/placefields.txt'))
    placefields.extend(loadPlaceFieldsFromFile('../rats/rats/Cor/Cor_7/placefields.txt'))
    placefields.extend(loadPlaceFieldsFromFile('../rats/rats/Cor/Cor_8/placefields.txt'))
    placefields.extend(loadPlaceFieldsFromFile('../rats/rats/Cor/Cor_9/placefields.txt'))
    unit_placefields = getPlaceFields(placefields, track, unit)
    diffs = []
    test_unit = unit_placefields[0]
    for p in range(1,len(unit_placefields)) :
        diffs.append(compareFields(unit_placefields[p], test_unit))
    #print(diffs)
    return diffs

#placeWTrackFieldAreaStats()
placeF8TrackFieldAreaStats()

trackAllPlaceFieldShifts()

placefields = loadPlaceFieldsFromFile('../rats/rats/bon/bon_4/placefields.txt')
placefields.extend(loadPlaceFieldsFromFile('../rats/rats/bon/bon_3/placefields.txt'))
placefields.extend(loadPlaceFieldsFromFile('../rats/rats/bon/bon_5/placefields.txt'))
placefields.extend(loadPlaceFieldsFromFile('../rats/rats/bon/bon_6/placefields.txt'))
placefields.extend(loadPlaceFieldsFromFile('../rats/rats/bon/bon_7/placefields.txt'))
placefields.extend(loadPlaceFieldsFromFile('../rats/rats/bon/bon_8/placefields.txt'))
placefields.extend(loadPlaceFieldsFromFile('../rats/rats/bon/bon_9/placefields.txt'))
placefields.extend(loadPlaceFieldsFromFile('../rats/rats/bon/bon_10/placefields.txt'))

#displayAddFields(getPlaceFields(placefields,'TrackB', '11_1'))
#displayCoverage()
unit_counts = getNumberOfCells('../rats/rats/bon/bon_3/process_input.txt')
unit_counts.extend(getNumberOfCells('../rats/rats/bon/bon_4/process_input.txt'))
unit_counts.extend(getNumberOfCells('../rats/rats/bon/bon_5/process_input.txt'))
unit_counts.extend(getNumberOfCells('../rats/rats/bon/bon_6/process_input.txt'))
unit_counts.extend(getNumberOfCells('../rats/rats/bon/bon_7/process_input.txt'))
unit_counts.extend(getNumberOfCells('../rats/rats/bon/bon_8/process_input.txt'))
unit_counts.extend(getNumberOfCells('../rats/rats/bon/bon_9/process_input.txt'))
unit_counts.extend(getNumberOfCells('../rats/rats/bon/bon_10/process_input.txt'))

print(np.mean(unit_counts))
print(max(unit_counts))
print(min(unit_counts))

unit_counts = getNumberOfCells('../rats/rats/Cor/Cor_1/process_input.txt')
unit_counts.extend(getNumberOfCells('../rats/rats/Cor/Cor_2/process_input.txt'))
unit_counts.extend(getNumberOfCells('../rats/rats/Cor/Cor_3/process_input.txt'))
unit_counts.extend(getNumberOfCells('../rats/rats/Cor/Cor_4/process_input.txt'))
unit_counts.extend(getNumberOfCells('../rats/rats/Cor/Cor_5/process_input.txt'))
unit_counts.extend(getNumberOfCells('../rats/rats/Cor/Cor_6/process_input.txt'))
unit_counts.extend(getNumberOfCells('../rats/rats/Cor/Cor_7/process_input.txt'))
unit_counts.extend(getNumberOfCells('../rats/rats/Cor/Cor_8/process_input.txt'))
unit_counts.extend(getNumberOfCells('../rats/rats/Cor/Cor_9/process_input.txt'))

print(np.mean(unit_counts))
print(max(unit_counts))
print(min(unit_counts))

unit_counts = getNumberOfCells('../rats/rats/_con/_con_1/process_input.txt')
unit_counts.extend(getNumberOfCells('../rats/rats/_con/_con_2/process_input.txt'))
unit_counts.extend(getNumberOfCells('../rats/rats/_con/_con_3/process_input.txt'))
unit_counts.extend(getNumberOfCells('../rats/rats/_con/_con_4/process_input.txt'))
unit_counts.extend(getNumberOfCells('../rats/rats/_con/_con_5/process_input.txt'))
unit_counts.extend(getNumberOfCells('../rats/rats/_con/_con_6/process_input.txt'))

print(np.mean(unit_counts))
print(max(unit_counts))
print(min(unit_counts))

placefields = loadPlaceFieldsFromFile('../rats/rats/bon/bon_4/placefields.txt')

#displayPlaceField(getPlaceFields(placefields,'TrackB', '11_1')[0])
#displayPlaceField(getPlaceFields(placefields,'TrackB', '11_1')[1])

def showBoxPlot() :
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)

    files = listdir('../rats/rats/bon/bon_4/bon_4_4_run/smoothed/')
    unit_spikes = []

    ax1.set_xlim([0,1000])
    ax1.set_ylim([0,0.1*len(files)])
    ax1.yaxis.set_visible(False)

    file_pos = 0
    for f in files :
        placecell1 = loadSpikes('../rats/rats/bon/bon_4/bon_4_4_run/smoothed/' + f)
        #pc_var = np.var(placecell1)
        #print(pc_var)

        ax1.text(-1.0, file_pos + 0.01, f[5:-4],
            verticalalignment='bottom', horizontalalignment='right',
            #transform=ax1.transAxes,
            color='black', fontsize=10)

        unit_spikes1 = smoothUnitSpikes(placecell1, 2)
        unit_spikes.append(unit_spikes1)
        #print(unit_spikes1)

        for s in range(0,len(unit_spikes1)) :
            if unit_spikes1[s] == 1 :
                ax1.add_patch(
                    pch.Rectangle(
                        (s, file_pos),   # (x,y)
                        1,          # width
                        0.1,          # height
                    facecolor="blue")
                )
        file_pos += 0.1

    plt.show()

    overlaps = compareUnitSpikes(unit_spikes)
    print(overlaps)
