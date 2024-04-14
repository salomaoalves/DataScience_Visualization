import pandas as pd
from datetime import datetime, timedelta
import constants as cts
import pytz


## Read DB
def set_datetime(df):

    # Convert the dates and times cols to datetime64
    df['StartTimeStamp'] = pd.to_datetime(df['StartTimeStamp'], format='%Y-%m-%d %H:%M:%S')
    df['EndTimeStamp'] = pd.to_datetime(df['EndTimeStamp'], format='%Y-%m-%d %H:%M:%S')

    return df

def read_db():
    '''Get data using the constant for the db path'''

    # Read the data
    df = pd.read_csv(cts.DB_PATH, sep=',')

    return set_datetime(df)

def read_db_fake():
    '''Get data using the constant for the db path'''

    # Read the data
    if cts.NO_TIME_MEASUREMENT: df = pd.read_csv(cts.DB_FK_PATH_NEW, sep=',')
    else: df = pd.read_csv(cts.DB_FK_PATH, sep=',')

    return set_datetime(df)


## Special Filter

def get_data_by_prev_day(df, prev_days=0):
    '''Get the events from a given date
        @df: events data frame
        @prev_days: qty of days from search date to current day'''

    # Get search datetime
    current_date = datetime.now()
    data_date = current_date - timedelta(days=prev_days)

    # Make the filter by year, month and day
    data = df[df['StartTimeStamp'].dt.year == data_date.year] 
    data = data[data['StartTimeStamp'].dt.month == data_date.month]
    data = data[data['StartTimeStamp'].dt.day == data_date.day]

    return data

def get_data_by_week(df, first_day):
    '''Get the events from a given week month
        @df: events data frame
        @first_day: 3tuple (YYYY,MM,DD)'''

    # Get search datetime
    tz = pytz.timezone('America/Sao_Paulo')
    first_date = datetime(first_day[0],first_day[1],first_day[2],0,0,0)
    last_date = first_date + timedelta(weeks=1)

    # Make the date filter
    data = df[df['StartTimeStamp']>=first_date]    
    data = data[data['EndTimeStamp']<=last_date]

    return data

def get_data_by_month(df, search_month=0, search_year=0):
    '''Get the events from a given week month
        @df: events data frame
        @search_month: month to be search - between 1 and 12, if not, use the current month
        @search_year: year to be search - between 2018 and current year, if not, use the current year'''
    current_date = datetime.now()

    # Get search month
    if search_month > 0 and search_month < 13:
        month = search_month
    else:
        month = current_date.month

    # Get search year
    if search_year > 2017 and search_year < current_date.year+1:
        year = search_year
    else:
        year = current_date.year

    # Make the filter by month
    data = df[df['StartTimeStamp'].dt.month==month]
    data = data[data['StartTimeStamp'].dt.year==year]

    return data

def get_data_by_year(df, search_year=0):
    '''Get the events from a given week month
        @df: events data frame
        @search_year: year to be search - between 2018 and current year, if not, use the current year'''
    current_date = datetime.now()

    # Get search year
    if search_year > 2017 and search_year < current_date.year+1:
        year = search_year
    else:
        year = current_date.year

    # Make the filter by month
    data = df[df['StartTimeStamp'].dt.year==year]

    return data

def get_date_period(df, first_day, last_day):
    '''Get the events from a given week month
        @df: events data frame
        @first_day: 3tuple (YYYY,MM,DD) - inclusive
        @last_day: 3tuple (YYYY,MM,DD) - inclusive'''

    # Get search datetime
    tz = pytz.timezone('America/Sao_Paulo')
    first_date = datetime(first_day[0],first_day[1],first_day[2],0,0,0)
    last_date = datetime(last_day[0],last_day[1],last_day[2],0,0,0) + timedelta(days=1)

    # Make the date filter
    data = df[df['StartTimeStamp']>=first_date]    
    data = data[data['EndTimeStamp']<=last_date]

    return data


def get_date_by_quarter(df, quarter):
    '''Get the events from a given week month
        @df: events data frame
        @quarter: which quarter of the year - (1-4)'''

    # Make the date filter
    data = df[df['StartTimeStamp'].dt.quarter==quarter]    

    return data