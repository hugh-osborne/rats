import csv
import numpy as np
from itertools import groupby
import matplotlib.pyplot as plt
import matplotlib.patches as pch
from os import listdir

mazes = ['Mwheel']#, 'bigSquare', 'plus', 'bigSquarePlus', 'linear', 'Zigzag', 'sleep', 'Tmaze']
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
        sesh_cells = [c for c in cells if c[2] == sesh[0] and (c[5] == 'CA1' or c[5] == 'CA2' or  c[5] == 'CA3') and c[14] == 'p']
        for cell in sesh_cells:
            sesh.append(cell[3] + '_' + cell[4])
        if sesh_cells:
            metawriter.writerow(sesh)



