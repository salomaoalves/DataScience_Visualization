
# Dict about week day - key is datetime week day index, value is the week day name
weekDayId = {'0':'Monday', '1':'Tuesday', '2':'Wednesday', '3':'Thursday', 
             '4':'Friday', '5':'Saturday', '6':'Sunday'}

# Dict about the colors/event types - key is the color id according with Google Calender
                                # value is a list, with the color name, event type, rgb and description (desc is valid for -2022-,2023,...)
colorId = {'0': ['Default', '#039be5', 'daily', 'Sleep'], 
           '1': ['Lavender', '#7986cb', 'streaming', 'Streamings n TV time'], 
           '2': ['Sage', '#33b679', 'resume', 'Learning something with a course or anything else'],
           '3': ['Grape', '#8e24aa', 'social', 'Social Time'],
           '4': ['Flamingo', '#e67c73', 'transport', 'Transport type or Travel (TranspType or From to To)'], 
           '5': ['Banana', '#f6c026', 'important', 'Learn something - health and important stuffs'], 
           '6': ['Tangerine', '#f5511d', 'daily', 'Daily events - like Morning Mood, Lunch, Dinner'], 
           '7': ['Peacock', '#039be5', None, None], # it's also the Default color - Google Calender bug
           '8': ['Graphite', '#616161', 'resume', 'Code Projects'], 
           '9': ['Blueberry', '#3f51b5', 'workout', 'Workout, like Gym'], 
           '10': ['Basil', '#0b8043', 'resume', 'Learning something by myself'], 
           '11': ['Tomato', '#d60000', 'resume', 'Job - to earn $$']
           }

# Another dict about color, just to get the color id by its name
colorName2Id = {'Default': 0, 'Lavender': 1, 'Sage': 2, 'Grape': 3,
                'Flamingo': 4, 'Banana': 5, 'Tangerine': 6, 'Peacock': 7, 
                'Graphite': 8, 'Blueberry': 9, 'Basil': 10, 'Tomato': 11}

def print_color():
    '''Shows the characteristics of colors'''
    for k, v in colorId.items():
        print(f'Id {k} - color {v[0]} - rgb: {v[1]} - event type: {v[2]} - description: {v[3]}')


# List of all events types
events_type = ['allDay', 'daily', 'important', 'rest', 'resume', 'social', 'streaming', 'transport', 'workout']


# Constants to use throw the code
EVENTS_SEP = ' EVENTS------------------------------------------------------------------------\n'
#TXT_PATH = './Reports/Weeks/report23_0301:0312.txt'
TXT_PATH = './Reports/report_202402.txt'
DB_PATH = './GetData/Database/events2024.csv'
DB_FK_PATH = './Fake/fake_events.csv'
DB_FK_PATH_NEW = './Fake/fake_events_new_format.csv'
VISU_PATH = './Visu/fake/'
PLOT_PATH = VISU_PATH+'plots/'
PAGE_PATH = VISU_PATH+'pages/'
DISPLAY = 'l03' # 'l01: txt format' - 'l02: html format' - 'l03: data'
NEW_FORMAT = True # events without time measurement
FK_DATA = True


# Import data
import data as data
def load_data(load_type, day_one, day_second, prev_day, month, year, quarter):
    '''Get the events from a given date
        @load_type: type of load to be executed
        @day_one: 3tuple (YYYY,MM,DD) - inclusive
        @day_second: 3tuple (YYYY,MM,DD) - inclusive
        @prev_day: qty of days from search date to current day
         #0 for current day, 1 for yesterday, 2 for before yesterday and so on
        @month: month to be search - (1-12)
        @year: year to be search - (2018-current)
        @quarter: which quarter of the year - (1-4)'''

    # Get data
    if load_type=='all':
        df = data.read_db()
    elif load_type=='prev_day':
        df = data.get_data_by_prev_day(data.read_db(), prev_day)
    elif load_type=='week':
        df = data.get_data_by_week(data.read_db(), day_one)
    elif load_type=='month':
        df = data.get_data_by_month(data.read_db(), month, year)
    elif load_type=='year':
        df = data.get_data_by_year(data.read_db(), year)
    elif load_type=='period':
        df = data.get_date_period(data.read_db(), day_one, day_second)
    elif load_type=='quarter':
        df = data.get_date_by_quarter(data.read_db(), quarter)

    # Get quantity of days
    qty_days = len(df['StartTimeStamp'].dt.date.unique())

    return df, qty_days
DATA, DAYS = load_data('all', (2023,2,12), (2023,2,18), 0, 2, 2024, 1)