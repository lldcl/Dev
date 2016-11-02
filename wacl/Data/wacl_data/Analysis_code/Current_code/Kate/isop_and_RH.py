import matplotlib.pyplot as plt

# Isoprene sensitvity decreasing as the RH increases.
RH1 = [1.16,21.81,43.46,60.67]
MOS1 = [20.64, 10.97, 6.77, 5.38]
MOS2 = [29.29, 15.91, 10.59, 9.10]

RH = plt.figure()
ax1 = RH.add_subplot(1,1,1)
ax1.scatter(RH1, MOS1, color = "tomato", label="MOS1")
ax1.set_ylabel("MO isoprene sensitivity mV ppb-1 (V)")
ax1.scatter(RH1, MOS2, color = "mediumslateblue", label="MOS2")
ax1.set_xlabel("Relative humidity (%)")
ax1.legend()

RHmonth =[ 23.44, 79.35428227, 43.40313722, 3.459355927]
MOS1month = [7.58, 2.87, 3.58, 19.18]
MOS2month = [14.02, 6.11, 8.51, 35.24]
RHlater = plt.figure()
ax1 = RHlater.add_subplot(1,1,1)
ax1.plot(RH1, MOS1, color = "tomato", label="MOS1 Dec 2015")
ax1.set_ylabel("MO isoprene sensitivity mV ppb-1 (V)")
ax1.plot(RH1, MOS2, color = "mediumslateblue", label="MOS2 Dec 2015")
ax1.scatter(RHmonth, MOS1month, color = "green", label="MOS1 Jan 2016")
ax1.scatter(RHmonth, MOS2month, color = "hotpink", label="MOS2 Jan 2016")
ax1.set_xlabel("Relative humidity (%)")
ax1.legend()

# Total VOC sensitvity vs RH.

RH2 = [56.56, 62.77,63.52,80.06,84.88,93.41,1.60,0.79,71.63,63.79,80.59,1.30,37.91,70.48]
MOS1VOC = [2.344,2.200,2.083,1.694,1.837,1.508,10.7,8.902,2.102,2.400,1.327,7.418,1.635,1.276]
MOS2VOC = [3.986,3.866,3.554,2.961,2.870,2.402,13.23,8.939,3.127,2.671,1.528,6.784,1.810,1.715]

RHVOC = plt.figure()
ax1 = RHVOC.add_subplot(1,1,1)
ax1.scatter(RH2, MOS1VOC, color = "darkorchid", label="MOS1")
ax1.set_ylabel("MO total VOC sensitivity mV ppb-1 (V)")
ax1.scatter(RH2, MOS2VOC, color = "hotpink", label="MOS2")
ax1.set_xlabel("Relative humidity (%)")
ax1.legend()

plt.show()