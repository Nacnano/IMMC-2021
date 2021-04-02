import numpy as np
import pandas as pd
from scipy import optimize
import scipy.stats as stats
import matplotlib.pyplot as plt
from lmfit import Model
from datetime import date
import os

global wta_elo
global wta_prev
wta_elo = {}
wta_prev = {}
for i in range(2018,2019):
  wta_matches_csv = pd.read_csv('/content/Grandslam2018.csv')
  wta_matches_i = pd.DataFrame(wta_matches_csv)
# keys=player_name, items = current_elo

  len_wta_matches_i = wta_matches_i.shape[0]
  for j in range(len_wta_matches_i):
    
    winner = wta_matches_i.iloc[j]['winner_name']
    loser = wta_matches_i.iloc[j]['loser_name']
    date_tour = wta_matches_i.iloc[j]['tourney_date']

    score_mix = str(wta_matches_i.iloc[j]['score'])

    elo_calc(winner_name=winner, loser_name=loser, score_str=score_mix, date_now = date_tour,dict_elo=wta_elo,dict_prev=wta_prev)
  print('year:', i,' player count:',len(wta_elo))

# print(wta_elo)


date_tour= str(2018) + '01' +'01'
for name in wta_elo.keys():
  rerank(player_name=name, date_now = date_tour,dict_elo=wta_elo, dict_prev=wta_prev)



display(wta_elo)