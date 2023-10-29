import plotly.graph_objs as go
from plotly.offline import plot
import numpy as np
from calendar import isleap
from plotly.subplots import make_subplots
import constants as cts

days_of_week_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

def get_hover_text(cols):
    hover_txt = ''
    for i,col_ in enumerate(cols):
        hover_txt += '<br>' + col_.replace('_',' ').capitalize() + ': %{customdata[' + str(i) + ']}'
    return hover_txt

def get_range_dates(df):
    days_remove = ['30/2','31/2','31/4','31/5','31/9','31/11']
    if not isleap(df['StartTimeStamp'].min().day): days_remove.append('29/2')
    days, first_month, second_month = [], df['StartTimeStamp'].min().month, df['StartTimeStamp'].max().month
    for month in range(first_month, second_month+1):
        if month == first_month: days += [str(i)+'/'+str(month) for i in range(df['StartTimeStamp'].min().day, 31)]
        elif month == second_month: days += [str(i)+'/'+str(month) for i in range(1, df['StartTimeStamp'].max().day+1)]
        else: days += [str(i)+'/'+str(month) for i in range(1, 31)]
    return [i for i in days if i not in days_remove]



def subBar(data, plot_name, hover_cols, evt):
    fig = make_subplots(rows=1, cols=2, subplot_titles=(evt+' daily', evt+' per day of week'))

    fig.add_trace(
        go.Bar(x=data.loc[:,'day'], y=data.loc[:,"duration"], customdata=data[hover_cols],
               hovertemplate='day/duration: %{x}---%{y}' + get_hover_text(hover_cols)),
        row=1, col=1)

    fig.add_trace(
        go.Bar(x=data.loc[:,'name_day'], y=data.loc[:,"duration"], customdata=data[hover_cols],
               hovertemplate='name_day/duration: %{x}---%{y}' + get_hover_text(hover_cols)),
        row=1, col=2)

    #fig.update_layout(height=600, width=800, title_text="Side By Side Subplots")
    fig.update_layout(showlegend=False)
    if data.shape[0]!=0:
        fig.update_xaxes(categoryorder='array', categoryarray=get_range_dates(data), row=1, col=1)
        fig.update_xaxes(categoryorder='array', categoryarray=days_of_week_order, row=1, col=2)
    plot(fig, filename=cts.PLOT_PATH+plot_name+'.html', auto_open=False)


def bar(data, col, plot_name, hover_cols):    
    graphic = [go.Bar(x=data.loc[:,col], y=data.loc[:,"duration"], customdata=data[hover_cols],
                      hovertemplate=col+'/duration: %{x}---%{y}' + get_hover_text(hover_cols)
                      )]
    fig = go.Figure(data=graphic, layout=go.Layout(barmode = 'group'))

    # Axis order
    if data.shape[0]!=0 and col=='day':
        days = get_range_dates(data)
        fig.update_xaxes(categoryorder='array', categoryarray=days)
    if data.shape[0]!=0 and col=='name_day':
        fig.update_xaxes(categoryorder='array', categoryarray=days_of_week_order)

    plot(fig, filename=cts.PLOT_PATH+plot_name+'.html', auto_open=False)


def stacked_bar(df, col, plot_name, hover_cols):
    data, unique_name = [], df.loc[:,'Name'].unique()
    sort_names = list(np.sort(unique_name))

    # Create the plots
    for name in unique_name:
        df_temp = df[df['Name'] == name]
        data.append(go.Bar(x=df_temp.loc[:,col], y=df_temp.loc[:,"duration"], name=name, 
                           legendrank=sort_names.index(name), customdata=df[hover_cols],
                           hovertemplate=col+'/duration: %{x}---%{y}' + get_hover_text(hover_cols)))
    fig = go.Figure(data = data, layout = go.Layout(barmode = 'group'))

    # Axis order
    if df.shape[0]!=0 and col=='day':
        days = get_range_dates(df)
        fig.update_xaxes(categoryorder='array', categoryarray=days)
    if df.shape[0]!=0 and col=='name_day':
        fig.update_xaxes(categoryorder='array', categoryarray=days_of_week_order)

    plot(fig, filename=cts.PLOT_PATH+plot_name+'.html', auto_open=False)


def subLine(data, data1, data2, data3, data4, data5, plot_name, col_x, col_y):
    fig = make_subplots(rows=2, cols=1)
    fig.add_trace(go.Scatter(
        x=data1.loc[:,col_x], y=data1.loc[:,col_y], #line=dict(color='royalblue', width=4),
        mode='lines+markers', name='Everyone', hovertemplate=col_x+'/frequency: %{x} --- %{y}'),
    row=1, col=1)
    fig.add_trace(go.Scatter(
        x=data2.loc[:,col_x], y=data2.loc[:,col_y], 
        mode='lines+markers', name='Streaming', hovertemplate=col_x+'/frequency: %{x} --- %{y}'),
    row=2, col=1)
    fig.add_trace(go.Scatter(
        x=data3.loc[:,col_x], y=data3.loc[:,col_y], 
        mode='lines+markers', name='Social', hovertemplate=col_x+'/frequency: %{x} --- %{y}'),
    row=2, col=1)
    fig.add_trace(go.Scatter(
        x=data4.loc[:,col_x], y=data4.loc[:,col_y], 
        mode='lines+markers', name='Fitness', hovertemplate=col_x+'/frequency: %{x} --- %{y}'),
    row=1, col=1)
    fig.add_trace(go.Scatter(
        x=data5.loc[:,col_x], y=data5.loc[:,col_y], 
        mode='lines+markers', name='Usefull', hovertemplate=col_x+'/frequency: %{x} --- %{y}'),
    row=1, col=1)

    # Axis order
    if col_x=='DayMonth': 
        fig.update_xaxes(categoryorder='array', categoryarray=get_range_dates(data), row=1, col=1)
        fig.update_xaxes(categoryorder='array', categoryarray=get_range_dates(data), row=2, col=1)
    if col_x=='WeekDayName':
        fig.update_xaxes(categoryorder='array', categoryarray=days_of_week_order, row=1, col=1)
        fig.update_xaxes(categoryorder='array', categoryarray=days_of_week_order, row=2, col=1)

    plot(fig, filename=cts.PLOT_PATH+plot_name+'.html', auto_open=False)


def table(df, plot_name):
    fig = go.Figure(data=[go.Table(
        columnwidth = [50, 25, 100],
        header=dict(values=list(df.drop('ColorRGB', axis=1).columns),
                    line_color='darkslategray',
                    font=dict(color='white', size=15)),
        cells=dict(values=[df.Name, df.loc[:,'count'], df.ColorDescriptionName],
                            fill_color=[list(df.ColorRGB)*3],
                            line_color='darkslategray',
                            font = dict(color = '#000000', size = 11))
        )])
    fig.update_layout(width=750, height=400)
    plot(fig, filename=cts.PLOT_PATH+plot_name+'.html', auto_open=False)
