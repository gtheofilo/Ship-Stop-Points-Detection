
# Ship-Stop-Points-Detection

A Pandas based Algorithm for Ship Stop Points Detection in AIS Data

Given a dataset of spatiotemporal data, the provided algorithm can create meaningful ship trajectories starting and ending at a stop point. The nature of each stop point varies depending on the vessel type. For a passenger or a cruise a ship a stop point could be a port or a mid - sea stop due to anomalous events. The same applies for fishing boats with the difference that a mid - sea stop could describe a specific fishing spot.

In order for the algorithm to work a DataFrame with the following columns should be provided:
- "longitude" : lon of each signal
- "latitude": lat of each signal
- "calc_speed": the speed noted by each AIS signal
- "timestamp": a unix timestamp(usually given in s or ms)
- "mmsi or an uid": describes a moving vessel or a temporal trajectory

The algoirthm runs by calling the following Python function:

    trajectories = stop_points_based_segmentation(dataframe, identifier='mmsi', speed_threshold=2., distance_threshold=5.0, time_threshold=300.)
    # returns a given DataFrame eniriched with a traj_id column 

 1. speed_threshold is given km/h 
 2. distance_threshold in km
 3. time_threshold in the same units as the "timestamp" column of the
    provided DataFrame
    
The default thresholds are based on the movement of passenger and cruise ships through the Aegean Sea. I advice you to experiment with these values and keep the ones that produce the best results for you as the heavily depend on the type of the vessels that you are analysing and the area that they are moving.

* The algorithm doesn't keep the continious stationary points after a stop. When a ship is stationary at a port it continues to produce AIS signals. These signals are not contained at the final trajectories so that each trajectory has a starting point(beginning of the trip), the intermidiate points(sailing) and the final stop point.
*  Depending on the health status, the uniformity of the given data and the goal of your data analysis, you may perform a cleaning procedure at the produced trajectories like removing those with less than 10 points etc.
*  For a Dataset of 450.000 rows and 35 unique MMSI, the algorithm produces 4132 trajectories in 109 seconds.

The below image contains the meaningful port to port trajectories from a cruise ship sailing through Greece.

![alt text](https://i.imgur.com/Gav3mF6.png)


