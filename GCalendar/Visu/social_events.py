from Analytics import agg_report
from Visu import build, common
from Visu import create_html

def main(data):
    # Get data to plot
    data = agg_report.get_social(data)
    data_prep = common.prepare_data(data)

    # Genarete the plots and its filename, description and title
    plots_names = ['social_day_bar', 'social_nameDay_bar']
    plots_title = ['General daily frequency', 'General day of the week frequency']
    plots_desc = ['', '']
    build.bar(data_prep, 'day', plots_names[0], ['Name','start_time'])
    build.bar(data_prep, 'name_day', plots_names[1], ['Name','start_time'])
    
    # Get the complete html plot
    html_plots = create_html.plots(plots_names, plots_title, plots_desc)
    html = '''
        <h2>Social Events</h2>
        <p>Events related with socials interactions</p>
        ''' + html_plots

    return html
