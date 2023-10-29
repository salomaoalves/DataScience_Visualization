import constants as cts


def plots(plots, plots_title, plots_desc):
    html_plot = ''
    if len(plots) == 0:
        pass
    for i, plot in enumerate(plots):
        with open(cts.PLOT_PATH+plot+'.html', 'r') as f:
            load_plots = f.read()
        html_plot += '''
            <h3>''' + plots_title[i] + '''</h3>
            ''' + load_plots + '''
            <p>''' + plots_desc[i] + '''</p>
            '''
    return html_plot


def save_html(str, name):
    with open(cts.PAGE_PATH+name+'.html', 'w', encoding = 'utf8') as f:
        f.write(str)


def event(html_plot, output_name, header):
    '''Create the html structure for a event - its page
        @html_plot: html string of the plot to be displayed
        @output_name: str with the event name
        @header: str with date range and duration'''

    html_str = '''
    <!doctype html>
    <html>
        <head> 
            <meta charset="UTF-8">
            <title>GCalender Dashboard - '''+output_name+'''</title>
            <style>body{ margin:0 100; background:whitesmoke; }</style>
        </head>
        <body>
            <h1>Plots and more plots...</h1>
            <p>'''+header+'''</p>
            ''' + html_plot + '''
        </body>
    </html>'''

    save_html(html_str, output_name)


def button(events):
    html_str = ''
    for evnt in events:
        html_str += '''
            <a href="./'''+evnt+'''.html">
            <button>'''+evnt+'''</button>
        </a>'''
    return html_str


def main(header, html_table, html_line1, html_line2, buttons):
    '''Create the html structure for a event
        @header: str with date range and duration
        @html_table: html string with event name frequency
        @html_line1: html plot line for event frequency daily
        @html_line2: html plot line for event frequency per week day
        @buttons: html string with buttons to go to a specific event plot page'''

    html_str = '''
    <!doctype html>
    <html>
        <head> 
            <meta charset="UTF-8">
            <title>GCalender Dashboard</title>
            <style>body{ margin:0 100; background:whitesmoke; }</style>
        </head>
        <body>
            <h1>Dashboard main page</h1>
            <p>'''+header+'''</p>
            <h2>Events Frequency Table</h2>
            <p>Separeted by color, its show how much a certain event happens during the period.</p>
            ''' + html_table + '''
            <h2>Daily Frequency Line</h2>
            <p>A line plot with the frequency (daily) of some events type.</p>
            ''' + html_line1 + '''
            <h2>Week day Frequency Line</h2>
            <p>A line plot with the frequency (per week day) of some events type.</p>
            ''' + html_line2 + '''
            <h2>Events plots pages</h2>
            <p>Click in one of the button to go to another page, with more detailed information about that event.</p>
            ''' + buttons + '''
        </body>
    </html>'''

    save_html(html_str, 'main')
