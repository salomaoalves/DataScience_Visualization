
from Analytics import agg_colors, agg_report
from Visu import build, common
from Visu import create_html

def main(data):
    # Get data to plot
    data_earn, data_learn = agg_colors.get_tomato(data), agg_report.get_main(data)
    dataPrep_earn, dataPrep_learn = common.prepare_data(data_earn), common.prepare_data(data_learn)
    dataPrep_learn.sort_values('Colors').reset_index(inplace=True)

    # Plots for earn events
    plots_names = ['resume_earn_day_bar', 'resume_earn_nameDay_bar']
    plots_title = ['Earn daily frequency', 'Earn day of the week frequency']
    plots_desc = ['', '']
    build.bar(dataPrep_earn, 'day', plots_names[0], ['Name','start_time'])
    build.bar(dataPrep_earn, 'name_day', plots_names[1], ['Name','start_time'])

    # Plots for learn events
    plots_names += ['resume_learn_day_bar', 'resume_learn_nameDay_bar']
    plots_title += ['Learn daily frequency', 'Learn day of the week frequency']
    plots_desc += ['', '']
    build.bar(dataPrep_learn, 'day', plots_names[2], ['Name','start_time'])
    build.bar(dataPrep_learn, 'name_day', plots_names[3], ['Name','start_time'])

    # Frequency table
    freqEarnName = dataPrep_earn[['Name']].value_counts().to_frame().reset_index()
    html_freq = '<h3>Frequency</h3><h4>Earn events</h4><ul>'
    for i in range(freqEarnName.shape[0]):
        html_freq += '<li><strong>' + freqEarnName.iloc[i,0] + '</strong> happens ' + \
            str(freqEarnName.iloc[i,1]) + ' times</li>'
    html_freq += '</ul>'
    freqLearnName = dataPrep_learn[['Name']].value_counts().to_frame().reset_index()
    html_freq += '<h4>Learn events</h4><ul>'
    for i in range(freqLearnName.shape[0]):
        html_freq += '<li><strong>' + freqLearnName.iloc[i,0] + '</strong> happens ' + \
            str(freqLearnName.iloc[i,1]) + ' times</li>'
    html_freq += '</ul>'
    
    # Get the complete html plot
    html_plots = create_html.plots(plots_names, plots_title, plots_desc)
    html = '''
        <h2>Daily Events</h2>
        <p>Events related with food</p>
        ''' + html_freq + html_plots

    return html
