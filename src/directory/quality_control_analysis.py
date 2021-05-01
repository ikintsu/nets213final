# -*- coding: utf-8 -*-
"""sandbox_mturk_manual.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dMcUQsDlSfPiCytXKfIXi7AyuXX7udaY

Maya Patel

NETS 213 Final Project

This script will analyze the labels given by the sandbox workers (experts), the Turkers (the crowd), and ourselves.
"""

import pandas as pd
import csv

# import csv files
sandbox_df = pd.read_csv("sandbox_results_final.csv")
turkers_df = pd.read_csv("mturk_labels.csv")
ourselves_df = pd.read_csv("sandbox_manual_url_labels.csv")

# grab relevant columns
def columns(df):
  return df[['Input.url', 'Answer.asian_hate_crime', 'Answer.reference_hate']]

sandbox_df = columns(sandbox_df)
turkers_df = columns(turkers_df)
ourselves_df = columns(ourselves_df)
ourselves_df['Answer.asian_hate_crime'] = ourselves_df['Answer.asian_hate_crime'].apply(lambda x: True if x == 'TRUE' else False)

# given control and experimental data, how many times did the experimental data agree with control?
def agree(control, experimental):
  total_urls = len(control)
  agree_only_hate_crime = 0
  agree_only_ref_hate = 0
  agree_both = 0
  no_agree = 0
  for i in range(0, len(control)):
    # find ith url in control, extract answers
    curr_url = control.at[i, 'Input.url']
    is_hate_crime = control.at[i, 'Answer.asian_hate_crime'].item()
    is_ref_hate = control.at[i, 'Answer.reference_hate'].item()

    # extract answers from experimental
    exp_row = experimental.loc[experimental['Input.url'] == curr_url]

    exp_hate_crime_ans = False
    exp_ref_hate_ans = False
    
    if (len(exp_row['Answer.asian_hate_crime'].tolist()) == 0 or len(exp_row['Answer.reference_hate'].tolist()) == 0):
      total_urls = total_urls - 1
      continue
    
    exp_hate_crime_ans = exp_row['Answer.asian_hate_crime'].tolist()[0]
    exp_ref_hate_ans = exp_row['Answer.reference_hate'].tolist()[0]

    agree_hc = is_hate_crime == exp_hate_crime_ans
    agree_rf = is_ref_hate == exp_ref_hate_ans
    agree_only_hc = agree_hc and (not(agree_rf))
    agree_only_rf = (not(agree_hc)) and agree_rf
    agree_both_2 = agree_hc and agree_rf

    if (agree_only_hc):
      agree_only_hate_crime = agree_only_hate_crime + 1
    elif (agree_only_rf):
      agree_only_ref_hate = agree_only_ref_hate + 1
    elif (agree_both_2):
      agree_both = agree_both + 1
    else:
      no_agree = no_agree + 1
  
  agree_only_hate_crime = (agree_only_hate_crime / total_urls) * 100
  agree_only_ref_hate = (agree_only_ref_hate / total_urls) * 100
  agree_both = (agree_both / total_urls) * 100
  no_agree = (no_agree / total_urls) * 100
  data = {'Outcome': ['Agreed Only on Hate Crime', 'Agreed Only on References Hate', 'Agreed on Both', 'Did not Agree'], 'Percent Occurred': [agree_only_hate_crime, agree_only_ref_hate, agree_both, no_agree]}
  return pd.DataFrame(data, columns=['Outcome', 'Percent Occurred'])

"""We can use the code above to see how much two sets of people were in agreement or not.  Let's compare the expert labels (from Sandbox) with the crowd labels (from MTurk)."""

agree(turkers_df, sandbox_df)

"""Assuming that the expert labels are 100% accurate, we see that the Turkers were correct with both questions 75% of the time.  13.64% of the time, they were wrong with both questions. 2.27% of the time, they only correctly identified if the article described a hate crime and 9.09% of the time, they only correctly identifed if the article references hate.

Now, let's compare the labels that we completed with the crowd labels (from MTurk).
"""

agree(ourselves_df, turkers_df)

"""Assuming that our opinions are 100% accurate, we see that the Turkers were much less accurate.  They only answered both questions correctly 56.81% of the time and answered both questions wrong 9.09% of the time.  They only answered the hate crime question correcltly 11.36% of the time and only answered the references hate question 22.73% of the time.  This gives us a better idea of how accurate the Turkers really are.

Now, let's compare the labels that we completed with the expert labels (from Sandbox)
"""

agree(ourselves_df, sandbox_df)

"""Assuming that our opinions are 100% accurate, we see that the experts answered both questions correctly 70% of the time and were totally wrong only 1.67% of the time.  However, they only got the hate crime question correct 10% of the time and the references hate question 18.33% of the time.  This suggests that our expert dataset could be interpreted as flawed depending on which opinion (ours or the experts) is considered 100% correct."""