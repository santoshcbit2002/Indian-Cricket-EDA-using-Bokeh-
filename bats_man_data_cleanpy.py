
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

def data_cleaning():
    player_data=pd.read_csv('./WC_players.csv')
    bats_man=pd.read_csv('./Batsman_Data.csv')
    match_results=pd.read_csv('./ODI_Match_Result.csv')

    player_data['ID']=np.where(player_data['Player']=='Oshane Thomas',49619,player_data['ID'])
    
    match_results.drop(columns=['BR','Unnamed: 0'],inplace=True)
    match_results['Opposition']=match_results['Opposition'].str.replace('v ','').str.strip()
    match_results['Match_ID']=match_results['Match_ID'].str.replace('ODI #','').str.strip()
    match_results['Start Date'] = pd.to_datetime(match_results['Start Date'])
    match_results['Year']=match_results['Start Date'].apply(lambda x : x.year)
    match_results_india=match_results[match_results['Country']=='India'] 

    bats_man.drop(columns=['Unnamed: 0'],inplace=True)
    bats_man['status']=np.where(bats_man['Bat1'].str.contains('*',regex=False),'not-out','out')
    bats_man.drop(columns=['Bat1'],inplace=True)
    bats_man['Player_ID']=np.where(bats_man['Batsman']=='Oshane Thomas',49619,bats_man['Player_ID'])
    bats_man=bats_man.merge(player_data,how='inner',left_on='Player_ID',right_on='ID')
    bats_man['Start Date'] = pd.to_datetime(bats_man['Start Date'])
    bats_man['Year']=bats_man['Start Date'].apply(lambda x : x.year)
    bats_man['Match_ID']=bats_man['Match_ID'].str.replace('ODI #','').str.strip()
    bats_man['Opposition']=bats_man['Opposition'].str.replace('v ','').str.strip()
    bats_man.drop(columns=['ID','Ground','Player'],inplace=True)
    bats_man_india=bats_man[bats_man['Country']=='India']
    bats_man_india=bats_man_india[bats_man_india['Year'].isin([2013, 2014, 2015, 2016, 2017, 2018, 2019])]

    match_results_india=match_results_india[~match_results_india['Match_ID'].isin(['3422a', '3444', '3497', '3498', '3499', '3513a', '3534a', '3535a'])]
    
    bats_man_data=bats_man_india.join(match_results_india.set_index('Match_ID'),on='Match_ID',lsuffix='_bats', rsuffix='_match')
    bats_man_data.drop(columns=['Player_ID','Country_bats','Opposition_match','Ground','Start Date_match','Country_match','Country_ID','Year_match'],inplace=True)
    bats_man_data['Batsman']=bats_man_data.Batsman.str.strip()
    bats_man_data['Runs']=bats_man_data['Runs'].str.replace('-','0')
    bats_man_data['Runs']=bats_man_data['Runs'].astype(int)
    return bats_man_data

  
