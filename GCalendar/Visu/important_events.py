from Analytics import agg_colors
from Visu import build, common
from Visu import create_html

def count_name(data):
    return data[['Name']].value_counts().to_frame().reset_index()

def split_data(data):
    dfRead = data[data['Name'].str.contains('read')]
    dfPodcast = data[data['Name'].str.contains('podcast')]
    dfOthers = data[~(data['Name'].str.contains(r"read|podcast"))]
    return [(dfRead, count_name(dfRead)),
            (dfPodcast, count_name(dfPodcast)),
            (dfOthers, count_name(dfOthers))]

def create_list(freq):
    list = '<ul>'
    for i in range(freq.shape[0]):
        list += '<li><strong>' + freq.iloc[i,0] + '</strong> happens ' + \
            str(freq.iloc[i,1]) + ' times</li>'
    list += '</ul>'
    return list

def main(data):
    # Get data to plot
    data = agg_colors.get_banana(data)
    data_prep = common.prepare_data(data)
    data_split = split_data(data_prep)

    # Genarete the plots and its filename, description and title
    plots_names = ['important_others_bar', 'important_read_subplot', 'important_podcast_subplot']#important_name_day_hourly
    plots_title = ['Important evts daily frequency', 'Read info', 'Podcast info']
    plots_desc = ['Except read n podcast.', '', '']
    build.bar(data_split[2][0], 'day', plots_names[0], ['Name','start_time'])
    build.subBar(data_split[0][0], plots_names[1], ['Name','start_time'], 'Read')
    build.subBar(data_split[1][0], plots_names[2], ['Name','start_time'], 'Podcast')
    #common.hourly(data_prep[data_prep['Name'].str.contains('Read')], 'name_day', plots_names[2]) # per hour - the one in Notion. for read and podcast, not others
    
    # Frequency table
    html_freq = '''<h3>Frequency</h3><h4>Read</h4>''' + create_list(data_split[0][1]) + '''
        <h4>Podcast</h4>''' + create_list(data_split[1][1]) + '''
        <h4>Others</h4>''' + create_list(data_split[2][1])

    # Get the complete html
    html_plots = create_html.plots(plots_names, plots_title, plots_desc)
    html = '''
        <h2>Important Events</h2>
        <p>Events related with importants tasks/stuffs, health, smooth learning ...</p>
        ''' + html_freq + html_plots

    return html
