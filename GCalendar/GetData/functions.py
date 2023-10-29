from datetime import datetime, date, time, timedelta
from calendar import isleap
import pytz, pandas as pd

EVENT_DB_PATH = './Database/events2023.csv'
METADATA_PATH = './Database/metadata.txt'

def get_search_date(year,month,month_final):
    tz = pytz.timezone('America/Sao_Paulo')
    first_day = datetime(year,month,1,0,0,0,tzinfo=tz)
    if month_final!=0 and month_final >= month:
        if month_final in [1, 3, 5, 7, 8, 10, 12]:
            last_day = datetime(year,month_final,31,0,0,0,tzinfo=tz)
        elif month_final in [4, 6, 9, 11]:
            last_day = datetime(year,month_final,30,0,0,0,tzinfo=tz)
        else:
            if isleap(year):
                last_day = datetime(year,month_final,29,0,0,0,tzinfo=tz)
            else:
                last_day = datetime(year,month_final,28,0,0,0,tzinfo=tz)
    else:
        last_day = first_day + timedelta(days=30)

    return first_day.isoformat(), (last_day+timedelta(days=1)).isoformat()


def get_data(service, first_day, last_day):
    '''Make a call and get all the events from a griven range - first and last day
        Also, get the information from the events and store it in a DataFrame
        @service: service to use to make the call
        @first_day: first day of the period - inclusive
        @last_day: last day of the period - exclusive'''
    
    # Getting events
    events_result = service.events().list(
        calendarId='primary', timeMin=first_day, timeMax=last_day,
        maxResults=2000, singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])

    # Stored
    data = []
    if not events:
        print(f'No events to be loaded for period: {first_day} --- {last_day}')
    for event in events:
        row = []
        try: # to check if there is some color
            color = event['colorId']
        except KeyError:
            color = '0'
        try: # to check if there is some name
            name = event['summary'].strip().lower()
        except KeyError:
            name = 'None'

        # Get start/end timestamp and transform into Date and Time format
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        date_start2 = date(int(start[:4]), int(start[5:7]), int(start[8:10]))
        date_start, date_end = start[:10], end[:10]
        if len(start)>10:
            time_start, time_end = start[11:19], end[11:19]
        else:
            time_start, time_end = '00:00:00', '00:00:00'
        tz = str(event['start'].get('timeZone', event['start'].get('date')))
        if len(tz) > 4 and tz[4]=='-': tz = 'America/Sao_Paulo'
        week_day = date_start2.weekday()
        week_year = date_start2.isocalendar()[1]
        week_month = (date_start2.day - 1) // 7 + 1

        # Only save the events that started on the first day
        if first_day>start:
            continue
        row.append(name)
        row.append(color)
        row.append(date_start+' '+time_start)
        row.append(date_end+' '+time_end)
        row.append(week_day)
        row.append(week_month)
        row.append(week_year)
        row.append(tz)
        data.append(row)

    # Build DataFrame w/ data
    col_name = ['Name','Colors','StartTimeStamp','EndTimeStamp',
                'WeekDay','WeekByMonth','WeekByYear','TimeZone']
    df = pd.DataFrame(data, columns=col_name)
    
    return df, col_name


def convert_events_layout(cols):
    '''To convert the database event layout, by add new cols
        @cols: list of 2tuple with col name and default value'''
    
    df = pd.read_csv(EVENT_DB_PATH, sep=',')
    for col in cols:
        df[col[0]] = [col[1]] * df.shape[0]
    df.to_csv(EVENT_DB_PATH, sep=',', index=False)


def transform_allDayEvents(df):
    '''Split the All Day Events into rows - so, a 4 days events will have 4 rows'''

    df_copy = df.copy()
    df_copy['StartTimeStamp'] = pd.to_datetime(df['StartTimeStamp'], format='%Y-%m-%d %H:%M:%S')
    df_copy['EndTimeStamp'] = pd.to_datetime(df['EndTimeStamp'], format='%Y-%m-%d %H:%M:%S')
    df_copy['duration'] = df_copy['EndTimeStamp']-df_copy['StartTimeStamp']
        
    # Separete All Day Events from the others
    df_all_day = df_copy[(df_copy['duration'].dt.total_seconds() // 86400) != 0]
    df_not_all_day = df_copy[(df_copy['duration'].dt.total_seconds() // 86400) == 0]

    # Transform them
    new_all_day = pd.DataFrame()
    for i in range(df_all_day.shape[0]):
        n_new_rows = df_all_day.iloc[i,-1].days
        for new_row_i in range(n_new_rows):
            start_date = df_all_day.iloc[i,2] + timedelta(days=new_row_i)
            end_date = df_all_day.iloc[i,2] + timedelta(days=new_row_i+1)
            # date specific info
            week_day = start_date.weekday()
            week_year = start_date.isocalendar()[1]
            week_month = (start_date.day - 1) // 7 + 1
            # create row
            new_row = pd.DataFrame({'Name': df_all_day.iloc[i,0], 'Colors': df_all_day.iloc[i,1], 
                                    'StartTimeStamp': start_date, 'EndTimeStamp': end_date,
                                    'WeekDay': week_day,'WeekByMonth': week_month,
                                    'WeekByYear': week_year,'TimeZone': df_all_day.iloc[i,7]
                                    }, index=[0])
            new_all_day = pd.concat([new_all_day,new_row])

    return pd.concat([df_not_all_day,new_all_day])

if __name__ == '__main__':
    #convert_events_layout([('new_col1',0),('new_col2','')])
    pass
