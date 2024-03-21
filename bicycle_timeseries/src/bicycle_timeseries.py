#!/usr/bin/env python3
'''
This script reads the given data set, cleans it (i.e. turns its Päivämäärä column into
 (row) DatetimeIndex (that is, to row names) of the DataFrame) and returns a new DataFrame
'''
import pandas as pd
 
def split_date(df):
    ldf = df
    full_date = ldf['Päivämäärä']
    
    day_dict = {'ma':'Mon','ti':'Tue','ke':'Wed','to':'Thu','pe':'Fri','la':'Sat','su':'Sun'}
    month_dict = {'tammi':1,'helmi':2,'maalis':3,'huhti':4,'touko':5,'kesä':6,'heinä':7,'elo':8,'syys':9,'loka':10,'marras':11,'joulu':12}
 
    expanded_date = full_date.str.split(expand=True)
    expanded_date[0] = expanded_date[0].map(day_dict)
    expanded_date[2] = expanded_date[2].map(month_dict)
 
    split_time = expanded_date[4].str.split(':')
    hours = split_time.apply(lambda x: x[0])
    expanded_date[4] = hours
    expanded_date = expanded_date.rename(columns={0:'Weekday', 1:'Day', 2:'Month', 3:'Year', 4:'Hour'})
    return expanded_date.astype({'Weekday':str, 'Day':int, 'Month':int,'Year':int, 'Hour':int})
 
def split_date_continues():
    df = pd.read_csv(r'src/Helsingin_pyorailijamaarat.csv', sep=';')
    df = df.dropna(how='all')
 
    exp_date = split_date(df)
    df = df.drop(columns = 'Päivämäärä')
    df = df.dropna(how='all', axis = 1)
 
 
    return pd.concat([exp_date, df], axis = 1)
 
def bicycle_timeseries():
    df = split_date_continues()
    df['compact_date'] = pd.to_datetime(df[['Year', 'Month', 'Day', 'Hour']])
    df = df.drop(columns=['Weekday', 'Day', 'Month', 'Year', 'Hour'])
    df2 = df.set_index('compact_date')
    return df2
 
def main():
    value = bicycle_timeseries()
    print(value)
 
if __name__ == "__main__":
    main()
 