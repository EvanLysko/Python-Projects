##Evan Lysko
##6/16
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime

bird_data = pd.read_csv("/Users/evanlysko/Desktop/PythonforResearch/Birds/bird_tracking.csv")

bird_names = pd.unique(bird_data.bird_name)

plt.figure(figsize=(7,7))
for bird_name in bird_names:
    ix = bird_data.bird_name == bird_name
    x, y = bird_data.longitude[ix], bird_data.latitude[ix]

    plt.plot(x, y, ".", label=bird_name)

plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.legend(loc="lower right")
plt.savefig("3traj.pdf")

plt.figure(figsize=(8,4))
speed = bird_data.speed_2d[bird_data.bird_name == "Eric"]
ind = np.isnan(speed)
plt.hist(speed[~ind], bins=np.linspace(0,30,20), density=True)
plt.xlabel("2D speed (m/s)")
plt.ylabel("Frequency");

bird_data.speed_2d.plot(kind='hist', range =[0,30])
plt.xlabel("2D speed");
plt.savefig("pd_hist.pdf")

timestamps = []
for k in range(len(bird_data)):
    timestamps.append(datetime.datetime.strptime\
    (bird_data.date_time.iloc[k][:-3],"%Y-%m-%d %H:%M:%S"))

bird_data["timestamp"] = pd.Series(timestamps, index=bird_data.index)
times = bird_data.timestamp[bird_data.bird_name == "Eric"]
elapsed_time = []
for time in times:
    elapsed_time.append(time-times[0])
print(bird_data[:5])
print(elapsed_time[1000])

plottime = []
for i in elapsed_time:
    plottime.append(i / datetime.timedelta(days=1))
print(max(plottime))
plt.plot(np.array(plottime))
plt.xlabel("Observation")
plt.ylabel("Elapsed time (days)");
plt.ylim(0,300)
plt.savefig("timeplot.pdf")

data = bird_data[bird_data.bird_name == "Eric"]
times = data.timestamp
elapsed_time = [time - times[0] for time in times]
elapsed_days = np.array(elapsed_time) / datetime.timedelta(days=1)

next_day = 1
inds = []
daily_mean_speed = []
for (i, t) in enumerate(elapsed_days):
    if t < next_day:
        inds.append(i)
    else:
        #compute mean speed
        daily_mean_speed.append(np.mean(data.speed_2d[inds]))
        next_day += 1
        inds = []
plt.figure(figsize=(8,6))
plt.plot(daily_mean_speed)
plt.xlabel("Day")
plt.ylabel("Mean speed (m/s)");
plt.savefig("dms.pdf")
