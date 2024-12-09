# Ship Stop Points Detection Framework

## A Pandas-Based Algorithm for Detecting Ship Stop Points in AIS Data  

This framework introduces a Pandas-based algorithm designed to analyze spatiotemporal Automatic Identification System (AIS) data and generate meaningful ship trajectories anchored at stop points. The nature of stop points varies depending on vessel type: for instance, stop points for passenger or cruise ships could be ports or mid-sea halts due to anomalous events. Similarly, fishing vessels may exhibit mid-sea stops representing specific fishing locations.

### Input Data Requirements  

To utilize the algorithm, a DataFrame with the following columns is required:  
- **`longitude`**: Longitude of each AIS signal.  
- **`latitude`**: Latitude of each AIS signal.  
- **`speed`**: Speed associated with each AIS signal.  
- **`timestamp`**: A Unix timestamp in seconds.  
- **`mmsi` or **`uid`**: A unique identifier for each vessel or temporal trajectory.

### Functionality  

The algorithm is executed through the following Python function:  

```python
trajectories = stop_points_based_segmentation(
    dataframe, 
    identifier='mmsi', 
    speed_threshold=2.0, 
    distance_threshold=5.0, 
    time_threshold=300.0
)
# Returns the input DataFrame enriched with a 'traj_id' column
```

#### Parameter Descriptions  
1. **`speed_threshold`**: Speed threshold (units match those in the input DataFrame).  
2. **`distance_threshold`**: Distance threshold (units match those in the input DataFrame).  
3. **`time_threshold`**: Time threshold in seconds (units match those of the `timestamp` column).  

#### Default Thresholds  
The default parameter values are tailored for passenger and cruise ships traversing the Aegean Sea. Users are encouraged to experiment with these parameters to optimize results based on the vessel type and the geographic region being analyzed.

### Algorithm Behavior  

1. The algorithm excludes continuous stationary points after a stop. For example, AIS signals generated while a ship is stationary at a port are filtered out to ensure that each trajectory includes only:  
   - A starting point (beginning of the trip).  
   - Intermediate points (sailing phase).  
   - A final stop point.  

2. Post-processing recommendations: Depending on the quality of the data, its uniformity, and analytical goals, users may apply additional cleaning procedures to the generated trajectories. For instance, removing trajectories with fewer than ten points can improve dataset relevance and clarity.

### Performance  

For a dataset of approximately 450,000 rows and 35 unique MMSI identifiers, the algorithm produced 4,132 trajectories in 109 seconds.  

### Visual Representation  

The image below illustrates meaningful port-to-port trajectories of a cruise ship navigating through Greece.  

![Port-to-Port Trajectories](https://i.imgur.com/Gav3mF6.png)

This algorithm provides a robust and efficient solution for extracting stop points and constructing trajectories from AIS data, enabling comprehensive maritime analysis.
