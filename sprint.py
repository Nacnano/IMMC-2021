import numpy as np
import pandas as pd
from scipy import optimize
import scipy.stats as stats
import matplotlib.pyplot as plt
from lmfit import Model
from datetime import date
import os


global sprint_elo
sprint_elo  = {}
global sprint_prev
sprint_prev = {}

sprint_result = pd.read_csv('/content/2004-2016-Short-Races.csv', encoding='latin-1' )
df_sprint = pd.DataFrame(sprint_result)
df_sprint = df_sprint[df_sprint['Gender'] == 'M']

tour_name = ['Preliminary', 'Heats', 'Semi', 'Final']

for year in range(2004,2017):

  if year%4!=0:
    continue
  print(year)
  date_tour = str(year)+'01'+'01'
  df_year = df_sprint[df_sprint['Year'] == year]

  for tour in tour_name:
    df_year_tour = df_year[df_year['Round'] == tour]
    
  
# keys=player_name, items = current_elo

    len_df_sprint = df_year_tour.shape[0]

    for i in range(len_df_sprint):
      
      player1 = df_year_tour.iloc[i]['ATHLETE']
      time1 = df_year_tour.iloc[i]['MARK']
      for j in range(i+1,len_df_sprint):
        player2 = df_year_tour.iloc[j]['ATHLETE']
        time2 = df_year_tour.iloc[j]['MARK']

        if type(time1) == 'str':
          time1.strip('Q')
          time1.strip('q')
        if type(time2) == 'str':
          time2.strip('Q')
          time2.strip('q')

        try:
          time1=float(time1)
          time2=float(time2)
        except:
          continue
        if time1 < time2:
          elo_calc_sprint(winner_name=player1, loser_name=player2, time_win = time1, time_lose=time2, date_now = date_tour,dict_elo = sprint_elo, dict_prev = sprint_prev)
      
        elif time1 > time2:
          elo_calc_sprint(winner_name=player2, loser_name=player1, time_win = time2, time_lose=time1, date_now = date_tour,dict_elo = sprint_elo, dict_prev = sprint_prev)

           

date_tour = str(2016) + '01' + '01'
for key in sprint_elo.keys():
  rerank_sprint(player_name=key, date_now=date_tour, dict_elo=sprint_elo, dict_prev=sprint_prev)

display(sprint_elo)