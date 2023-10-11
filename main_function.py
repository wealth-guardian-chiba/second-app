import pandas as pd
import numpy as np
import datetime
from dateutil.relativedelta import relativedelta

def function1(df):
  #parameters
  date = "2023-7-5" #date
  rate = 145 #USD-yen spot
  date = datetime.datetime.strptime(date, '%Y-%m-%d')
  
  col_num = df.columns[1:]
  
  duration = ["残存期間[年]"]
  benefit = ["参考利回り[％]"]
  yen = ["円換算購入金額[円]"]
  port = ["-"]
  weight = 0
  coupon_sum = 0
  duration_sum = 0
  benefit_sum = 0
  yen_sum = 0
  
  for name in col_num:
      position = df[name][5]/100
      duration.append(round((df[name][3]-date).days/365, 2))
      benefit.append(round(df[name][1]+(100 - df[name][6])/duration[len(duration)-1], 2))
      yen.append(round(rate*df[name][6]*position))
      
      weight += position
      coupon_sum += df[name][1]*position
      duration_sum += duration[len(duration)-1]*position
      benefit_sum += benefit[len(benefit)-1]*position
      yen_sum += yen[len(yen)-1]
      
  df.loc[len(df)] = duration
  df.loc[len(df)] = benefit
  df.loc[len(df)] = yen
  
  port.append(round(coupon_sum/weight, 2))
  for i in range(5):
      port.append("-")
  
  port.append(round(duration_sum/weight, 2))
  port.append(round(benefit_sum/weight, 2))
  port.append(round(yen_sum))
  
  df["ポートフォリオ"] = port
  return df
  
def function2(df):
  #parameters
  date = "2023-7-5" #date
  rate = 145 #USD-yen spot
  date = datetime.datetime.strptime(date, '%Y-%m-%d')
  col_num = df.columns[1:]
  year_array = []
  for name in col_num:
      end = df[name][3]
      year_array.append(end.year)
  year_array = np.array(year_array)
  year_max = year_array.max()
  index = []
  for i in range(date.year, year_max+1):
      index.append(str(i)+"年")
  index.append("利金合計")
  index.append("償還差損益")
  index.append("利金・償還損益合計")
  
  new_df = pd.DataFrame({
      "index": index})
  for name in col_num:
      array = np.zeros(year_max-date.year+4)
      benefit = df[name][5] * 0.01 * df[name][1]
      end = df[name][3]
      half_year_ago = end - relativedelta(months=6)
      
      date2 = datetime.datetime.strptime(str(date.month) + "-" + str(date.day), '%m-%d')
      end2 = datetime.datetime.strptime(str(end.month) + "-" + str(end.day), '%m-%d')
      half2 = datetime.datetime.strptime(str(half_year_ago.month) + "-" + str(half_year_ago.day), '%m-%d')
      
      if date.year == end.year:
          if end2.month > 5:
              if half2 > date:
                  array[0] = round(benefit)
              else:
                  array[0] = round(0.5 * benefit)
          else:
              array[0] = round(0.5 * benefit)
              
      else:
          if date2 < end2:
              if date2 < half2:
                  array[0] = round(benefit)
              else:
                  array[0] = round(0.5 * benefit)
          else:
              if date2 < half2:
                  array[0] = round(0.5 * benefit)
                  
          delta = end.year - date.year
          if delta > 1:
              for i in range(delta-1):
                  array[i+1] = round(benefit)
              
          if end2.month > 5:
              array[delta] = round(benefit)
          else:
              array[delta] = round(0.5 * benefit)
              
      sum_value = array.sum()
      array[-3] = round(sum_value)
      loss = df[name][5] * 0.01 * (df[name][6] - 100)
      array[-2] = -round(loss)
      array[-1] = round(sum_value-loss)
      new_df[name] = array
  
  port = []
  current = ["通貨"] 
  col = new_df.columns
  for i in range(len(new_df)):
      x = 0
      for j in range(1, len(col)):
          x = x + new_df[col[j]][i]
          if i == 1:
              current.append(df[col[j]][0])
      port.append(round(x))
  current.append(df[col[1]][0])   
  new_df["ポートフォリオ"] = port
  new_df.loc[0] = current

  return new_df
  

    
