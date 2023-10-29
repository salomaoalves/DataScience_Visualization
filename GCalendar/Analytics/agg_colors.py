import Analytics.aux_analytics as aux


def get_banana(data):
    # Filter by color - include
    df = aux.filter_color(data, 'Banana')

    # New col - events duration
    df['duration'] = df['EndTimeStamp']-df['StartTimeStamp']

    # Get only events with duration smaller than 24hrs
    df = df[(df['duration'].dt.total_seconds() // 86400) == 0]

    # Aggregations to return
    unique_names, total_hours, hours_byName, freq_byName = aux.get_agg(df)

    # Info display
    return aux.display_info('Yellow', unique_names, total_hours, hours_byName, freq_byName, df)

def get_tomato(data):
    # Filter by color - include
    df = aux.filter_color(data, 'Tomato')

    # New col - events duration
    df['duration'] = df['EndTimeStamp']-df['StartTimeStamp']

    # Get only events with duration smaller than 24hrs
    df = df[(df['duration'].dt.total_seconds() // 86400) == 0]

    # Aggregations to return
    unique_names, total_hours, hours_byName, freq_byName = aux.get_agg(df)

    # Info display
    return aux.display_info('Work', unique_names, total_hours, hours_byName, freq_byName, df)

def get_grape(data):
    # Filter by color - include
    df = aux.filter_color(data, 'Grape')

    # New col - events duration
    df['duration'] = df['EndTimeStamp']-df['StartTimeStamp']

    # Get only events with duration smaller than 24hrs
    df = df[(df['duration'].dt.total_seconds() // 86400) == 0]

    # Aggregations to return
    unique_names, total_hours, hours_byName, freq_byName = aux.get_agg(df)

    # Info display
    return aux.display_info('Social', unique_names, total_hours, hours_byName, freq_byName, df)

def get_flamingo(data):
    # Filter by color - include
    df = aux.filter_color(data, 'Flamingo')

    # New col - events duration
    df['duration'] = df['EndTimeStamp']-df['StartTimeStamp']

    # Get only events with duration smaller than 24hrs
    df = df[(df['duration'].dt.total_seconds() // 86400) == 0]

    # Aggregations to return
    unique_names, total_hours, hours_byName, freq_byName = aux.get_agg(df)

    # Info display
    return aux.display_info('Transport', unique_names, total_hours, hours_byName, freq_byName, df)

def get_blueberry(data):
    # Filter by color - include
    df = aux.filter_color(data, 'Blueberry')
    
    # New col - events duration
    df['duration'] = df['EndTimeStamp']-df['StartTimeStamp']

    # Get only events with duration smaller than 24hrs
    df = df[(df['duration'].dt.total_seconds() // 86400) == 0]

    # Aggregations to return
    unique_names, total_hours, hours_byName, freq_byName = aux.get_agg(df)

    # Info display
    return aux.display_info('Workout', unique_names, total_hours, hours_byName, freq_byName, df)

def get_tangerine(data):
    # Filter by color - include
    df = aux.filter_color(data, 'Tangerine')

    # Filter by name - exclude
    df = df[df['Name'] != 'go lnrs'] #delete in 2023

    # New col - events duration
    df['duration'] = df['EndTimeStamp']-df['StartTimeStamp']

    # Get only events with duration smaller than 24hrs
    df = df[(df['duration'].dt.total_seconds() // 86400) == 0]

    # Aggregations to return
    unique_names, total_hours, hours_byName, freq_byName = aux.get_agg(df)

    # Info display
    return aux.display_info('Food', unique_names, total_hours, hours_byName, freq_byName, df)

def get_sage(data):
    # Filter by color - include
    df = aux.filter_color(data, 'Sage')

    # New col - events duration
    df['duration'] = df['EndTimeStamp']-df['StartTimeStamp']

    # Get only events with duration smaller than 24hrs
    df = df[(df['duration'].dt.total_seconds() // 86400) == 0]

    # Aggregations to return
    unique_names, total_hours, hours_byName, freq_byName = aux.get_agg(df)

    # Info display
    return aux.display_info('Student', unique_names, total_hours, hours_byName, freq_byName, df)
    
def get_basil(data):
    # Filter by color - include
    df = aux.filter_color(data, 'Basil')
    
    # New col - events duration
    df['duration'] = df['EndTimeStamp']-df['StartTimeStamp']

    # Get only events with duration smaller than 24hrs
    df = df[(df['duration'].dt.total_seconds() // 86400) == 0]

    # Aggregations to return
    unique_names, total_hours, hours_byName, freq_byName = aux.get_agg(df)

    # Info display
    return aux.display_info('Self-Learning', unique_names, total_hours, hours_byName, freq_byName, df)
    
def get_lavender(data):
    # Filter by color - include
    df = aux.filter_color(data, 'Lavender')
    
    # New col - events duration
    df['duration'] = df['EndTimeStamp']-df['StartTimeStamp']

    # Get only events with duration smaller than 24hrs
    df = df[(df['duration'].dt.total_seconds() // 86400) == 0]

    # Aggregations to return
    unique_names, total_hours, hours_byName, freq_byName = aux.get_agg(df)

    # Info display
    return aux.display_info('Streaming', unique_names, total_hours, hours_byName, freq_byName, df)
    

