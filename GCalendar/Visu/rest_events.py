
from Analytics import agg_report
from Visu import build, common
from Visu import create_html
import pandas as pd

def main(data):
    # Get and prepare data to plot
    data = pd.concat([agg_report.get_sleep(data), agg_report.get_free(data)])
    data_prep = common.prepare_data(data)
    data_prep = data_prep[data_prep['duration']>0]

    # Genarete the plots for sleep to,e
    plots_names, plots_desc, plots_title = ['rest_sleep_bar'], [''], ['Sleep daily frequency']
    build.bar(data_prep[data_prep['Name'] == 'sleep'], 'day_end', plots_names[0], ['Name','start_time'])
    
    # Genarete the plots for free time
    plots_names += ['rest_nameDayFree_bar','rest_dayFree_bar']
    plots_desc += ['','']
    plots_title += ['Free week days frequency', 'Free daily frequency']
    build.bar(data_prep[data_prep['Name'] == 'free'], 'name_day', plots_names[2], ['Name','start_time'])
    build.bar(data_prep[data_prep['Name'] == 'free'], 'day', plots_names[1], ['Name','start_time'])
    
    # Get the complete html plot
    html_plots = create_html.plots(plots_names, plots_title, plots_desc)
    html = '''
        <h2>Rest Events</h2>
        <p>Events related with Sleep and Free Time</p>
        ''' + html_plots

    return html