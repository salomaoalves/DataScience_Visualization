from Analytics import agg_colors
from Visu import build, common
from Visu import create_html

def get_stats(data, event):
    data = data[data['Name'] == event]
    return [data['duration'].sum(), round(data['duration'].mean(),2), round(data['duration'].std(),2)]

def main(data):
    # Get data to plot
    data = agg_colors.get_lavender(data)
    data_prep = common.prepare_data(data)
    freqName = data_prep[['Name']].value_counts().to_frame().reset_index()

    # Genarete the plots and its filename, description and title
    plots_names = ['streaming_day_bar', 'streaming_nameDay_bar']
    plots_title = ['General daily frequency', 'Day of the week frequency']
    plots_desc = ['', '']
    build.bar(data_prep, 'day', plots_names[0], ['Name','start_time'])
    build.bar(data_prep, 'name_day', plots_names[1], ['Name','start_time'])

    # Get the complete html plot
    html_freq = '<h3>Frequency</h3><ul>'
    for i in range(freqName.shape[0]):
        stats = get_stats(data_prep, freqName.iloc[i,0])
        html_freq += '<li><strong>' + freqName.iloc[i,0] + '</strong> happens ' + \
            str(freqName.iloc[i,1]) + ' times - total of '+str(stats[0])+' hours '+ \
            ' - avg of '+str(stats[1])+' and std of '+str(stats[2])+'</li>'
    html_freq += '</ul>'
    html_plots = create_html.plots(plots_names, plots_title, plots_desc)
    html = '''
        <h2>Streaming Events</h2>
        <p>Events related with TV rsrsr</p>
        ''' + html_freq + html_plots

    return html