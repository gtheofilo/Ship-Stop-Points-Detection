import numpy as np
import pandas as pd

def side_search(partitioned_trajectory, center_point, distance_threshold):
    """
    Used for calculating the left and right limits of a trajectory given a center point and the needed conditions.
    """
    
    copy = partitioned_trajectory.copy(deep=False)
    # Calculates the haversine distance between the center and the remaining side points
    copy['d_distance'] = _distance_difference(copy, center_point)
    # Calculates the time difference between the center and the ramining side points
    copy['d_time'] = np.abs(copy['timestamp'] - center_point['timestamp'])

    try:
        # If a point that satisfying the above conditions exists, return it
        # otherwise reutrn None
        return copy[
            (copy['d_distance'] <= distance_threshold) 
            & (copy['d_time'] <= 3600)]['d_distance'].idxmax()
    except ValueError:
        return None


    
def stop_points_based_segmentation(trajectories, identifier='id', speed_threshold=2.0, distance_threshold=5.0, time_threshold=300):
    """
    Given a DataFrame with lon, lat, timestamp, speed and an identifier column where each row describes a time ordered
    gps point, 'stop_points_based_segmentation' calculates the stop points and segments the DataFrame into individual
    trips with a beginning and an end.
    
    The metric system of speed and distance threshold depends on your data. For example, if you provide the speed given in the 
    trajectories dataframe in km/h then the threshold should be set accordingly. The same applies for distance.
    
    The timestamp column of the dataframe should be in unix epoch (seconds).
    
    Step 1:
    For each unique identifier(could be a ship's MMSI or generally a number that describes unique moving objects) the
    algorithms begins by calculating the candidate stop points. A candidate stop point is simply a point with moving speed
    less than the given parameter for the speed_threshold.
    
    Step 2:
    For each candidate stop point, the algorithm performs a left search with radius given by the distance_threshold. For
    example if the given threshold is 2 nautical miles it searches for all points under the distance bound that has a speed
    higher than the threshold and time difference lower than the time_threshold. From these points it returns the one with the
    higher distance. The same procedure goes by for the right part of the trajectory.
    
    Step 3:
    If the time difference between the left and the right limit is more than the given time threshold then the point is assigned
    to the stop points set and the algorithm continious inspecting the other candidates points. In other words if the moving
    object completed the distance between the left and the right point in more than the threshold the center this distance
    is a stop point.
    
    ***
    For the 2nd step we could just loop through the left and right of each point and stop when the distance's limit is
    exceeded. We choosed not to follow this approach as Python's higher level loops where not as efficienty as Pandas
    indexing and selecting functions. 
    
    Thus during selecting the row with maximum distance under the given distance threshold we introduce one more temporal conditional 
    check. In this way, we avoid choosing left/right limits that are close in distance but have 
    a high time difference. Imagine if the moving object passed by the same spot before without stoping, it would be under 
    the distance threshould but this could have happened at different time - window.
    
    
    Arguments:
        trajectories {DataFrame} -- Data in Pandas DataFrame format. The geospatial data should be
                                     come along with their identifier, speed, lon, lat and timestamp
                                     columns.
                                     
        identifier (int) -- Used for aggregating the trajectories dataframe into seperated groups. 
                            By default it's the ship's MMSI. It could also be a custom calculated id.
                                       
        speed_threshold {number} -- The minimum speed that a point must have in order to be 
                                    characterized  a stop point.
                                    
        distance_threshold {number} -- Radius to search around each candidate stop point
        
        time_threshold {number} -- The minimum time to move through the given radius(distance_threshold) in seconds.
    """
    
    temp = []
    traj_id_ = 1

    for traj_id, sdf in trajectories.groupby(identifier, group_keys=False):
        grp_copy = sdf.copy(deep=False).reset_index(drop=True).sort_values(by='timestamp', ascending=True)
        
        # Stop points for each group
        stop_points = [0]    
        # Candidates points
        slow_speed_points = grp_copy[grp_copy['speed'] <= speed_threshold].index
        candidates_index = 0
        
        while not slow_speed_points.empty and candidates_index < len(slow_speed_points):
            center = slow_speed_points[candidates_index]
            center_row = grp_copy.iloc[center]
            
            # Left Search
            li = side_search(grp_copy.iloc[stop_points[-1]:center], center_row, distance_threshold)
            # Right Search
            ri = side_search(grp_copy.iloc[center + 1:], center_row, distance_threshold)
                 
            # If there is no right or left point closer that satisfies the side_search conditions
            if li is None or ri is None:
                candidates_index = candidates_index + 1
                continue

                
            left_limit = grp_copy.iloc[li]
            right_limit = grp_copy.iloc[ri]
            if (right_limit['timestamp'] - left_limit['timestamp']) >= time_threshold:  
                stop_points.append(center)
                try:
                    # If we are not at the end of the data stream
                    _next = grp_copy.iloc[ri + 1:][grp_copy['speed'] > speed_threshold]['timestamp'].idxmin()
                    slow_speed_points = grp_copy.iloc[_next:][grp_copy['speed'] <= speed_threshold].index
                    candidates_index = 0
                except ValueError:
                    break
            else:
                candidates_index = candidates_index + 1
                

        stop_points.pop(0)
        # Mark stop points
        if len(stop_points) == 0:
            continue
        grp_copy.loc[stop_points, 'stop'] = 'Yes'

        # Segment trips based on stop - points index position
        if grp_copy.iloc[:stop_points[0]][grp_copy['speed'] > speed_threshold]['timestamp'].empty:
            last_check = 0
        else:
            last_check = grp_copy.iloc[:stop_points[0]][grp_copy['speed'] > speed_threshold]['timestamp'].idxmin()
            
        sdfs = []
        for ind in stop_points:
            sdfs.append(grp_copy.iloc[last_check:ind + 1])
            try:
                last_check = grp_copy.iloc[ind + 1:][grp_copy['speed'] > speed_threshold]['timestamp'].idxmin()
            except ValueError:
                last_check = ind + 1

        for i in range(0,len(sdfs)):
            if sdfs[i].empty:
                continue
            sdfs[i]['traj_id'] = traj_id_
            traj_id_ = traj_id_ + 1
    
        temp.extend(sdfs) 
    
    return pd.concat(temp)
  
def _distance_difference(point1, point2):
    return _haversine_np(point1['lon'], point1['lat'], point2['lon'], point2['lat'])

  
def _haversine_np(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)

    All args must be of equal length.

    """
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = np.sin(dlat / 2.0) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2.0) ** 2

    c = 2 * np.arcsin(np.sqrt(a))
    km = 6367 * c
    return km
