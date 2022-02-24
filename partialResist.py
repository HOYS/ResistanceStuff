import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import csv
import re
import pandas as pd

pattern = r"^[^\d]*"
pattern2 = r"\*"
pattern3 = r"[^\d]"
pattern4 = r"\(O([\s\S]*)$"

df = pd.DataFrame()

with open('FILENAMEHERE.csv') as csvfile:
  reader = csv.DictReader(csvfile)
  for row in reader:
    mod_string = re.sub(pattern, '', row["Event"])
    mod_string = re.sub(pattern2, '', mod_string)
    # remove potential overkill
    mod_string = re.sub(pattern4, '', mod_string)
    mod_string = mod_string.split(" ",1)
    if len(mod_string) > 1:
      mod_string[1] = re.sub(pattern3, '', mod_string[1])
  
    #remove blank lines (immune etc)
    if mod_string[0] != '':
      dict = {'Damage': mod_string[0], 'Resisted': mod_string[1] if len(mod_string)>1 else 0}
      df = df.append(dict, ignore_index=True)


  df['Damage'] = df['Damage'].astype(int)
  df['Resisted'] = df['Resisted'].astype(int)
  print("Mean of damage resisted " + str(df['Resisted'].mean()))
  df['Total_Damage'] = df['Damage'] + df['Resisted']
  df['Percent_Resist'] = (df['Resisted'] / df['Total_Damage']) * 100
  print("Percent of damage resisted " + str(df['Percent_Resist'].mean()))

    
