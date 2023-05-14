import pandas as pd
import numpy as np


def _time_difference(timestamp1, timestamp2):
    return abs(timestamp2 - timestamp1)


def _calculate_speed(dis, time):
    return dis / time
    
    
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
    

def calculate_bearing(*args, **kwargs):
    if len(args) == 0:
        "When called with zero arguments"
        raise ValueError(
            f'Function takes  1 parameter, {len(args)} given. Either a DataFrame or a Row should be provided.')
    elif len(args) == 1:
        "When called by pandas groupby. Thus only one argument in *args is passed."
        if isinstance(args[0], pd.DataFrame):
            if 'lon' in kwargs and 'lat' in kwargs:
                df = args[0]
                df['bearing'] = _calculate_bearing(df[kwargs.get('lon')].values, df[kwargs.get('lat')].values,
                                                   df[kwargs.get('lon')].shift(-1).values,
                                                   df[kwargs.get('lat')].shift(-1).values)
                return df
            else:
                raise ValueError(f'The given {type(args[0])} must contains columns 1.lon, 2.lat')
    elif isinstance(args[0], pd.Series):
        "When called with series"
        return _calculate_bearing(args[0].values, args[1].values, args[2].values, args[3].values)


def calculate_time_difference(*args, **kwargs):
    if len(args) == 0 or len(args) > 2:
        raise ValueError(f'Function takes  1 or 2 parameters, {len(args)} given.')
    elif len(args) == 1:
        if isinstance(args[0], pd.DataFrame):
            if 'timestamp' in kwargs:
                df = args[0]
                df['time_diff'] = _time_difference(df[kwargs.get('timestamp')].shift(1).values,
                                                   df[kwargs.get('timestamp')].values)
                return df
            else:
                raise ValueError(f'The given {type(args[0])} must contains column 1. timestamp')
        elif isinstance(args[0], pd.Series):
            return _time_difference(args[0].shift(1).values, args[0].values)


def calculate_distance(*args, **kwargs):
    if len(args) == 0:
        "When called with zero arguments"
        raise ValueError(
            f'Function takes  1 parameter, {len(args)} given. Either a DataFrame or a Row should be provided.')
    elif len(args) == 1:
        "When called by pandas groupby. Thus only one argument in *args is passed."
        if isinstance(args[0], pd.DataFrame):
            if 'lon' in kwargs and 'lat' in kwargs:
                df = args[0]
                df['dis_diff'] = _haversine_np(df[kwargs.get('lon')].values, df[kwargs.get('lat')].values,
                                               df[kwargs.get('lon')].shift(1).values,
                                               df[kwargs.get('lat')].shift(1).values)
                return df
            else:
                raise ValueError(f'The given {type(args[0])} must contains columns 1.lon, 2.lat')
    elif isinstance(args[0], pd.Series):
        "When called with series"
        return _haversine_np(df[kwargs.get('lon')].values, df[kwargs.get('lat')].values,
                                               df[kwargs.get('lon')].shift(1).values,
                                               df[kwargs.get('lat')].shift(1).values)


def calculate_speed(*args, **kwargs):
    if len(args) == 0 or len(args) > 3:
        raise ValueError(f'Function takes  1 parameter, {len(args)} given.')
    elif len(args) == 1:
        "When called by pandas groupby. Thus only one argument in *args is passed."
        if isinstance(args[0], pd.DataFrame):
            if 'time_diff' in kwargs and 'dis_diff' in kwargs:
                df = args[0]
                df['speed'] = _calculate_speed(df[kwargs.get('dis_diff')].values,
                                                    df[kwargs.get('time_diff')].values) 
                return df
            else:
                raise ValueError(f'The given {type(args[0])} must contains column 1.time_diff, 2.dis_diff')
    elif len(args) == 2:
        "When called with series."
        if isinstance(args[0], pd.Series):
            return _calculate_speed(args[0].values, args[1].values)
