# !pip install lmfit
# !pip install spicy
# !pip install fsspec

import numpy as np
import pandas as pd
from scipy import optimize
import scipy.stats as stats
import matplotlib.pyplot as plt
from lmfit import Model
from datetime import date
import os

def elo_calc(winner_name, loser_name, score_str, date_now, dict_elo, dict_prev):
    who_won = 1

    ## Set new ELOs and change ELOs due to inactivity
    if winner_name not in dict_elo:
      dict_elo[winner_name] = 1200
      dict_prev[winner_name] = date_now
    elif dict_elo[winner_name] > 1200:
      date_prev = str(dict_prev[winner_name])
      dict_prev[winner_name]=date_now
      date_now = str(date_now)
      d0=date(int(date_prev[:4]), int(date_prev[4:6]), int(date_prev[6:8]))
      d1=date(int(date_now[:4]), int(date_now[4:6]), int(date_now[6:8]))
      delta = d1 - d0
      day_change = delta.days

      if day_change > 28:
        dict_elo[winner_name] = (dict_elo[winner_name] - 1200)/(1 + 1.001 ** (day_change/7)) +1200

    date_now =str(date_now)

    if loser_name not in dict_elo:
      dict_elo[loser_name] = 1200
      dict_prev[loser_name] = date_now
    elif dict_elo[loser_name] > 1200:
      date_prev = str(dict_prev[loser_name])
      dict_prev[loser_name]=date_now
      date_now = str(date_now)
      d0=date(int(date_prev[:4]), int(date_prev[4:6]), int(date_prev[6:8]))
      d1=date(int(date_now[:4]), int(date_now[4:6]), int(date_now[6:8]))
      delta = d1 - d0
      day_change = delta.days

      if day_change > 28:
        dict_elo[loser_name] = (dict_elo[loser_name] - 1200)/(1 + 1.001 ** (day_change/7)) +1200




    score_list = score_str.split(' ')

    for score in score_list:
      if score == 'W/O' or score == 'RET':
        continue
      try:
        score1, score2 = score.split('-')
      except:
        break

      try:
        score1 = int(score1)
      except:
        break

      if '(' not in score2:

        try:
          score2 = int(score2)
        except:
          break

        if score1 > score2:
          score_win = score1
          score_lose = score2
        else:
          score_win = score1
          score_lose = score2
      else:
        len_score2 = len(score2)
        for i in range(len_score2):
          if score2[i] == '(':
            mul=1
            tie_score2=0
            for j in range(i+1,100):
              if score2[j] ==')':
                break
              tie_score2 += int(score2[j])
              mul*=10
        tmp=0
        mul=1
        for i in range(len_score2):
          if score2[i] == '(':
            break
          tmp += int(score2[i])
          mul *= 10

        score2 = int(tmp)
        if score1 > score2:
          score2 += tie_score2
          if tie_score2 <=5:
            score1 += 7
          else:
            score1 += tie_score2 + 2
          score_win = score1
          score_lose = score2
        
        elif score1 < score2:
          score1 += tie_score2
          if tie_score2 <=5:
            score2 += 7
          else:
            score2 += tie_score2 + 2
          who_won = 2
          score_win = score2
          score_lose = score1


      #score
      score_win = int(score_win)
      score_lose = int(score_lose)

      if score_win - score_lose == 2:
        d=1.8
      elif score_win - score_lose == 3:
        d=2
      else:
        d=2+0.1*(score_win - score_lose)
      
      if d<1:
        break

      if score_win == 7 or score_win == 6:
        s=1
      else:
        s=1.5

      if score_lose < 12:
        t=1
      else:
        t=score_lose - 10

      x=5
      f=(d/s) ** (1/t)
      k_factor = f*x
  
      change = k_factor * (1 - (1+10**((dict_elo[winner_name]-dict_elo[loser_name])/600) )**(-1))

      if who_won == 1:

        dict_elo[winner_name] += change
        dict_elo[loser_name] -= change
      elif who_won == 2:
        dict_elo[winner_name] -= change
        dict_elo[loser_name] += change 


    #lower_bound
      # dict_elo[winner_name] = max(0,dict_elo[winner_name])
      # dict_elo[loser_name] = max(0,dict_elo[loser_name])



