from bokeh.io import output_notebook
from bokeh.plotting import figure, show, output_file
from bokeh.layouts import row, column
from bokeh.models import CustomJS, Slider, ColumnDataSource, CDSView, GroupFilter
from bokeh.plotting import reset_output

import numpy as np
import pandas as pd
import missingno as msno

result=['W','L','W','W','W','W','W','L','T','W']
home_team=['India','India','India','India','India','India','India','India','India','India']
oppo_team=['Australia','Australia','England','WestIndies','Pakistan','Pakistan','SriLanka','England','Newzealand','England']
matches=pd.DataFrame(data={'result':result,
                    'home_team':home_team,
                           'oppo_team':oppo_team})

print(matches)

source1=matches[matches['result']=='L'].groupby(['oppo_team'])['home_team'].count().sort_values().reset_index()
output_file('test_file')
fig = figure(title='Test Plot',y_range=[0,5],
            x_range=list(matches.oppo_team.unique()))
source_data= ColumnDataSource(source1)
fig.circle(x='oppo_team',y='home_team',source=source_data,size=20)

from bokeh.io import output_file, show
from bokeh.models.widgets import RadioButtonGroup
from bokeh.layouts import widgetbox, row
from bokeh.io import curdoc



def update():
    button_value= radio_button_group.active
    print('Button value  is : ', button_value)
    if button_value ==1:
        new_source=matches[matches['result']=='W'].groupby(['oppo_team'])['home_team'].count().sort_values().reset_index()
    else:
        new_source=matches[matches['result']=='L'].groupby(['oppo_team'])['home_team'].count().sort_values().reset_index()
    new_source_cds= ColumnDataSource(new_source)
    source_data.data=new_source_cds.data
    
radio_button_group = RadioButtonGroup(
        labels=['Loss', 'Win'], active=0)

radio_button_group.on_change('active', lambda attr, old, new: update())

# Make a row layout of widgetbox(slider) and plot and add it to the current document
layout = row(widgetbox(radio_button_group), fig)
curdoc().add_root(layout)