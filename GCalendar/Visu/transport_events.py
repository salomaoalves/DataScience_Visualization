
from Analytics import agg_colors, agg_report, aux_analytics
from Visu import build, common
from Visu import create_html
import pandas as pd
import calendar

def get_min(time):
    if time==0: return '00'
    else: return str(time)

def main(data):
    # Get and prepare the data
    data = agg_colors.get_flamingo(data)
    data_prep = common.prepare_data(data)
    data_prep_travel = data_prep[data_prep['Name'].str.contains('-')]
    data_prep_mov = data_prep[~(data_prep['Name'].str.contains('-'))]

    # Transport type used
    data_prep['transp_type'] = data['Name'].apply(lambda x: x.split(' - ')[0])
    freqName = data_prep[['transp_type']].value_counts().to_frame().reset_index()
    freq_html = '<div><h3>Transport type frequency</h3><ul>'
    for i in range(freqName.shape[0]):
        freq_html += '<li><strong>' + freqName.iloc[i,0] + '</strong> happens ' + \
            str(freqName.iloc[i,1]) + ' times</li>'
    freq_html += '</ul></div>'

    # Data description variables
    travel_html, mov_html = '<div><h3>Travel</h3>', '<div><h3>Displacement</h3>'

    # Create Travel Events descriptions
    travel_html += '<table style="width:50%">><tr><td>Transport used</td><td>Path</td><td>Departure</td>' + \
        '<td>Arrival</td><td>Duration</td></tr>'
    for _, row in data_prep_travel.iterrows():
        travel_html += '<tr><td>' + row['Name'].split(' - ')[0].capitalize() + '</td>' + \
            '<td>' + row['Name'].split(' - ')[1].title() + '</td>' + \
            '<td>' + str(row['StartTimeStamp'].day) + '/' + calendar.month_name[row['StartTimeStamp'].month] + \
                f' at {row["StartTimeStamp"].hour}:' + get_min(row["StartTimeStamp"].minute) + '</td>' + \
            '<td>' + str(row['EndTimeStamp'].day) + '/' + calendar.month_name[row['EndTimeStamp'].month] + \
                f' at {row["EndTimeStamp"].hour}:' + get_min(row["EndTimeStamp"].minute) + '</td>' + \
            f'<td>{row["duration"]:.1f} hour(s)</td></tr>'
    travel_html += '</table></div>'

    # Create Moviments Events descriptions
    _, _, df_sum, df_freq = aux_analytics.get_agg(data_prep_mov)
    mov_p, mov_per = '', ''
    for i in df_sum.index:       
        sum = df_sum.loc[i,'duration'].sum()
        str_freq = str(df_freq.loc[i,'duration'])
        avg = float(sum)/float(str_freq)
        mov_p += f'<p>Event {i.capitalize()}, repeats {str_freq} times in a total of {sum:.2f} hours' + \
            f', with average of {avg:.2f} hours or {(avg*60):.2f} minutes.</p>\n'

        # the events' periods
        data_temp = data_prep_mov[data_prep_mov['Name']==i].reset_index()
        mov_per += '<h4>' + i.capitalize() + '</h4><table style="width:20%"><tr><td>Departure</td><td>Arrival</td></tr>'
        for _, row in data_temp.iterrows():
            mov_per += '<tr>' + \
                '<td>' + str(row['StartTimeStamp'].day) + '/' + str(row['StartTimeStamp'].month) + \
                    f' at {row["StartTimeStamp"].hour}:' + get_min(row["StartTimeStamp"].minute) + '</td>' +\
                '<td>' + str(row['EndTimeStamp'].day) + '/' + str(row['EndTimeStamp'].month) + \
                    f' at {row["EndTimeStamp"].hour}:' + get_min(row["EndTimeStamp"].minute) + '</td></tr>'
        mov_per += '</table>'
    mov_html += mov_p + mov_per + '</div>'

    # Get the complete html
    html = '''
        <h2>Moviment Events</h2>
        <p>Events related with transportation, like inside a city or between them (travel).</p>
        ''' + freq_html + travel_html + mov_html

    return html
