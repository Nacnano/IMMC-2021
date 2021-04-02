import numpy as np
import pandas as pd
from scipy import optimize
import scipy.stats as stats
import matplotlib.pyplot as plt
from lmfit import Model
from datetime import date
import os


# input the winner => player1 and the loser => player2
global wta_elo
global wta_prev
wta_elo = {}
wta_prev = {}

for i in range(2018,2019):
  f= 'wta_matches_' +str(i) +'.csv'

  wta_matches_csv = pd.read_csv('https://github.com/JeffSackmann/tennis_wta/raw/master/' + f)
  wta_matches_i = pd.DataFrame(wta_matches_csv)

  len_wta_matches_i = wta_matches_i.shape[0]
  for j in range(len_wta_matches_i):
    
    winner = wta_matches_i.iloc[j]['winner_name']
    loser = wta_matches_i.iloc[j]['loser_name']
    date_tour = wta_matches_i.iloc[j]['tourney_date']

    score_mix = str(wta_matches_i.iloc[j]['score'])

    elo_calc_nutch(winner_name=winner, loser_name=loser, score_str=score_mix, date_now = date_tour,dict_elo=wta_elo,dict_prev=wta_prev)
  print('year:', i,' player count:',len(wta_elo))

# print(wta_elo)

date_tour= str(2018) + '01' +'01'
for name in wta_elo.keys():
  rerank(player_name=name, date_now = date_tour,dict_elo=wta_elo, dict_prev=wta_prev)


# Displaying the ELO Rating distribution
display(wta_elo)