def rerank(player_name, date_now, dict_elo, dict_prev):
    if player_name not in dict_elo:
      dict_elo[player_name] = 1200
      dict_prev[player_name] = date_now
    elif dict_elo[player_name] > 1200:
      date_prev = str(dict_prev[player_name])
      dict_prev[player_name]=date_now
      date_now = str(date_now)
      d0=date(int(date_prev[:4]), int(date_prev[4:6]), int(date_prev[6:8]))
      d1=date(int(date_now[:4]), int(date_now[4:6]), int(date_now[6:8]))
      delta = d1 - d0
      day_change = delta.days
    
      if day_change < 4*7: 
        tmp=1
      else:
        dict_elo[player_name] = (dict_elo[player_name] - 1200)/(1 + 1.001 ** (100*day_change/7 - 1000)) +1200


# def display(dict_elo):
#       df_elo = pd.DataFrame(list(dict_elo.items()), columns = ['Player Name', 'ELO'])

#   df_elo_sorted = df_elo.sort_values(by='ELO', ascending = False)
#   df_elo_sorted = df_elo_sorted.reset_index(drop=True)
#   df_elo_sorted.index +=1
#   print(df_elo_sorted.head(15))

#   mid = df_elo['ELO'].mean()
#   sd =  df_elo['ELO'].std()
#   num_player = df_elo.shape[0]
#   print('Number of Players:', num_player)
#   print('mean:', mid)
#   print('STD:', sd)
#   df_elo.plot.hist(bins=50)




def elo_calc_sprint(winner_name, loser_name, time_win, time_lose, date_now, dict_elo, dict_prev):
    ## Set new ELOs and change ELOs due to inactivity
    if winner_name not in dict_elo:
      dict_elo[winner_name] = 1200
      dict_prev[winner_name] = date_now
    elif dict_elo[winner_name] > 1200:
      date_prev = str(dict_prev[winner_name])
      dict_prev[winner_name]=date_now
      date_now = str(date_now)
      d0=date(int(date_prev[:4]), int(date_prev[4:6]), int(date_prev[6:8]))
      d1=date(int(date_now[:4]), int(date_now[4:6]), int(date_now[6:8]))
      delta = d1 - d0
      day_change = delta.days

      if day_change < 4*7:
        tmp=1
      else:
        dict_elo[winner_name] = (dict_elo[winner_name] - 1200)/(1 + 1.001 ** (100*day_change/7 - 1000)) +1200


    date_now =str(date_now)

    if loser_name not in dict_elo:
      dict_elo[loser_name] = 1200
      dict_prev[loser_name] = date_now
    elif dict_elo[loser_name] > 1200:
      date_prev = str(dict_prev[loser_name])
      dict_prev[loser_name]=date_now
      date_now = str(date_now)
      d0=date(int(date_prev[:4]), int(date_prev[4:6]), int(date_prev[6:8]))
      d1=date(int(date_now[:4]), int(date_now[4:6]), int(date_now[6:8]))
      delta = d1 - d0
      day_change = delta.days

      if day_change < 4*7:
        tmp=1
      else:
        dict_elo[loser_name] = (dict_elo[loser_name] - 1200)/(1 + 1.001 ** (100*day_change/7 - 1000)) + 1200

    #Calculating X from Normal Distribution
    mid = np.mean(list(dict_elo.values()))
    std = np.std(list(dict_elo.values()))

    try:
      z_score_winner = (dict_elo[winner_name] - mid) / std
      z_score_loser = (dict_elo[loser_name] - mid) / std
    except:
      x1=1
      x2=1

    if z_score_winner >= 2 :
      x1 = 5
    elif z_score_winner >= 1 :
      x1 = 4
    elif z_score_winner >= 0 :
      x1 = 3
    elif z_score_winner >= -1 :
      x1 = 2
    else :
      x1 = 1

    if z_score_loser >= 2 :
      x2 = 5
    elif z_score_loser >= 1 :
      x2 = 4
    elif z_score_loser >= 0 :
      x2 = 3
    elif z_score_loser >= -1 :
      x2 = 2
    else :
      x2 = 1
     
    d=time_lose - time_win
    t=time_win + time_lose
    f= 1.05 ** (1/d + 1/t)

      
    k_factor_loss = f*x1
    k_factor_won = f*x2
    

    change_won = k_factor_won * (1 - (1+10**((dict_elo[loser_name]-dict_elo[winner_name])/600) )**(-1))
    change_loss = k_factor_loss * (1 - (1+10**((dict_elo[winner_name]-dict_elo[loser_name])/600) )**(-1))

    dict_elo[winner_name] += change_won
    dict_elo[loser_name] -= change_loss

    #lower_bound
    # dict_elo[winner_name] = max(0,dict_elo[winner_name])
    # dict_elo[loser_name] = max(0,dict_elo[loser_name])

  