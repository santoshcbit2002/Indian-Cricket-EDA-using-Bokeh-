import data_cleanpy
from bokeh.models.widgets import RadioButtonGroup
from bokeh.layouts import widgetbox, row

from bokeh.io import output_file,curdoc,show
from bokeh.plotting import figure, show, output_file
from bokeh.layouts import row, column
from bokeh.models import CustomJS, Slider, ColumnDataSource, CDSView, GroupFilter
from bokeh.plotting import reset_output

match_results_data=data_cleanpy.read_match_results()
#print('Null Values in match_results_data: ', match_results_data.isnull().sum(axis=0).sort_values())
match_results_clean=data_cleanpy.match_results_cleaning(match_results_data)
match_results_clean=match_results_clean.reset_index()
print(match_results_clean.head(5))
yr=min(match_results_clean.Year)

match_source_year=match_results_clean[match_results_clean['Year']==yr].groupby(['Opposition','Result'])['index'].count().reset_index()

total_cds=ColumnDataSource(match_source_year)          
result_cds=ColumnDataSource(match_source_year[match_source_year['Result']=='won'])

fig = figure(title='Total Matches Played Aganist Opposition',
             y_range=[0,10],
             x_range=list(match_source_year['Opposition'].unique())
             )

fig.vbar(x='Opposition',top='index',source=total_cds,width=0.5)
#fig.vbar(x='Opposition',top='index',source=result_cds,width=0.5)
fig.xaxis.major_label_orientation = "vertical"

slider = Slider(start=min(match_results_clean.Year), end=max(match_results_clean.Year), step=1, value=min(match_results_clean.Year), title='Year of Play')
radio_button_group = RadioButtonGroup(labels=['Win', 'Loss','Tie'], active=0)

def update(attr,old,new):
  yr = slider.value
  print('Slider Value is : ', yr)
  new_source=match_results_clean[match_results_clean['Year']==yr].groupby(['Opposition','Result'])['index'].count().reset_index()

  button_value= radio_button_group.active
  print('Button value  is : ', button_value)
  
  if button_value==0:
         won_source=new_source[new_source['Result']=='won']
         new_won_cds= ColumnDataSource(won_source)
         total_cds.data=new_won_cds.data
  if button_value==1:
         lost_source=new_source[new_source['Result']=='lost']
         new_lost_cds= ColumnDataSource(lost_source)
         total_cds.data=new_lost_cds.data
  if button_value==2:
         tied_source=new_source[new_source['Result']=='tied']
         new_tied_cds= ColumnDataSource(tied_source)
         total_cds.data=new_tied_cds.data

  fig.title.text='Total Matches Played Aganist Opposition for Year %d' % yr
  fig.x_range.factors=[]
  fig.x_range.factors=list(new_source['Opposition'].unique())
    
radio_button_group.on_change('active',lambda attr, old, new :update(attr, old, new))

slider.on_change('value', update)

# Make a row layout of widgetbox(slider) and plot and add it to the current document
layout = row(column(widgetbox(slider),widgetbox(radio_button_group)), fig)

curdoc().add_root(layout)
