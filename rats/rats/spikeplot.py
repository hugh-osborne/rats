import csv
import numpy as np
import matplotlib.pyplot as plt

filenames = ['pc1.txt', 'pc2.txt', 'pc3.txt', 'pc4.txt', 'pc5.txt']

plt.figure()

for fn in filenames :
    spikes = []
    with open(fn) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader :
            spikes.append(np.float64(row[0]))

    spikes_avg = np.convolve(np.array(spikes), np.ones((10,))/10, mode='valid')
    plt.plot(range(0, len(spikes_avg)), spikes_avg)

plt.legend(filenames);
plt.show()
