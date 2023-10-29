
from Analytics import agg_colors
from Visu import build, common
from Visu import create_html

def main(data):
    # Get data
    data = agg_colors.get_tangerine(data)
    data_prep = common.prepare_data(data)

    # Genarete general plots
    plots_names = ['daily_day_bar', 'daily_day_stackedbar', 'daily_nameDay_stackedbar']
    plots_title = ['General frequency per day of the month'] * 2 + ['Day of the week frequency']
    plots_desc = ['', '', '']
    build.bar(data_prep, 'day', plots_names[0], ['Name','start_time'])
    build.stacked_bar(data_prep, 'day', plots_names[1], ['Name','start_time'])
    build.stacked_bar(data_prep, 'name_day', plots_names[2], ['Name','start_time'])

    # Frequency table
    freqName = data[['Name']].value_counts().to_frame().reset_index()
    html_freq = '<h3>Frequency</h3><ul>'
    for i in range(freqName.shape[0]):
        html_freq += '<li><strong>' + freqName.iloc[i,0] + '</strong> happens ' + \
            str(freqName.iloc[i,1]) + ' times</li>'
    html_freq += '</ul>'

    # Get the complete html
    html_plots = create_html.plots(plots_names, plots_title, plots_desc)
    html = '''
        <h2>Daily Events</h2>
        <p>Events related with food and meals.</p>
        ''' + html_freq + html_plots

    return html