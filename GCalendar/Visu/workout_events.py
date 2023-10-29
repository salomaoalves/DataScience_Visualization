
from Analytics import agg_colors
from Visu import build, common
from Visu import create_html

def main(data):
    # Get data to plot
    data = agg_colors.get_blueberry(data)
    data_prep = common.prepare_data(data)

    # Separeted by some eventy types
    data_gym = data_prep[data_prep['Name'].str.contains("gym")]
    data_run = data_prep[data_prep['Name'].str.contains(r"run|walk")]
    data_others = data_prep[~(data_prep['Name'].str.contains(r"run|walk|gym"))]

    # Frequency set
    freqName = data_prep[['Name']].value_counts().to_frame().reset_index()

    # Plots
    plots_names = ['workout_day_bar','workout_gym_bar','workout_run_stackedbar','workout_other_stackedbar']
    plots_title = ['General daily frequency', 'Gym daily frequency', 'Run/Walk daily frequency', 'Others daily frequency']
    plots_desc = ['', '', '', '']
    build.bar(data_prep, 'day', plots_names[0], ['Name','start_time'])
    build.bar(data_gym, 'day', plots_names[1], ['Name','start_time'])
    build.stacked_bar(data_run, 'day', plots_names[2], ['Name','start_time'])
    build.stacked_bar(data_others, 'day', plots_names[3], ['Name','start_time'])

    # Frequency by quarter of hour per name event - do only for gym and run (latest update)
    # the one in notion

    # Get the complete html plot
    html_freq = '<h3>Frequency</h3><ul>'
    for i in range(freqName.shape[0]):
        html_freq += '<li><strong>' + freqName.iloc[i,0] + '</strong> happens ' + \
            str(freqName.iloc[i,1]) + ' times</li>'
    html_freq += '</ul>'
    html_plots = create_html.plots(plots_names, plots_title, plots_desc)
    html = '''
        <h2>Workout Events</h2>
        <p>Events related body moviment, exercices</p>
        ''' + html_freq + html_plots

    return html