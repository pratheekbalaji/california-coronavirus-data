import datetime as dt
from datetime import date
import pandas as pd
import numpy as np
from bokeh.plotting import figure, output_file, ColumnDataSource, curdoc
from bokeh.io import curdoc
from bokeh.models import HoverTool, FactorRange, Label
from bokeh.models import DatePicker, WidgetBox, Tabs, Panel, TextInput
from bokeh.transform import factor_cmap
from bokeh.layouts import column, row


def tab1():
    data = pd.read_csv('latimes-state-totals.csv')
    data['date_time'] = pd.to_datetime(data['date'])
    max_date = max(data['date_time']).date()
    data = data[data['date_time'].dt.month == 8]
    p = figure(y_axis_label='New cases', title='New confirmed cases of Coronavirus in CA on August',
               x_axis_type='datetime')
    r = p.line('date_time', 'new_confirmed_cases', source=data)
    p.add_tools(HoverTool(
        tooltips=[
            ('date', "@date_time{%Y-%m-%d}"),
            ('new cases', "@new_confirmed_cases")
        ],
        formatters={'@date_time': 'datetime'}
    ))

    label= Label(x=18, y=-150, x_units='screen', text="Source of data: latimes-state-totals.csv \t "
                                                       "Date of last update{}".format(max_date),
                   render_mode='css', y_units='screen')
    p.add_layout(label)
    tab = Panel(child=p, title='New covid cases in California on a particular day in August')
    return tab


def tab2():
    data_ethinicity = pd.read_csv('cdph-race-ethnicity.csv')
    data_ethinicity['date_time'] = pd.to_datetime(data_ethinicity['date'])
    max_date = max(data_ethinicity['date_time']).date()

    data_ethinicity = data_ethinicity[(data_ethinicity['age'] == 'all')]
    ratios = ['cases', 'general population']
    races = data_ethinicity['race'].unique()
    x = [(race, ratio) for race in races for ratio in ratios]

    def create_dataset(df):
        counts = sum(zip(df['confirmed_cases_percent'], df['population_percent']), ())
        source = ColumnDataSource(data=dict(x=x, counts=counts))
        return source

    def create_plot(source):
        p = figure(x_range=FactorRange(*x),
                   title='Ratio of cases by race to the general population',
                   y_axis_label='Percentage')

        p.vbar(x='x', top='counts', width=0.9, source=source, line_color="white",
               fill_color=factor_cmap('x', factors=ratios, start=1, end=2,palette=['yellow','orange']))
        p.y_range.start = 0

        p.xaxis.major_label_orientation = 1


        label = Label(x=18, y=-150,x_units='screen', text="Source of data: cdph-race-ethnicity.csv \n "
                                                            "Date of last update {}".format(max_date),
                       render_mode='css', y_units='screen')
        p.add_layout(label)
        return p

    def callback(attr, old, new):
        update_src = create_dataset(data_ethinicity[(data_ethinicity['date_time'] ==date_picker.value)])
        src.data.update(update_src.data)


    src = create_dataset(data_ethinicity[(data_ethinicity['date_time'] == '2020-05-15')])
    p = create_plot(src)
    date_picker = DatePicker(title=' Choose a date ', min_date=min(data_ethinicity['date_time']).date(),
                             max_date=max(data_ethinicity['date_time']).date(),value='2020-05-15')
    date_picker.on_change('value', callback)
    controls = WidgetBox(date_picker)
    layout = row(controls, p)
    tab = Panel(child=layout, title='Percentage of cases by race')
    return tab

def tab3():
    data_ethinicity = pd.read_csv('cdph-race-ethnicity.csv')
    data_ethinicity['date_time'] = pd.to_datetime(data_ethinicity['date'])
    max_date = max(data_ethinicity['date_time']).date()

    data_ethinicity = data_ethinicity[(data_ethinicity['age'] == 'all')]
    ratios = ['deaths cases', 'general population']
    races = data_ethinicity['race'].unique()
    x = [(race, ratio) for race in races for ratio in ratios]

    def create_dataset(df):
        counts = sum(zip(df['deaths_percent'], df['population_percent']), ())
        source = ColumnDataSource(data=dict(x=x, counts=counts))
        return source

    def create_plot(source):
        p = figure(x_range=FactorRange(*x),
                   title='Ratio of deaths by race to the general population',
                   y_axis_label='Percentage')

        p.vbar(x='x', top='counts', width=0.9, source=source, line_color="white",
               fill_color=factor_cmap('x', factors=ratios, start=1, end=2, palette=['yellow', 'orange']))
        p.y_range.start = 0

        p.xaxis.major_label_orientation = 1

        label = Label(x=18, y=-150, x_units='screen', text="Source of data: cdph-race-ethnicity.csv \n "
                                                           "Date of last update {}".format(max_date),
                      render_mode='css', y_units='screen')
        p.add_layout(label)
        return p

    def callback(attr, old, new):
        update_src = create_dataset(data_ethinicity[(data_ethinicity['date_time'] == date_picker.value)])
        src.data.update(update_src.data)

    src = create_dataset(data_ethinicity[(data_ethinicity['date_time'] == '2020-05-15')])
    p = create_plot(src)
    date_picker = DatePicker(title=' Choose a date ', min_date=min(data_ethinicity['date_time']).date(),
                             max_date=max(data_ethinicity['date_time']).date(), value='2020-05-15')
    date_picker.on_change('value', callback)
    controls = WidgetBox(date_picker)
    layout = row(controls, p)
    tab = Panel(child=layout, title='Percentage of deaths by race')
    return tab


tab1 = tab1()
tab2 = tab2()
tab3 = tab3()
# Put all the tabs into one application
tabs = Tabs(tabs=[tab1, tab2, tab3])
curdoc().add_root(tabs)