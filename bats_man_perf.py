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
opposition_list=list(bats_man_data.Opposition_bats.unique())
opposition_list.insert(0,'All')

bats_man_name_init=bats_man_name_list[0]
bats_man_data_year=bats_man_data[(bats_man_data['Batsman']==bats_man_name_init) & (bats_man_data['Year_bats']==yr)].groupby(['Match_ID','4s'])['Runs'].sum().sort_values().reset_index().sort_values(by=['Match_ID'])
bats_man_data_year.rename({'4s': 'shots'},axis='columns',inplace=True)

runs_cds=ColumnDataSource(bats_man_data_year[['Match_ID','Runs']])   
shots_cds=ColumnDataSource(bats_man_data_year[['Match_ID','shots']])

fig = figure(title='Player Performance Across the Seasons in a Year',
             y_range=[0,300],
             x_range=list(np.sort(bats_man_data_year['Match_ID'].unique()))
             )

fig.line(x='Match_ID',y='Runs',source=runs_cds,line_width=4,line_color="blue")
fig.line(x='Match_ID',y='shots',source=shots_cds,line_width=4,line_color="Orange")
fig.xaxis.major_label_orientation = "vertical"

slider = Slider(start=min(bats_man_data.Year_bats), end=max(bats_man_data.Year_bats), step=1, value=min(bats_man_data.Year_bats), title='Year of Play')
radiogroup_batsman = RadioGroup(labels=bats_man_name_list, active=0)
run_type = RadioButtonGroup(labels=['Number of 4s','Number of 6s'], active=0)
radiogroup_oppo= RadioGroup(labels=opposition_list, active=0)

def update(attr,old,new):
  yr1 = slider.value
  print('Slider Value is : ', yr1)
  
  selected_batsman=bats_man_name_list[radiogroup_batsman.active]
  print('Selected batsman is : ', selected_batsman)
  
  selected_oppo=opposition_list[radiogroup_oppo.active]
  print('Selected Opposition Team is : ', selected_oppo)

  button_value= run_type.active
  print('Button value  is : ', button_value)
  if selected_oppo == 'All':

    if button_value==0:
      new_source=bats_man_data[(bats_man_data['Batsman']==selected_batsman) & (bats_man_data['Year_bats']==yr1)].groupby(['Match_ID','4s'])['Runs'].sum().sort_values().reset_index().sort_values(by=['Match_ID'])
      new_source.rename({'4s': 'shots'},axis='columns',inplace=True)

    if button_value==1:
      new_source=bats_man_data[(bats_man_data['Batsman']==selected_batsman) & (bats_man_data['Year_bats']==yr1)].groupby(['Match_ID','6s'])['Runs'].sum().sort_values().reset_index().sort_values(by=['Match_ID'])
      new_source.rename({'6s': 'shots'},axis='columns',inplace=True)
  else:
    if button_value==0:
      new_source=bats_man_data[(bats_man_data['Batsman']==selected_batsman) & (bats_man_data['Year_bats']==yr1) & (bats_man_data['Opposition_bats']==selected_oppo)].groupby(['Match_ID','4s'])['Runs'].sum().sort_values().reset_index().sort_values(by=['Match_ID'])
      new_source.rename({'4s': 'shots'},axis='columns',inplace=True)

    if button_value==1:
      new_source=bats_man_data[(bats_man_data['Batsman']==selected_batsman) & (bats_man_data['Year_bats']==yr1) & (bats_man_data['Opposition_bats']==selected_oppo)].groupby(['Match_ID','6s'])['Runs'].sum().sort_values().reset_index().sort_values(by=['Match_ID'])
      new_source.rename({'6s': 'shots'},axis='columns',inplace=True)
    
  new_runs_cds=ColumnDataSource(new_source[['Match_ID','Runs']])   
  new_shots_cds=ColumnDataSource(new_source[['Match_ID','shots']])
  runs_cds.data=new_runs_cds.data
  shots_cds.data=new_shots_cds.data
    
  fig.title.text='%s Performance Across the Seasons in the Year %d' % (selected_batsman,yr)
  fig.x_range.factors=[]
  fig.x_range.factors=list(np.sort(new_source['Match_ID'].unique()))


run_type.on_change('active',lambda attr, old, new :update(attr, old, new))
slider.on_change('value', update)
radiogroup_batsman.on_change('active', update)
radiogroup_oppo.on_change('active', update)

# Make a row layout of widgetbox(slider) and plot and add it to the current document
layout = row(column(widgetbox(slider),widgetbox(radiogroup_batsman)), fig, column(widgetbox(run_type),widgetbox(radiogroup_oppo)))

curdoc().add_root(layout)
