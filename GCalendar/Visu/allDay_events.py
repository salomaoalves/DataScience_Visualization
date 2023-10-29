from Analytics import agg_report
from Visu import common
import calendar

def get_min(time):
    if time==0: return '00'
    else: return str(time)

def main(data):
    # Get data to plot
    data = agg_report.get_all_day(data)
    data_prep = common.prepare_data(data)
    evts_name = data_prep.sort_values(by='Name')['Name'].unique()

    # Create All Day Events descriptions - for each allDay event
    allDay_html = ''
    for name in evts_name:
        df_temp = data_prep[data_prep['Name']==name].reset_index(drop=True)
        rowF = df_temp['StartTimeStamp'].iloc[0]
        rowL = df_temp['StartTimeStamp'].iloc[df_temp.shape[0]-1]
        duration = df_temp['duration'].sum()
        allDay_html += '<p>Event ' + name.capitalize() + ', between ' + \
            str(rowF.day) + '/' + calendar.month_name[rowF.month] + \
            ' to ' + str(rowL.day) + '/' + calendar.month_name[rowL.month] + \
            f', with duration of {duration/24:.0f} day(s).</p>\n'

    # Get the complete html plot
    html = '''
        <h2>All Day Events</h2>
        ''' + allDay_html

    return html
