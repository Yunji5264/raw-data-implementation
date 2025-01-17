from class_predefine import *

# For spatial parameters
def get_space(spatial_parameter_list, df):
    with_granularity = []
    for param in spatial_parameter_list:
        granularity_value = spatial_granularity_mapping[param.spatialLevel]
        with_granularity.append((granularity_value, param))

    if not with_granularity:
        print("No valid spatial parameters found.")
        return None, None

    # Sort by granularity value
    sorted_para = sorted(with_granularity, key=lambda x: x[0])

    # Return the smallest and largest granularity items
    spatial_min = sorted_para[0][1]  # Item with smallest granularity value
    spatial_max = sorted_para[-1][1]  # Item with largest granularity value
    # Define the spatial granularity, which is the maximum granularity level in all spatial parameters
    spatial_granularity = spatial_max.spatialLevel
    # Define the spatial scope level, which is the minimum granularity level in all spatial parameters
    spatial_scope_level = spatial_min.spatialLevel

    # Get the saptial scope list
    # Extract column name from the spatial_min parameter
    column_name = spatial_min.dataName
    # Get unique values from the corresponding column in the DataFrame
    spatial_scope = df[column_name].dropna().unique()

    return spatial_granularity, spatial_scope_level, spatial_scope

def format_date(date, format_string):
    """
    Converts a date to a formatted string.

    Args:
    date (date or str): The date to format.
    format_string (str): The format string to apply.

    Returns:
    str: The formatted date string.
    """
    try:
        return pd.to_datetime(date).strftime(format_string)
    except Exception as e:
        print(f"Error formatting date: {e}")
        return None

# For temporal parameters
def get_time(temporal_parameter_list, df):
    with_granularity = []
    for param in temporal_parameter_list:
        granularity_value = temporal_granularity_mapping[param.temporalLevel]
        with_granularity.append((granularity_value, param))

    if not with_granularity:
        print("No valid spatial parameters found.")
        return None, None

    # Sort by granularity value
    sorted_para = sorted(with_granularity, key=lambda x: x[0])

    # Return the smallest and largest granularity items
    temporal_min = sorted_para[0][1]  # Item with smallest granularity value
    temporal_max = sorted_para[-1][1]  # Item with largest granularity value
    # Define the temporal granularity, which is the maximum granularity level in all temporal parameters
    temporal_granularity = temporal_max.temporalLevel
    # Define the temporal scope level, which is the minimum granularity level in all temporal parameters
    temporal_scope_level = temporal_min.temporalLevel

    # Get the saptial scope
    # Extract column name from the temporal_min parameter
    column_name = temporal_min.dataName
    temporalScopeStart = df[column_name].dropna().unique().min()
    temporalScopeEnd = df[column_name].dropna().unique().max()

    match temporal_min.temporalLevel:
        case "YEAR":
            temporalScopeStart = format_date(temporalScopeStart, '%Y-01-01')
            temporalScopeEnd = format_date(temporalScopeEnd, '%Y-12-31')
        case "MONTH":
            temporalScopeStart = format_date(temporalScopeStart, '%Y-%m-01')
            temporalScopeEnd = format_date(temporalScopeEnd, '%Y-%m-31')  # May need adjusting for actual month end

    return temporal_granularity, temporal_scope_level, temporalScopeStart, temporalScopeEnd

