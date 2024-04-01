import constants as cts
import Analytics.aux_analytics as aux
import pandas as pd
from datetime import timedelta

def get_main(data):
    # Filter by color and name - include
    df_basil = aux.filter_color(data, 'Basil')
    df_graphite = aux.filter_color(data, 'Graphite')
    df_sage = aux.filter_color(data, 'Sage')
    
    # Concataned all df
    df = pd.concat([df_basil, df_graphite, df_sage])
    
    # New col - events duration
    df['duration'] = df['EndTimeStamp']-df['StartTimeStamp']

    # Get only events with duration smaller than 24hrs
    df = df[(df['duration'].dt.total_seconds() // 86400) == 0]

    # Aggregations to return
    unique_names, total_hours, hours_byName, freq_byName = aux.get_agg(df)

    # Info display
    return aux.display_info('Main', unique_names, total_hours, hours_byName, freq_byName, df)

def get_fk_free():
    df = pd.read_csv(cts.DB_FK_PATH, sep=',')
    df['StartTimeStamp'] = pd.to_datetime(df['StartTimeStamp'], format='%Y-%m-%d %H:%M:%S')
    df['EndTimeStamp'] = pd.to_datetime(df['EndTimeStamp'], format='%Y-%m-%d %H:%M:%S')
    df['duration'] = df['EndTimeStamp']-df['StartTimeStamp']
    return df[df['Colors']==-1]
def get_free(data):
    # Copy data
    df = data.copy()

    # New col - events duration
    df['duration'] = df['EndTimeStamp']-df['StartTimeStamp']
    
    # Get only events with duration smaller than 24hrs
    df = df[(df['duration'].dt.total_seconds() // 86400) == 0]

    if cts.FK_DATA: 
        # Agg fake data for l01 or l02
        df = get_fk_free()
        free_hours = df['duration'].sum().total_seconds()/3600
        free_pref, days = '', df.shape[0]
    else:
        # Aggregations to return
        busy_hours = df['duration'].sum().total_seconds()/3600
        free_hours = (24*cts.DAYS) - busy_hours

        # Percentage of total hours
        period_hours, days = cts.DAYS*24, cts.DAYS
        perc_hour = (free_hours*100)/period_hours
        free_pref = f' - {perc_hour:.3f}% of the time.'

    # Info display
    if cts.NEW_FORMAT:
        return ''
    if cts.DISPLAY=='l01':
        return f'\tFree Time: {free_hours:.2f} - on avg {free_hours/days:.2f}'+free_pref
    elif cts.DISPLAY=='l02':
        return f'<h2>Free Time</h2><p>{free_hours} - on avg {free_hours/cts.DAYS:.2f}'+free_pref+'</p>'
    elif cts.DISPLAY=='l03':
        df['day'], df['Colors'] = df['StartTimeStamp'].apply(lambda x: x.strftime("%Y-%m-%d")), -1
        gb = df[['day','duration','Colors','WeekDay','WeekByMonth','WeekByYear','TimeZone']].\
            groupby(by=['day','Colors','WeekDay','WeekByMonth','WeekByYear','TimeZone']).sum()
        df_free = gb.sort_values(by='day').reset_index()
        df_free['duration'] = df_free['duration'].apply(lambda x: timedelta(days=1) - x)
        df_free['day'] = df_free['day'].apply(lambda x: x + ' 00:00:00')
        df_free['day'] = pd.to_datetime(df_free['day'], format='%Y-%m-%d %H:%M:%S')
        df_free['StartTimeStamp'], df_free['EndTimeStamp'], df_free['Name'] = df_free['day'], None, 'free'
        if cts.FK_DATA: return get_fk_free()
        else: return df_free.drop(['day'], axis=1)
    else:
        return 'No layout defined.'

def get_sleep(data):
    # Filter by color - include
    df = aux.filter_color(data, 'Default')

    # Filter by name - include
    df = df[df['Name'] == 'sleep']

    # New col - events duration
    df['duration'] = df['EndTimeStamp']-df['StartTimeStamp']

    # Get only events with duration smaller than 24hrs
    df = df[(df['duration'].dt.total_seconds() // 86400) == 0]

    # Aggregations to return
    total_hours = df['duration'].sum().total_seconds()/3600

    # Remove 'nan' response from total hours
    if str(total_hours)=='nan':
        total_hours = 0

    # Info display
    if cts.DISPLAY=='l01':
        return f'\tSleep Time:\n\t\tTotal Hours: {total_hours} hours - {(total_hours/cts.DAYS):.2f} per day.'
    elif cts.DISPLAY=='l02':
        return f'<h2>Sleep Time</h2><strong>Total Hours:</strong><p>{total_hours} hours - {(total_hours/cts.DAYS):.2f} per day.</p>'
    elif cts.DISPLAY=='l03':
        return df
    else:
        return 'No layout defined.'

def get_all_day(data):
    # Copy data
    df = data.copy()

    # New col - events duration
    df['duration'] = df['EndTimeStamp']-df['StartTimeStamp']

    # Get only events with duration bigger than 24hrs
    df = df[(df['duration'].dt.total_seconds() // 86400) != 0]

    # Aggregations to return
    unique_names, total_hours, hours_byName, freq_byName = aux.get_agg(df)

    # Info display
    return aux.display_info('All Day', unique_names, total_hours, hours_byName, freq_byName, df)

def get_social(data):
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
