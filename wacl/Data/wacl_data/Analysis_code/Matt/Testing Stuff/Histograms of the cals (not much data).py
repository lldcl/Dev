import matplotlib.pyplot as plt

import pandas as pd

slopes_pid2 = pd.Series([1.03,1.38,7.43,2.83,1.44,1.37,1.05,1.1,2.64,1.22,0.97,1.53,1.44,1.20,1.31,1.29,1.30,0.75,0.63,0.32,0.88,0.75,0.63,0.32,1.23,0.72,1.13])
slopes_pid3 = pd.Series([3.55,2.04,2.12,1.94,2.17,3.96,2.06,2.14,2.45,1.65,2.41,1.55,1.30,2.4,2.28,1.41,1.76,1.84,0.75,1.59,1.43,2.09,1.54,1.58,1.59])
slopes_pid4 = pd.Series([3.97,2.42,1.84,2.30,2.70,4.85,3.36,1.98,1.87,3.34,2.51,2.52,2.42,2.88,2.60,2.65,2.62,2.78,2.48,2.36,2.15,2.53,3.20,2.85,2.16,2.91])





figH = plt.figure()


ax1H = figH.add_subplot(311)
slopes_pid2.hist(bins = 13)
ax1H.set_ylim([0,12])
ax1H.set_xlim([0,8])

ax2H = figH.add_subplot(312)
slopes_pid3.hist(bins = 13)
ax2H.set_ylim([0,12])
ax2H.set_xlim([0,8])

ax3H = figH.add_subplot(313)
slopes_pid4.hist(bins = 13)
ax3H.set_ylim([0,12])
ax3H.set_xlim([0,8])






figB = plt.figure()

ax1B = figB.add_subplot(311)
ax1B.boxplot(slopes_pid2)
ax1B.set_ylim([0,8])

ax2B = figB.add_subplot(312)
ax2B.boxplot(slopes_pid3)
ax2B.set_ylim([0,8])

ax3B = figB.add_subplot(313)
ax3B.boxplot(slopes_pid4)
ax3B.set_ylim([0,8])

plt.show()