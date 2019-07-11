from bokeh.io import output_notebook
from bokeh.plotting import figure, show, output_file
from bokeh.layouts import row, column
from bokeh.models import CustomJS, Slider, ColumnDataSource, CDSView, GroupFilter
from bokeh.plotting import reset_output
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

def read_bats_man():
    bats_man=pd.read_csv('./Batsman_Data.csv')
    return bats_man

def read_player():
    player_data=pd.read_csv('./WC_players.csv')
    return player_data

def read_match_results():
    match_results=pd.read_csv('./ODI_Match_Result.csv')
    return match_results

def bats_man_cleaning(bats_man):
    bats_man.drop(columns=['Unnamed: 0'],inplace=True)
    bats_man['status']=np.where(bats_man['Bat1'].str.contains('*',regex=False),'not-out','out')
    bats_man.drop(columns=['Bat1'],inplace=True)
    bats_man=bats_man[~(bats_man['Player_ID']==49619)]
    bats_man['Start Date'] = pd.to_datetime(bats_man['Start Date'])
    bats_man['Year']=bats_man['Start Date'].apply(lambda x : x.year)
    bats_man['Match_ID']=bats_man['Match_ID'].str.replace('ODI #','').str.strip()
    bats_man['Opposition']=bats_man['Opposition'].str.replace('v ','').str.strip()
    bats_man=bats_man[bats_man['Year'].isin([2013, 2014, 2015, 2016, 2017, 2018, 2019])]
    return bats_man

def player_data_cleaning(player_data):
    return player_data

def match_results_cleaning(match_results):
    match_results.drop(columns=['BR','Unnamed: 0'],inplace=True)
    match_results['Opposition']=match_results['Opposition'].str.replace('v ','').str.strip()
    match_results['Match_ID']=match_results['Match_ID'].str.replace('ODI #','').str.strip()
    match_results['Start Date'] = pd.to_datetime(match_results['Start Date'])
    match_results['Year']=match_results['Start Date'].apply(lambda x : x.year)
    match_results_india=match_results[match_results['Country']=='India'] 
    match_results_india=match_results_india[match_results_india['Result'].isin(['lost', 'won','tied'])]
    return match_results_india
  
