import constants as cts
import numpy as np
import pandas as pd
from datetime import timedelta


def filter_color(df, color, diff=False):
    '''Computes a filter over the colors
        @df: dataset of events
        @color: color name to be filtered
        @diff: bool - decide if will exclude or include'''

    # Filter
    if not diff:
        df = df[df['Colors'] == cts.colorName2Id[color]]
    else:
        df = df[df['Colors'] != cts.colorName2Id[color]]

    return df


def get_specif_agg(df_sum, df_freq, title):
    '''Convert to string the information contained into the group by
        @df_sum: group by Name/Duration, agg sum
        @df_freq: group by Name/Duration, agg count'''

    info = ''
    for i in df_sum.index:       
        # All Day Events user case
        if title=='All Day':
            str_sum = str(df_sum.loc[i,'duration'].total_seconds()/3600/24)
            main_info = f'Event {i.capitalize()} - total {str_sum} days.'
        else:
            sum = df_sum.loc[i,'duration'].total_seconds()/3600/1
            str_freq = str(df_freq.loc[i,'duration'])
            str_avg = float(sum)/float(str_freq)
            main_info = f'Event {i.capitalize()} - reapeats {str_freq} times --- total {sum:.2f} hours --- avg {str_avg:.2f}.'
        
        if cts.DISPLAY=='l01':
            info += '\t\t\t'+main_info+'\n'
        elif cts.DISPLAY=='l02':
            info += '<p>'+main_info+'</p>'
        else:
            info += 'No layout defined.'

    return info


def display_info(title, unique_names, total_hours, hours_byName, freq_byName, df):
    '''Return a string with using some layout
        @title: cluster of events name
        @unique_name: list of unique events names
        @total_hours: int - total of time spend
        @hour_byName: group by Name/Duration, agg sum
        @freq_buName: group by Name/Duration, agg count'''

    # All Day Events user case
    if title=='All Day':
        div_by, time_ref = 24, 'days'
    else:
        div_by, time_ref = 1, 'hours'

    # Expected total hours
    if title=='Work':
        df_temp = df[['WeekByYear','StartTimeStamp']]
        df_temp['DayByWeek'] = df['StartTimeStamp'].dt.weekday
        df_temp = df_temp[df_temp['DayByWeek'] != 6]
        df_temp = df_temp[df_temp['DayByWeek'] != 5]
        workdays = df_temp.drop_duplicates(subset=['WeekByYear','DayByWeek']).shape[0]
        work_pref = f' - normal of {8*workdays} hours in {workdays} days'
    elif title=='Main':
        expected_hours = 21
        work_pref = f' - expected {(expected_hours/7)*cts.DAYS} hours'
    else:
        work_pref = ''

    # Remove empty response in total hours
    if str(total_hours)=='NaT':
        total_hours_str = ''
    else:
        # Total hours in float
        hours = total_hours.total_seconds()/3600/div_by

        # Percentage of total hours
        if title!='All Day':
            period_hours = cts.DAYS * 24
            perc_hour = (hours*100)/period_hours
            work_pref += f' - {perc_hour:.3f}% of the time'

        # Response
        total_hours_str = f'{(hours):.2f} '+time_ref+work_pref+'.'

    # Remove empty response in unique names
    if len(unique_names)>0:
        unique_names = np.append(unique_names,'.')
        uniq_name_str = f'{", ".join(unique_names[:-1])}{unique_names[-1]}'
    else:
        uniq_name_str = ''

    if cts.DISPLAY=='l01': # txt format
        title_display = f'\t{title} Time:\n'
        unq_name = f'\t\tUniques Names: {uniq_name_str}\n'
        total_hours_display = f'\t\tTotal Hours: ' + total_hours_str + '\n'
        hours_byName_display = f'\t\tHours by name: \n{get_specif_agg(hours_byName, freq_byName, title)[:-2]}'
        return title_display+unq_name+total_hours_display+hours_byName_display
    elif cts.DISPLAY=='l02': # html format
        title_display = f'<h2>{title} Time</h2>\n'
        unq_name = f'<strong>Uniques Names</strong><p>{uniq_name_str}</p>'
        total_hours_display = f'<strong>Total Hours</strong><p>'+total_hours_str+'</p>'
        hours_byName_display = f'<strong>Hours by name</strong>{get_specif_agg(hours_byName, freq_byName, title)}'
        return title_display+unq_name+total_hours_display+hours_byName_display
    elif cts.DISPLAY=='l03': # data format
        return df
    else:
        return 'No layout defined.'


def get_agg(df):
    '''Computes aggreations - unique name, total of hours spend
        and two group by Name and Duration, one is sum and count
         @df: dataset with the events'''
    
    # Aggregations
    unique_names, total_hours = df['Name'].unique(), df['duration'].sum()
    hours_byName = df[['Name','duration']].groupby(by='Name').sum()
    freq_byName = df[['Name','duration']].groupby(by='Name').count()
    hours_byNameSort = hours_byName.sort_values(['duration'], ascending=False)
    freq_byNameSort = freq_byName.sort_values(['duration'], ascending=False)

    return unique_names,total_hours,hours_byNameSort,freq_byNameSort
