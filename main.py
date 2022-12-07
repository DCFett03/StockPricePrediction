'''
ML Research #1
Calculate the difference of daily return from each timestamp; collect returns

Decide if it is more than 99% or less than 1%

Then use historical to see what might happen based on historical data

Can be a plot or chart

From Column A to right the order:
Date, Minute, Open, High, Low, Close, Volume

Correlation Graphic Function
'''
from pathlib import Path
import glob
import pandas as pd
import os
import glob
import pandas as pd
import seaborn as sb
import numpy as np
from numpy import cov
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import pprint

#path = r'/Users/danielchen/Desktop/2_year_sample/*.csv'
#path = r'/Users/danielchen/Desktop/2_year_sample/allstocks_20190319/*.csv' #65 characters
path = r'/Users/danielchen/Desktop/2_year_sample/test/*.csv' #51 characters
#Add conditional statement to account for gaps in times and subsequent data
files = glob.glob(path)
close = [pd.read_csv(f, index_col = None, header = None, sep=',',usecols = [5]) for f in files]
date = [pd.read_csv(f, index_col = None, header = None, sep=',',usecols = [0]) for f in files]
time = [pd.read_csv(f, index_col = None, header = None, sep=',',usecols = [1]) for f in files]
#print(files)
def Pct_Testing():
    appended_data = []
    for i in range(len(close)):
        pct = close[i].pct_change()
        appended_data.append(pct)
    final_data = (pd.concat(appended_data, axis = 1).stack().reset_index(drop = True))
    pctl_high = (final_data.quantile(q = [0.99]))
    pctl_low = (final_data.quantile(q = [0.01]))
    print("(Quantiles in %)")
    print(pctl_high*100)
    print(pctl_low*100)

    dfdict = {}
    for i in range(len(close)):
        pct = close[i].pct_change()
        #print(pct)
        #print(close)
        #print(time[0].iloc[j+2])
        #print((pct.iloc[j][0]))
        indices = []
        for j in range(len(pct)-1):
            #print(type((pct.iloc[j][0])))
            if pct.iloc[j+1,0] <= pctl_low.iloc[0]:
                str_time = str(time[i].iloc[j+1,0])
                str_date = str(date[i].iloc[j+1,0])
                str_pct = str(pct.iloc[j+1,0]*100)
                indices.append(str("Row: " + str(j+2)) + str(" | Time: ") +
                               str_time [:-2] + ":" +
                               str_time [-2:] + str(" | Date: ") +
                               str_date[:4] + "/" +
                               str_date[4:6] + "/" +
                               str_date[6:] + str(" | %\u0394: ") +
                               str_pct[:8] + "%")
            elif pct.iloc[j+1,0] >= pctl_high.iloc[0]:
                str_time = str(time[i].iloc[j+1,0])
                str_date = str(date[i].iloc[j+1,0])
                str_pct = str(pct.iloc[j+1,0]*100)
                indices.append(str("Row: " + str(j+2)) + str(" | Time: ") +
                               str_time [:-2] + ":" +
                               str_time [-2:] + str(" | Date: ") +
                               str_date[:4] + "/" +
                               str_date[4:6] + "/" +
                               str_date[6:] + str(" | %\u0394: ") +
                               str_pct[:8] + "%")
        dfdict[str(files[i])[51:]] = indices #files str indices change with path
    pprint.pprint(dfdict)

#Correlation Function
def Correlation_Matrix():
    filedict = {}
    for i in range(len(close)):
        #if len(close[i]):
        lol = close[i].values.tolist() #list of lists of each stock close in df [[],[]]
        nonlist = []
        for j in range(len(close[i])):
            intlol = lol[j][0]
            nonlist.append(intlol)
        filedict[files[i]] = (nonlist)
    #print(filedict)
    dict_df = pd.DataFrame({ key:pd.Series(value) for key, value in (filedict.items()) })
    #print(dict_df)
    corrMatrix = dict_df.corr()
    #print(corrMatrix)
    sns.color_palette("hls", 8)
    #good cmap options: Blues, Wistia,bone,autumn, cool_r, gist_rainbow_r, rainbow_r
    sns.heatmap(corrMatrix, annot = True, cmap = 'Blues')
    plt.show()
    #print(df.size)
    #print(df_transposed)
    #print(df.size,df.ndim)

#Pct_Testing()
#Correlation_Matrix()


'''
#fulldf=pd.concat(df,1)
#ax = sns.heatmap(df_transposed)
#fulldata = pd.concat([close[i_index], close[j_index]])
#print(fulldata)

#connect to windows Google Cloud VM
#path2 = virtual machine path that updates regularly
#files2 = glob.glob(path2)
#dfs2 = [pd.read_csv(f, index_c
#ol = None, header = 0, sep=',' ,usecols = [4]) for f in files]

dfs2 = df_list
#could make into function
outliers = []
dfs_list = []
appended_data2 = []
for i in range(len(dfs2)):
    pct2 = dfs2[i].pct_change()
    appended_data2.append(pct2)
final_data2 = (pd.concat(appended_data2, axis = 1).stack().reset_index(drop = True))
#Problem with below code is that we dont know which company that the pct's come from and what the
#location of the data points are after concatenation of all the dataframes. Find out if possible to
#go through dataframe index to read through entries within each dataframe rather than concatenation.
for i in len(final_data2):
    if final_data2[i] <= pctl_low:
        outliers.append(final_data2[i])
        #dfs_list.append(i)
    elif final_data2[i] >= pctl_high:
        outliers.append(final_data2[i])
        #dfs_list.append(i)
df_list = [pd.read_csv(f, index_col = None, header = 0, sep=',') for f in files]
print(outliers)
#print(dfs_list)
#Once percentiles are calculated from historical data, assign value to a variable.
#Then use new updating data from VM to find outliers using if, elif statements with the variables being conditions
'''

