import bats_man_data_cleanpy
import numpy as np
from bokeh.models.widgets import RadioButtonGroup, RadioGroup
from bokeh.layouts import widgetbox, row

from bokeh.io import output_file,curdoc,show
from bokeh.plotting import figure, show, output_file
from bokeh.layouts import row, column
from bokeh.models import CustomJS, Slider, ColumnDataSource, CDSView, GroupFilter
from bokeh.plotting import reset_output

bats_man_data=bats_man_data_cleanpy.data_cleaning()

print(bats_man_data.head(2))

yr=max(bats_man_data.Year_bats)
bats_man_name_list=list(bats_man_data.Batsman.unique())
bats_man_name_init='Shikhar Dhawan'
bats_man_data_year=bats_man_data[(bats_man_data['Batsman']==bats_man_name_init) & (bats_man_data['Year_bats']==yr)].groupby(['Batsman','Year_bats','Match_ID'])['Runs'].sum().sort_values().reset_index().sort_values(by=['Match_ID'])
bats_man_data_year['cumruns']=bats_man_data_year['Runs'].cumsum()

data_cds=ColumnDataSource(bats_man_data_year)   

fig = figure(title='Player Performance Across the Seasons in a Year',
             y_range=[0,300],
             x_range=list(np.sort(bats_man_data_year['Match_ID'].unique()))
             )

fig.vbar(x='Match_ID',top='Runs',source=data_cds,width=0.2)
fig.xaxis.major_label_orientation = "vertical"

slider = Slider(start=min(bats_man_data.Year_bats), end=max(bats_man_data.Year_bats), step=1, value=min(bats_man_data.Year_bats), title='Year of Play')
radiogroup_batsman = RadioGroup(labels=bats_man_name_list, active=0)
#radio_button_group = RadioButtonGroup(labels=['Win', 'Loss','Tie'], active=0)

def update(attr,old,new):
  yr = slider.value
  print('Slider Value is : ', yr)
  
  selected_batsman=bats_man_name_list[radiogroup_batsman.active]
  print('Selected batsman is : ', selected_batsman)

  new_source=bats_man_data[(bats_man_data['Batsman']==selected_batsman) & (bats_man_data['Year_bats']==yr)].groupby(['Batsman','Year_bats','Match_ID'])['Runs'].sum().sort_values().reset_index().sort_values(by=['Match_ID'])

  new_data_cds=ColumnDataSource(new_source) 
  
  data_cds.data=new_data_cds.data

#  button_value= radio_button_group.active
#  print('Button value  is : ', button_value)
  
#  if button_value==0:
#         won_source=new_source[new_source['Result']=='won']
#         new_won_cds= ColumnDataSource(won_source)
#         total_cds.data=new_won_cds.data
#  if button_value==1:
#         lost_source=new_source[new_source['Result']=='lost']
#         new_lost_cds= ColumnDataSource(lost_source)
#         total_cds.data=new_lost_cds.data
#  if button_value==2:
#         tied_source=new_source[new_source['Result']=='tied']
#         new_tied_cds= ColumnDataSource(tied_source)
#         total_cds.data=new_tied_cds.data

  fig.title.text='%s Performance Across the Seasons in the Year %d' % (selected_batsman,yr)
  fig.x_range.factors=[]
  fig.x_range.factors=list(np.sort(new_source['Match_ID'].unique()))


    
#radio_button_group.on_change('active',lambda attr, old, new :update(attr, old, new))

slider.on_change('value', update)
radiogroup_batsman.on_change('active', update)

# Make a row layout of widgetbox(slider) and plot and add it to the current document
layout = row(column(widgetbox(slider),widgetbox(radiogroup_batsman)), fig)

curdoc().add_root(layout)
