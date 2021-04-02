print("What's your gender ? : (Male / Female)")
sex = input()

print("What's your name ? :")
DTS_name = input()

if sex == 'Male' or sex == 'male' :
  print('Hi, Mr.%s' %DTS_name)
else :
  print("Hi, Mrs.%s" %DTS_name)

print('This is GFinder, a program to calculate players\' rating based on our mathematical model')
print('How to use:')
print('Enter the required information to the program')
print('We hope you to like it')
print('Thank you')

print('*************** S T A R T - G F i n d e r ***************')

global letter_elo
letter_elo = {}
global letter_prev
letter_prev = {}

i=1
while 1 :
  print('Match %d :' %i)
  print('Enter match date : (YYYYMMDD)')
  tour_date=input()
  
  print('Enter winner name : ')
  winner = input()


  print('Enter loser name : ')
  loser = input()

  print('Does this match has a Tiebreaker? : (Y/N)')
  tie=str(input())

  if tie =='Y':
    print('Enter loser\'s tiebreaker score : ')
    st2 = int(input())
    score_mix = str(s1) + '-' + str(s2) +'(' + str(st2) + ')'
  else:
    print('Enter winner\'s score : ')
    s1 = int(input())
    print('Enter loser\'s score : ')
    s2 = int(input())
    score_mix = str(s1) + '-' + str(s2)
  
  elo_calc(winner_name=winner,loser_name=loser,score_str=score_mix, date_now=tour_date, dict_elo=letter_elo,dict_prev=letter_prev)

  i=i+1
  
  print('ELO Rating Updated Completed')
  print('Continue the Program? : (Y/N)')
  con = str(input())
  if con == 'N':
    break

print('ELO Ranking')
display(letter_elo)