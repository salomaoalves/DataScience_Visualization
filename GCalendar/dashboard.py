from Visu import rest_events as rest_visu, daily_events as daily_visu, workout_events as workout_visu
from Visu import streaming_events as stream_visu, important_events as impt_visu, transport_events as transpt_visu
from Visu import resume_events as resume_visu, social_events as social_visu, allDay_events as all_visu
from Visu import create_html
import constants as cts
from datetime import timedelta
import pandas as pd
from Visu import build

import data as data
DATA = cts.DATA

# Functions and Definitions used in the code
def remove_allDay(df):
    '''Remove all allDay event from the data'''
    df['duration'] = df['EndTimeStamp'] - df['StartTimeStamp']
    df = df[(df['duration'].dt.total_seconds() // 86400) == 0]
    return df
dfRemoveAllDay = remove_allDay(DATA.copy())
if cts.FK_DATA: dfRemoveAllDay = dfRemoveAllDay[dfRemoveAllDay['Colors']!=-1]

def only_colors(df, colors):
    '''Leave only colors that we want to use'''
    return df[df['Colors'].isin(colors)]

def create_agg(data, col1, col2, sortDayMonth=False):
    '''Create a simple aggregation to show the frequency'''
    data = data[col1].value_counts().to_frame().sort_values(col2).reset_index()
    if sortDayMonth:
        data['DayMonthExpand'] = data['DayMonth'].apply(lambda x: 
                                (str(x.split('/')[0]) if len(str(x.split('/')[0]))>1 else '0'+str(x.split('/')[0]))+'/'+
                                (str(x.split('/')[1]) if len(str(x.split('/')[1]))>1 else '0'+str(x.split('/')[1])))
        data['DayMonthDatetime'] = pd.to_datetime(data['DayMonthExpand'], format='%d/%m')
        return data.sort_values('DayMonthDatetime').drop(['DayMonthExpand','DayMonthDatetime'], axis=1)
    else:
        return data

# Header info
first_day = min(DATA["StartTimeStamp"]).date()
last_day = max(DATA["StartTimeStamp"]).date()
duration = (max(DATA["StartTimeStamp"]) + timedelta(days=1)).date() - first_day
header = f'Data from {first_day} to {last_day} - with duration of {duration}.'


# General informations about the data
#   Event Name frequency by color - tables with colors with rgb
nameFreq = create_agg(dfRemoveAllDay, ['Name','Colors'], 'Colors')
nameFreq['ColorDescription'] = nameFreq['Colors'].apply(lambda x: cts.colorId[str(x)][3])
nameFreq['ColorName'] = nameFreq['Colors'].apply(lambda x: cts.colorId[str(x)][0])
nameFreq['ColorRGB'] = nameFreq['Colors'].apply(lambda x: cts.colorId[str(x)][1])
nameFreq['ColorDescriptionName'] = nameFreq['ColorDescription'] + ' --- ' + nameFreq['ColorName']
nameFreq.drop(['Colors','ColorDescription','ColorName'], axis=1, inplace=True)
build.table(nameFreq, 'freq_table')
table_html = create_html.plots(['freq_table'], ['Events frequency divid by types'], [''])

#   Daily frequency of events - line plot
dfRemoveAllDay['DayMonth'] = dfRemoveAllDay['StartTimeStamp'].apply(lambda x: str(x.day)+'/'+str(x.month))
dailyFreqAll = create_agg(dfRemoveAllDay, ['DayMonth'], 'DayMonth', True)
dailyFreqStream = create_agg(only_colors(dfRemoveAllDay,[1]), ['DayMonth'], 'DayMonth', True)
dailyFreqSocial = create_agg(only_colors(dfRemoveAllDay,[3]), ['DayMonth'], 'DayMonth', True)
dailyFreqFitness = create_agg(only_colors(dfRemoveAllDay,[9]), ['DayMonth'], 'DayMonth', True)
dailyFreqUsefull = create_agg(only_colors(dfRemoveAllDay,[2, 5, 8, 10, 11]), ['DayMonth'], 'DayMonth', True)
build.subLine(dfRemoveAllDay, dailyFreqAll, dailyFreqStream, dailyFreqSocial, dailyFreqFitness, dailyFreqUsefull, 
           'daily_freq', 'DayMonth', 'count')
line1_html = create_html.plots(['daily_freq'], ['Daily frequency of events'], [''])

#   Week Day name frequency of events - line plot
dfRemoveAllDay['WeekDayName'] = dfRemoveAllDay['WeekDay'].apply(lambda x: cts.weekDayId[str(x)])
weekDayFreq = create_agg(dfRemoveAllDay, ['WeekDayName','WeekDay'], 'WeekDay').drop('WeekDay', axis=1)
weekDayStream = create_agg(only_colors(dfRemoveAllDay,[1]), ['WeekDayName','WeekDay'], 'WeekDay').drop('WeekDay', axis=1)
weekDaySocial = create_agg(only_colors(dfRemoveAllDay,[3]), ['WeekDayName','WeekDay'], 'WeekDay').drop('WeekDay', axis=1)
weekDayFitness = create_agg(only_colors(dfRemoveAllDay,[9]), ['WeekDayName','WeekDay'], 'WeekDay').drop('WeekDay', axis=1)
weekDayUsefull = create_agg(only_colors(dfRemoveAllDay,[2, 5, 8, 10, 11]), ['WeekDayName','WeekDay'], 'WeekDay').drop('WeekDay', axis=1)
build.subLine(dfRemoveAllDay, weekDayFreq, weekDayStream, weekDaySocial, weekDayFitness, weekDayUsefull, 
           'weekDay_freq', 'WeekDayName', 'count')
line2_html = create_html.plots(['weekDay_freq'], ['Frequency of events during the week days'], [''])


# Create the html plot pages for each event type
create_html.event(rest_visu.main(DATA), 'rest', header)
create_html.event(daily_visu.main(DATA), 'daily', header)
create_html.event(workout_visu.main(DATA), 'workout', header)
create_html.event(stream_visu.main(DATA), 'streaming', header)
create_html.event(impt_visu.main(DATA), 'important', header)
create_html.event(transpt_visu.main(DATA), 'transport', header)
create_html.event(resume_visu.main(DATA), 'resume', header)
create_html.event(social_visu.main(DATA), 'social', header)
create_html.event(all_visu.main(DATA), 'allDay', header)


# Create main html and its components
buttons = create_html.button(cts.events_type)
create_html.main(header, table_html, line1_html, line2_html, buttons)
