import csv
import numpy as np
from itertools import groupby
import matplotlib.pyplot as plt
import matplotlib.patches as pch
from os import listdir

mazes = ['Mwheel']#, 'bigSquare', 'plus', 'bigSquarePlus', 'linear', 'Zigzag', 'sleep', 'Tmaze']
files = [ 'ec014.123', 'ec014.195', 'ec014.405', 'ec014.440', 'ec016.483'] #['ec013.773', 'ec013.782', 'ec013.819', 'ec013.898', 'ec013.922', 'ec014.183',
out = []

with open('../hc3-session.csv') as sessionfile:
    sessionreader = csv.reader(sessionfile)
    for session in sessionreader:
        if session[3] in mazes :
            session_id = session[1]
            run_id = session[2]
            rat_id = (session_id.split('.'))[0]
            out.append([rat_id, run_id, session_id, session[3]])

cells = []
with open('../hc3-cell.csv') as cellfile:
    cellreader = csv.reader(cellfile)
    for cell in cellreader:
        cells.append(cell)

with open('../hc3-meta.csv', 'w') as metafile:
    metawriter = csv.writer(metafile,lineterminator='\n')
    for sesh in out: # pick associated CA1 and CA3 pyramid cells
        sesh_cells = [c for c in cells if c[1] == sesh[2] and (c[5] == 'CA1' or c[5] == 'CA2' or  c[5] == 'CA3') and c[14] == 'p']
        units = []
        shanks = []
        for cell in sesh_cells:
            sesh.append(cell[3] + '_' + cell[4])
            units.append(cell[3] + '_' + cell[4])
            if not int(cell[3]) in shanks:
                shanks.append(int(cell[3]))
        if sesh_cells:
            metawriter.writerow(sesh)

        pos_timestep = 1.0 / 39.06
        pos_time = 0.0
        dir = sesh[1]

        if not dir in files:
            continue

        if not shanks:
            continue

        print('Dir ' + dir + '\n')
        print(shanks)

        with open('../'+ dir + '_raw/'+ dir + '.whl') as whlfile:
            with open('../' + dir + '/run.txt','w') as posfile:
                poswriter = csv.writer(posfile,lineterminator='\n')
                whlreader = csv.reader(whlfile,delimiter='	')
                for whl_row in whlreader:
                    pos_time += pos_timestep
                    if(whl_row[0] == '-1' or whl_row[1] == '-1') :
                        continue
                    poswriter.writerow(['{:.2f}'.format(pos_time), '{:.2f}'.format(float(whl_row[0])), '{:.2f}'.format(float(whl_row[1]))])

        with open('../'+ dir +'/process_input.txt', 'w') as processfile:
            processwriter = csv.writer(processfile,lineterminator='\n')
            processwriter.writerow([dir +'/placefields.txt'])
            processwriter.writerow(['track','day','epoch','unit','run_file','spike_file','smoothed_output_file','place_field_image'])

            res_timestep = 1.0 / 20000.0
            for shank in shanks :
                with open('../' + dir + '_raw/' + dir + '.clu.' + str(shank)) as clufile:
                    with open('../' + dir + '_raw/' + dir + '.res.' + str(shank)) as resfile:
                        clureader = csv.reader(clufile)
                        resreader = csv.reader(resfile)

                        row1 = next(clureader)
                        num_clusters = int(row1[0])
                        spikes = []
                        for i in range(0,num_clusters) :
                            spikes.append([])

                        for clu_row in clureader:
                            cluster = int(clu_row[0])
                            res = float(next(resreader)[0]) * res_timestep

                            spikes[int(clu_row[0])].append(res)

                for s in range(2,len(spikes)):
                    if len(spikes[s]) <= 2 :
                         continue
                    if not str(shank) + '_' + str(s) in units:
                        continue
                    with open ('../'+ dir +'/spikes/unit_' + str(shank) + '_' + str(s) + '.txt', 'w') as spikefile:
                        spikewriter = csv.writer(spikefile,lineterminator='\n')
                        for spiketime in spikes[s]:
                            spikewriter.writerow(['{:.2f}'.format(spiketime)])

                for s in range(2, len(spikes)):
                    if len(spikes[s]) <= 2 :
                        continue
                    if not str(shank) + '_' + str(s) in units:
                        continue
                    processwriter.writerow(
                        ['figure8', '0', '0', str(shank) + '_' + str(s), dir + '/run.txt', dir +'/spikes/unit_' + str(shank) + '_' + str(s) + '.txt', dir + '/smoothed/unit_' + str(shank) + '_' + str(s) + '.txt', dir + '/fields/unit_' + str(shank) + '_' + str(s) + '.bmp'])
