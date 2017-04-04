import matplotlib.pyplot as plt
import pandas
import pandas as pd
import urllib2
import os, sys
import time
import datetime

def download():
    for y in range (1,28):
        url="https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_provinceData.php?country=UKR&provinceID="+str(y)+"&year1=1981&year2=2017&type=Mean"
        vhi_url = urllib2.urlopen(url)
        out = open('region'+str(y)+'.csv','wb')
        out.write(vhi_url.read())
        
        
    out.close()
#download()
    
    
def vhi(file,year):
    list_of_columns = ["year", "week", "SMN", "SMK", "VCI", "TCI", "VHI", ]
    df = pd.read_csv(file,names=list_of_columns, engine='python', delimiter='\,\s+|\,|\s+', skiprows=1)
    df1=df[df.year==year]
    max_vhi, min_vhi = df1["VHI"].max(), df1["VHI"].min()
    print("maximum vhi of "+'year ' + str(max_vhi)+" and min is "+str(min_vhi))
    print(df1[:50])
    print(list(df1.columns.values))
    df.plot(x='year', y='VHI', style='y--')
    plt.show()
    



def download_vhi():
    for y in range(1,28):
        url = "https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_provinceData.php?country=UKR&provinceID={}&year1=1981&year2=2017&type=VHI_Parea".format(y)
        vhi_url = urllib2.urlopen(url)
        out = open("percent_vhi_{}.csv".format(y), 'wb')
        out.write(vhi_url.read())
        out.close()
        print("percent"+str(y))
#download_vhi()

def percent_func(file):
    list_of_columns = ["year", "week"]
    list_percent = [str(x) for x in range(0, 105, 5)]
    list_of_columns.extend(list_percent)
    frame_id = pd.read_csv(file, names=list_of_columns, engine='python', delimiter='\,\s+|\,|\s+', skiprows=1)
    # print(list(frame_id.columns.values))
    return frame_id
    # print(frame_id[:1])

    
    
def vhi_of_percent(frame, percent):
    dict_of_years = {}
    list_of_years = []
    for year in range(1981, 2018):
        short_frame = frame[frame.year == str(year)][['0', '5', '10', '15']]  # part of frame with one year,and percent<=15
        list_sum = 0
        for i in list(short_frame.columns.values):
            list_sum += short_frame[i].mean()
        dict_of_years[str(year)] = list_sum
    series_year = pd.Series(dict_of_years)
    print(series_year.iteritems())
    for key in series_year.keys():
        if series_year[key] > percent:
            list_of_years.append(key)
    print(list_of_years)
    return list_of_years



vhi("region2.csv","2000")
frame = percent_func("percent_vhi_1.csv")  #table with a percent of vhi
list_of_bad_years = vhi_of_percent(frame, 5) #check province level of VHI

