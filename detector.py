#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 25 17:54:34 2022

@author: armin
"""

import pandas as pd

#Reading data from Excel
df1 = pd.read_excel('Data8.xlsx',index_col=(0))
df2 = pd.read_excel('0444.xlsx',index_col=(0))
"""
#Deleting Extra Data (optional/talk with aouthor)
#(Be careful)
df1.drop("Luminate", inplace = True, axis = 1)
df1.drop("L/val", inplace = True, axis = 1)


df2.drop("Luminate", inplace = True, axis = 1)
df2.drop("L/val", inplace = True, axis = 1)
"""

#Listing wanted data for calculating
X1 = df1['X'].tolist()
X2 = df2['X'].tolist()

Y1 = df1['Y'].tolist()
Y2 = df2['Y'].tolist()

val1 = df1['val'].tolist()
val2 = df2['val'].tolist()

Match = []
Error = 0   #Error function


for i in range(len(X1)):
    Min_Error = 3*len(X1) #Minimum Error function for detecting
    counter = -1
    for j in range(len(X2)):
        if val2[j] != 0:
            Error = 0
            Error += (X1[i]-X2[j])**2 + (Y1[i]-Y2[j])**2 + (val1[i]-val2[j])**2
        if Error < Min_Error :
            Min_Error = Error
            counter = j
    Min_Error = 3*len(X1)
    if counter != -1:   #Rechecking from opposite
        check = -1
        for k in range(i,len(X1)):
            Error=0
            Error += (X2[counter]-X1[k])**2 + (Y2[counter]-Y1[k])**2 + (val2[counter]-val1[k])**2
            if Error < Min_Error :
                Min_Error = Error
                check = k
    if i == check:  #Real star!
        Match.append([X2[counter],Y2[counter],val2[counter]])
        val2[counter] = 0
    else:   #Fake light!
        df1.drop(index = i, inplace = True)
                
    
       

df1.index = range(len(df1)) #Reindexing dataframe

Match_df = pd.DataFrame(Match ,columns =[ 'X9','Y9', 'val9' ])

result=pd.concat([df1, Match_df], axis=1)   #Merging Data

#Export to exel
datatoexcel = pd.ExcelWriter('Data9.xlsx')
result.to_excel(datatoexcel)
datatoexcel.save()
