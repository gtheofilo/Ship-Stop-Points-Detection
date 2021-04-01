# Ship-Stop-Points-Detection

A Pandas based Algorithm for Ship Stop Points Detection in AIS Data

Given a dataset of spatiotemporal data, the provided algorithm can create meaningful ship trajectories starting and ending at a stop point. The nature of each stop point varies depending on the vessel type. For a passenger or a cruise a ship a stop point could be a port or a mid - sea stop due to anomalous events. The same applies for fishing boats with the different that a mid - sea stop could describe a specific fishing spot.

In order for the algorithm to work a DataFrame with the following columns should be provided:

- "calc_speed": the speed noted by each AIS signal
- "timestamp": a unix timestamp(usually given in s or ms)
- "mmsi or an uid": describes a moving vessel or a temporal trajectory


