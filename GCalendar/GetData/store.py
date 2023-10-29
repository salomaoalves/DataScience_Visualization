from functions import EVENT_DB_PATH, METADATA_PATH
from functions import get_search_date, get_data, transform_allDayEvents
from call_setup import get_calendar_service
from datetime import datetime, timedelta
import pytz, pandas as pd


def get_all_year(year):
    '''Stored all events of a year for a given year
        @year: year number YYYY'''

    # Make the GCalender connection
    service = get_calendar_service()

    # verificar se algum mes já está ingerido
    with open(METADATA_PATH, 'r') as f:
        metadata = f.read().split('\n')
    new_df = event_data = pd.read_csv(EVENT_DB_PATH, sep=',')
    if len(metadata[1]) > 0:
        year_ingested = [int(year_meta) for year_meta in metadata[1].split(',')]
    else:
        year_ingested = []

    # Year already ingested
    if year in year_ingested or year>=datetime.now().year:
        print(f'Year {year} is already stored or is the current year')
        return

    for month in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]:
        # Getting period
        first_day, last_day = get_search_date(year,month,month)
    
        # Get events
        df, col_name = get_data(service, first_day, last_day)
        df = transform_allDayEvents(df) #each day is a row
        new_df = pd.concat([new_df, df])

    # Build new metadata    
    year_ingested.append(year)
    new_year = [str(year_meta) for year_meta in year_ingested]
    new_metadata = (f'{metadata[0]}\n' +          # Last datetime ingested
                    f'{",".join(new_year)}\n' +   # Year with all month already ingested
                    f'{",".join(col_name)}\n')    # DataFrame Columns

    # Stored the metadata and data
    new_df.to_csv(EVENT_DB_PATH, sep=',', index=False)
    with open(METADATA_PATH, 'w') as f:
        f.write(new_metadata)


def update_current_year():
    '''Update the events of the current year
        So, until the current day, all events will be stored'''

    # Make the GCalender connection
    service = get_calendar_service()

    # verificar se algum mes já está ingerido
    with open(METADATA_PATH, 'r') as f:
        metadata = f.read().split('\n')
    new_df = event_data = pd.read_csv(EVENT_DB_PATH, sep=',')

    # First (inclusive) and last (exclusive) date to get events
    last_update_date = datetime.strptime(metadata[0].split('.')[0], '%Y-%m-%d %H:%M:%S')
    current_date, tz = datetime.now(), pytz.timezone('America/Sao_Paulo')
    first_day = datetime(last_update_date.year,last_update_date.month,last_update_date.day,0,0,0,tzinfo=tz).isoformat()
    last_day = datetime(current_date.year,current_date.month,current_date.day,0,0,0,tzinfo=tz).isoformat()
    
    # Everything is already updated
    if (current_date - last_update_date).days == -1:
        print('Everything is already updated')
        return 

    # Get events for period smaller them 30 days
    if (current_date - last_update_date).days < 31:
        df, col_name = get_data(service, first_day, last_day)
        df = transform_allDayEvents(df) #each day is a row
        new_df = pd.concat([event_data, df])

    # Get events for period bigger them 35 days but in batch of 30 days
    else:
        # Initialize batch dates and flag to alert when is finished
        start_date, is_done = last_update_date, False
        end_date = start_date + timedelta(days=30)

        # Get event in batch of 30 days
        while (current_date - end_date).days >= 0:
            first_day = datetime(start_date.year,start_date.month,start_date.day,0,0,0,tzinfo=tz).isoformat()
            last_day = datetime(end_date.year,end_date.month,end_date.day,0,0,0,tzinfo=tz).isoformat()

            df, col_name = get_data(service, first_day, last_day)
            df = transform_allDayEvents(df) #each day is a row
            new_df = pd.concat([new_df, df])

            # Update batch dates and the finished flag
            start_date = end_date
            end_date = start_date + timedelta(days=30)
            if (current_date - end_date).days==0:
                is_done = True #last batch had 30 days
        
        # Last batch has less them 30 days to colect
        if not is_done:
            first_day = datetime(start_date.year,start_date.month,start_date.day,0,0,0,tzinfo=tz).isoformat()
            last_day = datetime(current_date.year,current_date.month,current_date.day,0,0,0,tzinfo=tz).isoformat()
            df, col_name = get_data(service, first_day, last_day)
            df = transform_allDayEvents(df) #each day is a row
            new_df = pd.concat([new_df, df])

    # Build new metadata    
    new_metadata = (str(datetime.now())+'\n' +    # Last datetime ingested
                    f'{metadata[1]}\n' +          # Year with all month already ingested
                    f'{",".join(col_name)}\n')    # DataFrame Columns

    # Stored the metadata and data
    new_df.to_csv(EVENT_DB_PATH, sep=',', index=False)
    with open(METADATA_PATH, 'w') as f:
        f.write(new_metadata)


def get_specif_date(first_day, last_day, db_name):
    '''Get all event for a period of time - [first_day, last_day[
          For less than 30 days and store in a new db
        @first_day: 3tuple (YYYY,MM,DD)
        @last_day: 3tuple (YYYY,MM,DD)
        @db_name: str, database name'''

    # Make the GCalender connection
    service = get_calendar_service()

    # First (inclusive) and last (exclusive) date to get events
    tz = pytz.timezone('America/Sao_Paulo')
    first_day = datetime(first_day[0],first_day[1],first_day[2],0,0,0,tzinfo=tz).isoformat()
    last_day = datetime(last_day[0],last_day[1],last_day[2],0,0,0,tzinfo=tz).isoformat()

    # Get events
    df, _ = get_data(service, first_day, last_day)
    df = transform_allDayEvents(df) #each day is a row

    # Stored the data
    df.to_csv(db_name, sep=',', index=False)

if __name__ == '__main__':
    update_current_year()
    # get_all_year(2022)
    #get_specif_date((2023,5,29),(2023,6,5),'./Database/perfect_week.csv')
    pass