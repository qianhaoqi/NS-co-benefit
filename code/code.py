# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 21:57:01 2020
@author: thund
"""

import pandas as pd
import re
import numpy as np
import matplotlib.pyplot as plt  
import time
from scipy import stats, integrate
import seaborn as sns
import os
from matplotlib import font_manager as fm, rcParams

#change to your workspace
os.chdir(r'C:\Users\18110\Desktop\NS')
try:
    os.mkdir(r'C:\Users\18110\Desktop\NS\final-result')
except Exception as e:
    print(e)
try:
    os.mkdir(r'C:\Users\18110\Desktop\NS\final-result\direct-ei')
except Exception as e:
    print(e)
try:
    os.mkdir(r'C:\Users\18110\Desktop\NS\final-result\indirect-electrification')
except Exception as e:
    print(e)
try:
    os.mkdir(r'C:\Users\18110\Desktop\NS\final-result\indirect-scale')
except Exception as e:
    print(e)
try:
    os.mkdir(r'C:\Users\18110\Desktop\NS\final-result\lmdi')
except Exception as e:
    print(e)
try:
    os.mkdir(r'C:\Users\18110\Desktop\NS\final-result\lmdi\pic')
except Exception as e:
    print(e)    
try:
    os.mkdir(r'C:\Users\18110\Desktop\NS\final-result\lmdi\pic\temp')
except Exception as e:
    print(e)    
        
# =============================================================================
# LMDI for pollutant (based on sample from 2011 to 2014)
# =============================================================================
def get(df1,df0,item):
    a = list(df1[item])[0]
    b = list(df0[item])[0] 
    z =np.log(a/b)
    return z

def lmdi_dynamic_nonpower(pol,start,end,data):
    l1, l2, l3, l4, l5 = [], [], [], [], []
    l_year, l_ind, l_region = [], [], []
    result = pd.DataFrame()
    for region in ['EASTERN','CENTRAL','WESTERN','NATIONAL']:    
        for ind in [22,25,26,30,31,32]:
            if region == 'NATIONAL':
                temp = data[data['ind2code']==ind]
            else:
                temp = data[(data['ind2code']==ind)&(data['region']==region)]    
            for year in range(start+1,end+1):
                keep = set()
                temp0 = temp[temp['year'] == year-1]
                temp1 = temp[temp['year'] == year]
                merge = pd.merge(temp1,temp0,on='firmid',how='left')
                firmset = set(merge[merge['EOP_y']==merge['EOP_y']]['firmid'])
                D1,D2,D3,D4,D5 = 0,0,0,0,0
                for firm in firmset:
                    em1 = temp1[temp1['firmid']==firm][pol].sum()
                    em0 = temp0[temp0['firmid']==firm][pol].sum()
                    if em1 != em0:
                        keep = keep|{firm}
                EM1 = temp1[temp1['firmid'].isin(keep)][pol].sum()
                EM0 = temp0[temp0['firmid'].isin(keep)][pol].sum()                
                for firm in keep:
                    df1 = temp1[temp1['firmid']==firm]
                    df0 = temp0[temp0['firmid']==firm]   
                    if len(df1)!=1 | len(df0)!=1:
                        print ('error')
                    em1 = df1[pol].sum()
                    em0 = df0[pol].sum()
                    w = ((em1-em0)/(np.log(em1)-np.log(em0)))/((EM1 - EM0)/(np.log(EM1)-np.log(EM0)))
                    D1 = D1 + get(df1,df0,'EOP') * w
                    D2 = D2 + get(df1,df0,'EF') * w
                    D3 = D3 + get(df1,df0,'ES') * w
                    D4 = D4 + get(df1,df0,'EI') * w
                    D5 = D5 + get(df1,df0,'totalproduct_modify') * w
                l1.append(np.exp(D1))
                l2.append(np.exp(D2))
                l3.append(np.exp(D3))
                l4.append(np.exp(D4))
                l5.append(np.exp(D5))
                l_region.append(region)
                l_year.append(year)
                l_ind.append(ind)
                
    result['year'] = l_year
    result['ind'] = l_ind    
    result['region'] = l_region    
    result['EOP'] = l1
    result['EF'] = l2
    result['ES'] = l3
    result['EI'] = l4
    result['TP'] = l5
    return result

def lmdi_2year_nonpower(pol,start,end,data):
    l1, l2, l3, l4, l5 = [], [], [], [], []
    l_year, l_ind, l_region = [], [], []
    
    result = pd.DataFrame()
    for region in ['EASTERN','CENTRAL','WESTERN','NATIONAL']:    
        for ind in [22,25,26,30,31,32]:
            if region == 'NATIONAL':
                temp = df[df['ind2code']==ind]
            else:
                temp = df[(df['ind2code']==ind)&(df['region']==region)]            
            for year in [end]:
                keep = set()
                temp0 = temp[temp['year'] == start]
                temp1 = temp[temp['year'] == year]
                merge = pd.merge(temp1,temp0,on='firmid',how='left')
                firmset = set(merge[merge['EOP_y']==merge['EOP_y']]['firmid'])
                D1,D2,D3,D4,D5 = 0,0,0,0,0
                for firm in firmset:
                    em1 = temp1[temp1['firmid']==firm][pol].sum()
                    em0 = temp0[temp0['firmid']==firm][pol].sum()
                    if em1 != em0:
                        keep = keep|{firm}
                EM1 = temp1[temp1['firmid'].isin(keep)][pol].sum()
                EM0 = temp0[temp0['firmid'].isin(keep)][pol].sum()  
                for firm in keep:
                    df1 = temp1[temp1['firmid']==firm]
                    df0 = temp0[temp0['firmid']==firm]
                    if len(df1)!=1 | len(df0)!=1:
                        print ('error')
                    em1 = df1[pol].sum()
                    em0 = df0[pol].sum()
                    w = ((em1-em0)/(np.log(em1)-np.log(em0)))/((EM1 - EM0)/(np.log(EM1)-np.log(EM0)))
                    D1 = D1 + get(df1,df0,'EOP') * w
                    D2 = D2 + get(df1,df0,'EF') * w
                    D3 = D3 + get(df1,df0,'ES') * w
                    D4 = D4 + get(df1,df0,'EI') * w
                    D5 = D5 + get(df1,df0,'totalproduct_modify') * w
                else:
                    pass
                l1.append(np.exp(D1))
                l2.append(np.exp(D2))
                l3.append(np.exp(D3))
                l4.append(np.exp(D4))
                l5.append(np.exp(D5))
                l_region.append(region)
                l_year.append(year)
                l_ind.append(ind)
    result['year'] = l_year
    result['ind'] = l_ind    
    result['region'] = l_region 
    result['EOP'] = l1
    result['EF'] = l2
    result['ES'] = l3
    result['EI'] = l4
    result['TP'] = l5
    return result


def lmdi_2year_power(pol,start,end,data):
    result = pd.DataFrame()
    l1, l2, l3, l4 = [], [], [], []
    l_year, l_region = [], []
    for region in ['EASTERN','CENTRAL','WESTERN','NATIONAL']:
        if region == 'NATIONAL':
            temp = data
        else:
            temp = data[data['region']==region]
        for year in [end]:
            temp0 = temp[temp['year'] == start]
            temp1 = temp[temp['year'] == year]
            merge = pd.merge(temp1,temp0,on='plant_id',how='left')
            firmset = set(merge[merge['EOP_y']==merge['EOP_y']]['plant_id'])
            keep = set()
                   
            D1,D2,D3,D4 = 0,0,0,0
            for firm in firmset:
                em1 = temp1[temp1['plant_id']==firm][pol].sum()
                em0 = temp0[temp0['plant_id']==firm][pol].sum()
                if em1 != em0:
                    keep = keep|{firm}
            EM1 = temp1[temp1['plant_id'].isin(keep)][pol].sum()
            EM0 = temp0[temp0['plant_id'].isin(keep)][pol].sum()                
            for firm in keep:
                df1 = temp1[temp1['plant_id']==firm]
                df0 = temp0[temp0['plant_id']==firm] 
                if len(df1)!=1 | len(df0)!=1:
                    print ('error')
                em1 = df1[pol].sum()
                em0 = df0[pol].sum()
                w = ((em1-em0)/(np.log(em1)-np.log(em0)))/((EM1 - EM0)/(np.log(EM1)-np.log(EM0)))           
                D1 = D1 + get(df1,df0,'EOP') * w
                D2 = D2 + get(df1,df0,'EF') * w
                D3 = D3 + get(df1,df0,'EI') * w
                D4 = D4 + get(df1,df0,'generation') * w
            l1.append(np.exp(D1))
            l2.append(np.exp(D2))
            l3.append(np.exp(D3))
            l4.append(np.exp(D4))
            l_year.append(year)
            l_region.append(region)       
    result['year'] = l_year
    result['region'] = l_region        
    result['EOP'] = l1
    result['EF'] = l2
    result['EI'] = l3
    result['TP'] = l4
    return result


def lmdi_dynamic_power(pol,start,end,data):
    result = pd.DataFrame()
    l1, l2, l3, l4 = [], [], [], []
    l_year, l_region = [], []
    for region in ['EASTERN','CENTRAL','WESTERN','NATIONAL']:
        if region == 'NATIONAL':
            temp = data
        else:
            temp = data[data['region']==region]
        for year in range(start+1,end+1):
            temp0 = temp[temp['year'] == year - 1]
            temp1 = temp[temp['year'] == year]
            merge = pd.merge(temp1,temp0,on='plant_id',how='left')
            firmset = set(merge[merge['EOP_y']==merge['EOP_y']]['plant_id'])
            keep = set()
            D1,D2,D3,D4 = 0,0,0,0
            for firm in firmset:
                em1 = temp1[temp1['plant_id']==firm][pol].sum()
                em0 = temp0[temp0['plant_id']==firm][pol].sum()
                if em1 != em0:
                    keep = keep|{firm}
            EM1 = temp1[temp1['plant_id'].isin(keep)][pol].sum()
            EM0 = temp0[temp0['plant_id'].isin(keep)][pol].sum()                
            for firm in keep:
                df1 = temp1[temp1['plant_id']==firm]
                df0 = temp0[temp0['plant_id']==firm] 
                if len(df1)!=1 | len(df0)!=1:
                    print ('error')
                em1 = df1[pol].sum()
                em0 = df0[pol].sum()
                w = ((em1-em0)/(np.log(em1)-np.log(em0)))/((EM1 - EM0)/(np.log(EM1)-np.log(EM0)))
                D1 = D1 + get(df1,df0,'EOP') * w
                D2 = D2 + get(df1,df0,'EF') * w
                D3 = D3 + get(df1,df0,'EI') * w
                D4 = D4 + get(df1,df0,'generation') * w
            l1.append(np.exp(D1))
            l2.append(np.exp(D2))
            l3.append(np.exp(D3))
            l4.append(np.exp(D4))
            l_year.append(year)
            l_region.append(region)       
    result['year'] = l_year
    result['region'] = l_region        
    result['EOP'] = l1
    result['EF'] = l2
    result['EI'] = l3
    result['TP'] = l4
    return result


#using the non-power firm-level data
frame = pd.read_excel(r'.\data\dataset20201029.xlsx',sheet_name='non-power')
frame.loc[frame['so2emit']==0,'so2emit'] = pow(10,-10)
frame.loc[frame['noxemit']==0,'noxemit'] = pow(10,-10)
frame.loc[frame['smokedustemit']==0,'smokedustemit'] = pow(10,-10)

# non-power sectors: lmdi  for so2 
# =============================================================================
condition =  (frame['totalproduct_modify']>0) &  (frame['fossil']>0)  &  (frame['so2generate']>0)&(frame['so2emit']==frame['so2emit'])
df = frame[condition]
df['EOP'] = df['so2emit'].fillna(0)/ df['so2generate']
df['EF'] = df['so2generate'].fillna(0)/df['fossil']
df['ES'] = df['fossil'].fillna(0)/ df['energy']
df['EI'] = df['energy'].fillna(0)/ df['totalproduct_modify']
for item in ['ES','EI','EOP','EF']:
    df = df[df[item]!=np.inf]
 
data = df[df['ind2code'].isin({22,25,26,30,31,32})]
#2011 to 2014
result1 = lmdi_2year_nonpower('so2emit',2011,2014,data=data) # 2-year lmdi
result2 = lmdi_dynamic_nonpower('so2emit',2011,2014,data=data) # dynamic lmdi
result1.to_excel(r'.\final-result\lmdi\2year-so2.xlsx',index=None)
result2.to_excel(r'.\final-result\lmdi\dynamic-so2.xlsx',index=None)
#2009 to 2014
result1 = lmdi_2year_nonpower('so2emit',2009,2014,data=data) # 2-year lmdi
result2 = lmdi_dynamic_nonpower('so2emit',2009,2014,data=data) # dynamic lmdi
result1.to_excel(r'.\final-result\lmdi\base2009-2year-so2.xlsx',index=None)
result2.to_excel(r'.\final-result\lmdi\base2009-dynamic-so2.xlsx',index=None)

# non-power sectors: lmdi  for nox  
# =============================================================================
condition =  (frame['totalproduct_modify']>0) &  (frame['fossil']>0)  &  (frame['noxgenerate']>0)&(frame['noxemit']==frame['noxemit'])
df = frame[condition]   
df['ES'] = df['fossil'].fillna(0)/ df['energy']
df['EI'] = df['energy'].fillna(0)/ df['totalproduct_modify']
df['EOP'] = df['noxemit'].fillna(0)/ df['noxgenerate']
df['EF'] = df['noxgenerate'].fillna(0)/df['fossil']
for item in ['ES','EI','EOP','EF']:
    df = df[df[item]!=np.inf]
data = df[df['ind2code'].isin({22,25,26,30,31,32})]
#2011 to 2014
result1 = lmdi_2year_nonpower('noxemit',2011,2014,data=data) # 2-year lmdi
result2 = lmdi_dynamic_nonpower('noxemit',2011,2014,data=data) # dynamic lmdi
result1.to_excel(r'.\final-result\lmdi\2year-nox.xlsx',index=None)
result2.to_excel(r'.\final-result\lmdi\dynamic-nox.xlsx',index=None)
#2009 to 2014
result1 = lmdi_2year_nonpower('noxemit',2009,2014,data=data) # 2-year lmdi
result2 = lmdi_dynamic_nonpower('noxemit',2009,2014,data=data) # dynamic lmdi
result1.to_excel(r'.\final-result\lmdi\base2009-2year-nox.xlsx',index=None)
result2.to_excel(r'.\final-result\lmdi\base2009-dynamic-nox.xlsx',index=None)

# non-power sectors: lmdi  for pm   (2011 to 2013)
# =============================================================================
condition =  (frame['totalproduct_modify']>0) &  (frame['fossil']>0)  &  (frame['smokedustgenerate']>0)&(frame['smokedustemit']==frame['smokedustemit'])
df = frame[condition]   
df['ES'] = df['fossil'].fillna(0)/ df['energy']
df['EI'] = df['energy'].fillna(0)/ df['totalproduct_modify']
df['EOP'] = df['smokedustemit'].fillna(0)/ df['smokedustgenerate']
df['EF'] = df['smokedustgenerate'].fillna(0)/df['fossil']
for item in ['ES','EI','EOP','EF']:
    df = df[df[item]!=np.inf]
data = df[df['ind2code'].isin({22,25,26,30,31,32})]
#2011 to 2013
result1 = lmdi_2year_nonpower('smokedustemit',2011,2013,data=data) # 2-year lmdi
result2 = lmdi_dynamic_nonpower('smokedustemit',2011,2013,data=data) # dynamic lmdi
result1.to_excel(r'.\final-result\lmdi\2year-pm.xlsx',index=None)
result2.to_excel(r'.\final-result\lmdi\dynamic-pm.xlsx',index=None)
#2009 to 2013
result1 = lmdi_2year_nonpower('smokedustemit',2009,2013,data=data) # 2-year lmdi
result2 = lmdi_dynamic_nonpower('smokedustemit',2009,2013,data=data) # dynamic lmdi
result1.to_excel(r'.\final-result\lmdi\base2009-2year-pm.xlsx',index=None)
result2.to_excel(r'.\final-result\lmdi\base2009-dynamic-pm.xlsx',index=None)


# coal-fired power plants: lmdi  for so2 
# =============================================================================
frame = pd.read_excel(r'.\data\dataset20201029.xlsx',sheet_name='power')
condition = (frame['coal_gross']>0)  & (frame['generation']>0) & (frame['so2generate']>0) & (frame['so2emit']==frame['so2emit'])
data = frame[condition]   
data['EOP'] = data['so2emit']/data['so2generate']
data['EF'] = data['so2generate']/data['fossil']
data['EI'] = data['fossil']/data['generation']
#2011 to 2014
result1 = lmdi_2year_power('so2emit',2011,2014,data=data) # 2-year lmdi
result2 = lmdi_dynamic_power('so2emit',2011,2014,data=data) # dynamic lmdi
result1.to_excel(r'.\final-result\lmdi\power-2year-so2.xlsx',index=None)
result2.to_excel(r'.\final-result\lmdi\power-dynamic-so2.xlsx',index=None)

# coal-fired power plants: lmdi  for nox 
# =============================================================================
condition = (frame['coal_gross']>0)  & (frame['generation']>0) & (frame['noxgenerate']>0) & (frame['noxemit']==frame['noxemit'])
df = frame[condition]   
data = df.copy()
data['EOP'] = data['noxemit']/data['noxgenerate']
data['EF'] = data['noxgenerate']/data['fossil']
data['EI'] = data['fossil']/data['generation']
#2011 to 2014
result1 = lmdi_2year_power('noxemit',2011,2014,data=data) # 2-year lmdi
result2 = lmdi_dynamic_power('noxemit',2011,2014,data=data) # dynamic lmdi
result1.to_excel(r'.\final-result\lmdi\power-2year-nox.xlsx',index=None)
result2.to_excel(r'.\final-result\lmdi\power-dynamic-nox.xlsx',index=None)

# coal-fired power plants: lmdi  for pm 
# =============================================================================
condition = (frame['coal_gross']>0)  & (frame['generation']>0) & (frame['smokedustgenerate']>0) &(frame['smokedustemit']==frame['smokedustemit'])
data = frame[condition]   
data['EOP'] = data['smokedustemit']/data['smokedustgenerate']
data['EF'] = data['smokedustgenerate']/data['fossil']
data['EI'] = data['fossil']/data['generation']
#2011 to 2013
result1 = lmdi_2year_power('smokedustemit',2011,2013,data=data) # 2-year lmdi
result2 = lmdi_dynamic_power('smokedustemit',2011,2013,data=data) # dynamic lmdi
result1.to_excel(r'.\final-result\lmdi\power-2year-pm.xlsx',index=None)
result2.to_excel(r'.\final-result\lmdi\power-dynamic-pm.xlsx',index=None)


# =============================================================================
# Direct co-benefits: energy intensity adjustment
# =============================================================================

#Coal-fired power plants
region_map = {'EASTERN':'Eastern',
              'CENTRAL':'Central',
              'WESTERN':'Western',
              'NATIONAL':'National'}
def direct_cobenefit_power(temp0, pol):
    temp0['ef'] = temp0['fossil']/temp0['generation']
    potential = pd.DataFrame()
    l1, l2, l3, l4 = [], [], [], []
    for region in ['EASTERN','CENTRAL','WESTERN','NATIONAL']:
        if region == 'NATIONAL':
            data = temp0
        else:
            data = temp0[temp0['region']==region]
        wmean = data['fossil'].sum()/data['generation'].sum()
        smean = (data['fossil']/data['generation']).mean()
        med = (data['fossil']/data['generation']).median()
        highGroup1 = data[data['ef'] > wmean]
        highGroup2 = data[data['ef'] > smean]
        highGroup3 = data[data['ef'] > med]
        r1 = (highGroup1['ef'] - wmean)/highGroup1['ef']
        r2 = (highGroup2['ef'] - smean)/highGroup2['ef'] 
        r3 = (highGroup3['ef'] - med)/highGroup3['ef']
        potential1 = (r1 * highGroup1[pol]).sum()/data[pol].sum()
        potential2 = (r2 * highGroup2[pol]).sum()/data[pol].sum()    
        potential3 = (r3 * highGroup3[pol]).sum()/data[pol].sum()      
        l4.append(region)
        l1.append(potential1*(-100))
        l2.append(potential2*(-100))
        l3.append(potential3*(-100)) 
    potential['region'] = l4
    potential['indname'] = 'Plants'
    potential['weighted_average2'] = l1
    potential['arithmetic_mean2'] = l2
    potential['median2'] = l3
    return potential
frame = pd.read_excel(r'.\data\dataset20201029.xlsx',sheet_name='power')
condition = (frame['coal_gross']>0)  & (frame['generation']>0) & (frame['year']==2014)
df = frame[condition] 
temp = df.copy()
temp0 = temp.copy()
potential_so2_power = direct_cobenefit_power(temp0, 'so2emit')
potential_so2_power.to_excel(r'.\final-result\direct-ei\power-so2.xlsx',index=None,encoding='utf-8')

potential_co2_power = direct_cobenefit_power(temp0, 'co2EmitDirect')
potential_co2_power.to_excel(r'.\final-result\direct-ei\power-co2.xlsx',index=None,encoding='utf-8')

potential_nox_power = direct_cobenefit_power(temp0, 'noxemit')
potential_nox_power.to_excel(r'.\final-result\direct-ei\power-nox.xlsx',index=None,encoding='utf-8')

condition = (frame['coal_gross']>0)  & (frame['generation']>0) & (frame['year']==2013)
df = frame[condition] 
temp = df.copy()
temp0 = temp.copy()
potential_pm_power = direct_cobenefit_power(temp0, 'smokedustemit')
potential_pm_power.to_excel(r'.\final-result\direct-ei\power-pm.xlsx',index=None,encoding='utf-8')


#non-power sectors
def direct_cobenefit_nonpower(df, pol):
    df['ind4code'] = (df['industry_code']/1).astype(int)
    ind4_list = list(set(df['ind4code']))
    ind4_list.sort()
    ind_list=[22,25,26,30,31,32]
    
    #1.weighted average by total product
    wmean = pd.DataFrame()
    wmean['ind'] = ind4_list
    l0 = []
    for ind in  ind4_list:
        condition = df['ind4code']==ind 
        temp = df[condition] 
        totalcoal = temp['energy'].sum()
        product = temp['totalproduct_modify'].sum()
        l0.append(totalcoal/product)
    wmean['ef'] = l0  
    
    #2.Arithmetic mean
    smean = pd.DataFrame()
    smean['ind'] = ind4_list
    l0 = []
    for ind in  ind4_list:
        condition = df['ind4code']==ind
        temp = df[condition] 
        temp['ef'] = temp['energy']/temp['totalproduct_modify']
        ef = temp['ef'].mean()
    
        l0.append(ef)
    smean['ef'] = l0
    
    #3.median
    med = pd.DataFrame()
    med['ind'] = ind4_list
    l0 = []
    for ind in  ind4_list:
        condition = df['ind4code']==ind
        temp = df[condition] 
        temp['ef'] = temp['energy']/temp['totalproduct_modify']
        temp['es'] = temp['fossil']/temp['energy']
        ef = temp['ef'].median()
    
        l0.append(ef)
    med['ef'] = l0
    mapping_ef1=dict(zip(list(wmean['ind']), list(wmean['ef'])))
    mapping_ef2=dict(zip(list(smean['ind']), list(smean['ef'])))
    mapping_ef3=dict(zip(list(med['ind']), list(med['ef'])))

    df['ef'] = df['energy'].fillna(0)/ df['totalproduct_modify']
    df['weighted_average'] = df['ind4code'].map(mapping_ef1)
    df['arithmetic_mean'] = df['ind4code'].map(mapping_ef2)
    df['median'] = df['ind4code'].map(mapping_ef3)
    
    potential_region = pd.DataFrame()
    l1, l2, l3 = [], [], []
    l_region, l_ind = [], []
    for region in ['EASTERN','CENTRAL','WESTERN','NATIONAL']:
        for ind in ind_list:
            if region == 'NATIONAL':
                temp = df[(df['ind2code'] == ind)]
            else:           
                temp = df[(df['ind2code'] == ind)&(df['region']==region)]
                
            highGroup1 = temp[temp['ef'] > temp['weighted_average']]
            r1 = (highGroup1['ef'] - highGroup1['weighted_average'])/highGroup1['ef']
            potential1 = (r1* highGroup1[pol]).sum()/temp[pol].sum()
           
            highGroup2 = temp[temp['ef'] > temp['arithmetic_mean']]
            r2 = (highGroup2['ef'] - highGroup2['arithmetic_mean'])/highGroup2['ef']
            potential2 = (r2* highGroup2[pol]).sum()/temp[pol].sum()
           
            highGroup3 = temp[temp['ef'] > temp['median']]
            r3 = (highGroup3['ef'] - highGroup3['median'])/highGroup3['ef']
            potential3 = (r3* highGroup3[pol]).sum()/temp[pol].sum()
           
            l1.append(potential1*100)
            l2.append(potential2*100)
            l3.append(potential3*100)
            l_region.append(region)
            l_ind.append(ind)    
            
    potential_region['region'] = l_region
    potential_region['ind'] = l_ind
    potential_region['weighted_average'] = l1 
    potential_region['arithmetic_mean'] = l2 
    potential_region['median'] = l3 
    
    potential = pd.DataFrame()
    l1, l2, l3 = [], [], []
    l_region, l_ind = [], []
    for region in ['EASTERN','CENTRAL','WESTERN','NATIONAL']:
        for ind in ind4_list:
            if region == 'NATIONAL':
                temp = df[(df['ind4code'] == ind)]
            else:
                temp = df[(df['ind4code'] == ind) & (df['region'] == region)]
            if len(temp) ==0:
                continue
            highGroup1 = temp[temp['ef'] > temp['weighted_average']]
            r1 = (highGroup1['ef'] - highGroup1['weighted_average'])/highGroup1['ef']
            potential1 = (r1* highGroup1[pol]).sum()/temp[pol].sum()
           
            highGroup2 = temp[temp['ef'] > temp['arithmetic_mean']]
            r2 = (highGroup2['ef'] - highGroup2['arithmetic_mean'])/highGroup2['ef']
            potential2 = (r2* highGroup2[pol]).sum()/temp[pol].sum()
           
            highGroup3 = temp[temp['ef'] > temp['median']]
            r3 = (highGroup3['ef'] - highGroup3['median'])/highGroup3['ef']
            potential3 = (r3* highGroup3[pol]).sum()/temp[pol].sum()
           
            l1.append(potential1*100)
            l2.append(potential2*100)
            l3.append(potential3*100)
            
            l_region.append(region)
            l_ind.append(ind)
    potential['region'] = l_region
    potential['ind4code'] = l_ind
    potential['weighted_average'] = l1 
    potential['arithmetic_mean'] = l2 
    potential['median'] = l3 
    
    potential[['weighted_average','arithmetic_mean','median']] = potential[['weighted_average','arithmetic_mean','median']]  * (-1)
    potential = potential[potential['weighted_average']<0]
    potential['ind'] = (potential['ind4code']/100).astype(int)
    
    potential_region = potential_region[['weighted_average','arithmetic_mean','median','region','ind']]
    potential_region.rename(columns={'weighted_average':'weighted_average2',
                                         'arithmetic_mean':'arithmetic_mean2',
                                         'median':'median2',},inplace = True)
    potential_region[['weighted_average2','arithmetic_mean2','median2']] = potential_region[['weighted_average2','arithmetic_mean2','median2']]  * (-1)
    potential = pd.merge(potential,potential_region, how = 'left', on = ['ind','region'])
    return potential
frame = pd.read_excel(r'.\data\dataset20201029.xlsx',sheet_name='non-power')

condition =  (frame['totalproduct_modify']>0) &  (frame['fossil']>0)  & (frame['year']==2014)
df = frame[condition & frame['ind2code'].isin({22,25,26,30,31,32})]   

potential_so2 = direct_cobenefit_nonpower(df, 'so2emit')
potential_so2.to_excel(r'.\final-result\direct-ei\nonpower_so2.xlsx',index=None,encoding='utf-8')

potential_co2 = direct_cobenefit_nonpower(df, 'co2EmitDirect')
potential_co2.to_excel(r'.\final-result\direct-ei\nonpower_co2.xlsx',index=None,encoding='utf-8')

potential_nox = direct_cobenefit_nonpower(df, 'noxemit')
potential_nox.to_excel(r'.\final-result\direct-ei\nonpower_nox.xlsx',index=None,encoding='utf-8')

condition =  (frame['totalproduct_modify']>0) &  (frame['fossil']>0)  & (frame['year']==2013)
df = frame[condition & frame['ind2code'].isin({22,25,26,30,31,32})]   
potential_pm = direct_cobenefit_nonpower(df, 'smokedustemit')
potential_pm.to_excel(r'.\final-result\direct-ei\nonpower_pm.xlsx',index=None,encoding='utf-8')

#Boxplot
ind_map = {22:'Paper.',
           25:"Petroleum.",
           26:'Chemical.',
           30:'Non-meta.',
           31:'Ferrous.',
           32:'Non-ferr.'}

potential_pm['indname'] = potential_pm['ind'].map(ind_map)
potential_so2['indname'] = potential_so2['ind'].map(ind_map)
potential_nox['indname'] = potential_nox['ind'].map(ind_map)
potential_co2['indname'] = potential_co2['ind'].map(ind_map)


ind_color = {'Paper.':'firebrick',
           'Petroleum.':"blue",
           'Chemical.':'green',
           'Non-meta.':'purple',
           'Ferrous.':'darkorange',
           'Non-ferr.':'deepskyblue',
           'Plants':'gray'}
no= {1:'a',
     2:'b',
     3:'c',
     4:'d',
     5:'e',
     6:'f',
     7:'g',
     8:'h'}
for s  in ['weighted_average','arithmetic_mean','median']:
    standard = s
    standard1 = standard
    plt.rcParams.update({'font.size': 20})
    fig = plt.figure(figsize=(25,20), frameon = False, dpi=300)
    plt.rc('font',family='calibri') 
    
    for item in [standard1,]:   
        itr = 0
        for region in ['EASTERN','CENTRAL','WESTERN','NATIONAL']:
            data_plot_pm = potential_pm[potential_pm['region']==region]
            data_plot_so2 = potential_so2[potential_so2['region']==region]
            data_plot_nox = potential_nox[potential_nox['region']==region]
            data_plot_co2 = potential_co2[potential_co2['region']==region]
 
            itr = itr + 1
            if item == standard1:
                ax1 = fig.add_subplot(4,4,itr) 
                ax2 = fig.add_subplot(4,4,itr+4) 
                ax3 = fig.add_subplot(4,4,itr+8) 
                ax4 = fig.add_subplot(4,4,itr+12) 
            sns.boxplot(x="indname", y=item, data=data_plot_so2, whis=(10,90),palette=ind_color,
                        linewidth=1,ax=ax1,saturation=1,showfliers = False)  
            sns.boxplot(x="indname", y=item, data=data_plot_nox, whis=(10,90),palette=ind_color,
                        linewidth=1,ax=ax2,saturation=1,showfliers = False)              
            sns.boxplot(x="indname", y=item, data=data_plot_pm, whis=(10,90),palette=ind_color,
                        linewidth=1,ax=ax3,saturation=1,showfliers = False)
            
            sns.boxplot(x="indname", y=item, data=data_plot_co2, whis=(10,90),palette=ind_color,
                linewidth=1,ax=ax4,saturation=1,showfliers = False)
            
            ax1.set_xlabel('')     
            ax2.set_xlabel('')  
            ax3.set_xlabel('')     
            ax4.set_xlabel('')  

            if  (item == standard1):
                ax1.set_title(region_map[region],fontsize=24)
                    
            if itr ==1:    
                ax1.set_ylabel('SO2 (%)',fontsize=24)
                ax2.set_ylabel('NOx (%)',fontsize=24)                  
                ax3.set_ylabel('PM (%)',fontsize=24)
                ax4.set_ylabel('CO2 (%)',fontsize=24)
                
                ax1.set_yticks([-100,-80,-60,-40,-20,0])
                ax2.set_yticks([-100,-80,-60,-40,-20,0])    
                ax3.set_yticks([-100,-80,-60,-40,-20,0])
                ax4.set_yticks([-100,-80,-60,-40,-20,0])                 
            else:
                ax1.set_yticks([-100,-80,-60,-40,-20,0])
                ax2.set_yticks([-100,-80,-60,-40,-20,0])    
                ax3.set_yticks([-100,-80,-60,-40,-20,0])
                ax4.set_yticks([-100,-80,-60,-40,-20,0]) 
                ax1.set_yticklabels([-100,-80,-60,-40,-20,0], fontsize=0)   
                ax2.set_yticklabels([-100,-80,-60,-40,-20,0], fontsize=0)   
                ax3.set_yticklabels([-100,-80,-60,-40,-20,0], fontsize=0)   
                ax4.set_yticklabels([-100,-80,-60,-40,-20,0], fontsize=0)   
                ax1.set_ylabel('')
                ax2.set_ylabel('')                  
                ax3.set_ylabel('')
                ax4.set_ylabel('')
            
            ax1.set_xticklabels(['Paper.',"Petroleum.",'Chemical.','Non-meta.','Ferrous.','Non-ferr.'], fontsize=0)   
            ax2.set_xticklabels(['Paper.',"Petroleum.",'Chemical.','Non-meta.','Ferrous.','Non-ferr.'], fontsize=0)   
            ax3.set_xticklabels(['Paper.',"Petroleum.",'Chemical.','Non-meta.','Ferrous.','Non-ferr.'], fontsize=0)   
            ax4.set_xticklabels(['Paper.',"Petroleum.",'Chemical.','Non-meta.','Ferrous.','Non-ferr.'], fontsize=0) 
            
            ax1.set_ylim([-100,5])
            ax2.set_ylim([-100,5])
            ax3.set_ylim([-100,5])
            ax4.set_ylim([-100,5])
            if (itr==1)&(item == standard1):
                ax1.text(-1.5,0,no[1] , fontdict={'size': '32', 'color': 'black','weight':'bold'})
                ax2.text(-1.5,0,no[2] , fontdict={'size': '32', 'color': 'black','weight':'bold'})
                ax3.text(-1.5,0,no[3] , fontdict={'size': '32', 'color': 'black','weight':'bold'})
                ax4.text(-1.5,0,no[4] , fontdict={'size': '32', 'color': 'black','weight':'bold'})
          
            ax1.axhline(y=0,ls="--",c="gray",alpha=0.3)
            ax2.axhline(y=0,ls="--",c="gray",alpha=0.3)
          
            ax3.axhline(y=0,ls="--",c="gray",alpha=0.3)
            ax4.axhline(y=0,ls="--",c="gray",alpha=0.3)
            
            for tick in ax1.get_xticklabels():
                tick.set_rotation(25)
            for tick in ax2.get_xticklabels():
                tick.set_rotation(25)           
            for tick in ax3.get_xticklabels():
                tick.set_rotation(25)
            for tick in ax4.get_xticklabels():
                tick.set_rotation(25)
    fig.subplots_adjust(hspace=0.1, wspace=0.1)
    
    import matplotlib.patches as mpatches
    import matplotlib.lines as mlines
    labels = ['Paper',"Petroleum",'Chemical','Non-metallic','Ferrous','Non-ferrous']
    color = ['firebrick',"blue",'green','purple','darkorange','deepskyblue']
    patches = [ mpatches.Patch(color=color[i], label="{:s}".format(labels[i]) ) for i in range(len(color)) ]
    plt.legend(handles=patches, ncol=6,loc='lower center', 
                bbox_to_anchor=(-1.4,-0.3),fancybox=False, shadow=False,frameon=False,fontsize=24)
    
    fig.savefig(r'.\final-result\direct-ei\direct-cobefit-3pol-%s.png'%standard,
                dpi=300,bbox_inches="tight")
     
#comparison between different benchmark (weighted average, arithmetic mean, median)
marker_map = {'weighted_average2':'o',
              'arithmetic_mean2':'^',
              'median2':'x'}
plt.rcParams.update({'font.size': 20})
fig = plt.figure(figsize=(25,20), frameon = False, dpi=300)
plt.rc('font',family='calibri') 
itr = 0 
#so2
for region in ['EASTERN','CENTRAL','WESTERN','NATIONAL']:
    itr = itr + 1
    ax1 = fig.add_subplot(4,4,itr)
    for ind in ['Paper.',"Petroleum.",'Chemical.','Non-meta.','Ferrous.','Non-ferr.','Plants']:
        if ind !='Plants':
            temp = potential_so2[(potential_so2['region']==region)&(potential_so2['indname']==ind)]
        else:
            temp = potential_so2_power[potential_so2_power['region']==region]
        for item in  ['weighted_average2','arithmetic_mean2','median2']:
            ax1.scatter(x='indname',y = item,data=temp,color=ind_color[ind],s=120,marker = marker_map[item])
    ax1.set_yticks([-100,-80,-60,-40,-20,0])
    for tick in ax1.get_xticklabels():
        tick.set_rotation(25)           
    ax1.axhline(y=0,ls="--",c="gray",alpha=0.3)
    ax1.set_ylim(-100,5)
    ax1.set_title(region)
    ax1.set_ylabel('SO2 (%)')
    if itr ==1:
        ax1.text(-1.5,5,no[1] , fontdict={'size': '32', 'color': 'black','weight':'bold'})
#nox    
for region in ['EASTERN','CENTRAL','WESTERN','NATIONAL']:
    itr = itr + 1
    ax1 = fig.add_subplot(4,4,itr)
    for ind in ['Paper.',"Petroleum.",'Chemical.','Non-meta.','Ferrous.','Non-ferr.','Plants']:
        if ind !='Plants':
            temp = potential_nox[(potential_nox['region']==region)&(potential_nox['indname']==ind)]
        else:
            temp = potential_nox_power[potential_nox_power['region']==region]
        for item in  ['weighted_average2','arithmetic_mean2','median2']:
            ax1.scatter(x='indname',y = item,data=temp,color=ind_color[ind],s=120,marker = marker_map[item])
    ax1.set_yticks([-100,-80,-60,-40,-20,0])
    for tick in ax1.get_xticklabels():
        tick.set_rotation(25)           
    ax1.axhline(y=0,ls="--",c="gray",alpha=0.3)
    ax1.set_ylim(-100,5)
    ax1.set_ylabel('NOx (%)')
    if itr ==5:
        ax1.text(-1.5,5,no[2] , fontdict={'size': '32', 'color': 'black','weight':'bold'})
#pm
for region in ['EASTERN','CENTRAL','WESTERN','NATIONAL']:
    itr = itr + 1
    ax1 = fig.add_subplot(4,4,itr)
    for ind in ['Paper.',"Petroleum.",'Chemical.','Non-meta.','Ferrous.','Non-ferr.','Plants']:
        if ind !='Plants':
            temp = potential_pm[(potential_pm['region']==region)&(potential_pm['indname']==ind)]
        else:
            temp = potential_pm_power[potential_pm_power['region']==region]
        for item in  ['weighted_average2','arithmetic_mean2','median2']:
            ax1.scatter(x='indname',y = item,data=temp,color=ind_color[ind],s=120,marker = marker_map[item])
    ax1.set_yticks([-100,-80,-60,-40,-20,0])
    for tick in ax1.get_xticklabels():
        tick.set_rotation(25)           
    ax1.axhline(y=0,ls="--",c="gray",alpha=0.3)
    ax1.set_ylim(-100,5)
    ax1.set_ylabel('PM (%)')
    if itr ==9:
        ax1.text(-1.5,5,no[3] , fontdict={'size': '32', 'color': 'black','weight':'bold'})    
#co2    
for region in ['EASTERN','CENTRAL','WESTERN','NATIONAL']:
    itr = itr + 1
    ax1 = fig.add_subplot(4,4,itr)
    for ind in ['Paper.',"Petroleum.",'Chemical.','Non-meta.','Ferrous.','Non-ferr.','Plants']:
        if ind !='Plants':        
            temp = potential_co2[(potential_co2['region']==region)&(potential_co2['indname']==ind)]
        else:
            temp = potential_co2_power[potential_co2_power['region']==region]
        for item in  ['weighted_average2','arithmetic_mean2','median2']:
            ax1.scatter(x='indname',y = item,data=temp,color=ind_color[ind],s=120,marker = marker_map[item])  
    ax1.set_yticks([-100,-80,-60,-40,-20,0])
    for tick in ax1.get_xticklabels():
        tick.set_rotation(25)  
    ax1.axhline(y=0,ls="--",c="gray",alpha=0.3)

    ax1.set_ylim(-100,5)   
    ax1.set_ylabel('CO2 (%)')
    if itr ==13:
        ax1.text(-1.5,5,no[4] , fontdict={'size': '32', 'color': 'black','weight':'bold'})
fig.subplots_adjust(hspace=0.4, wspace=0.3)

import matplotlib.patches as mpatches
import matplotlib.lines as mlines
labels = ['Paper',"Petroleum",'Chemical','Non-metallic','Ferrous','Non-ferrous','Coal-fired Power Plants']
color = ['firebrick',"blue",'green','purple','darkorange','deepskyblue','gray']
patches = [ mpatches.Patch(color=color[i], label="{:s}".format(labels[i]) ) for i in range(len(color)) ]

m_patch1, = plt.plot([], "o", markersize=15,label='Weighted Average',color='black')
m_patch2, = plt.plot([], "^", markersize=15, label='Arithmetic Mean',color='black')
m_patch3, = plt.plot([], "x", markersize=15, label='Median',color='black')

ax1.set_yticks([-100,-80,-60,-40,-20,0])
l1 = plt.legend(handles=patches, ncol=4,loc='lower center', 
            bbox_to_anchor=(-2.5,-0.8),fancybox=False, shadow=False,frameon=False)
plt.legend(handles=[m_patch1,m_patch2,m_patch3], ncol=2,loc='lower center', 
            bbox_to_anchor=(-0.3,-0.8),fancybox=False, shadow=False,frameon=False)
plt.gca().add_artist(l1)         
fig.savefig(r'.\final-result\direct-ei\direct-ei-compare-3pol.png',
            dpi=300,bbox_inches="tight")

##get iqr
for s  in ['weighted_average','arithmetic_mean','median']:
    standard = s
    standard1 =  standard
    plt.rcParams.update({'font.size': 20})
    fig = plt.figure(figsize=(25,20), frameon = False, dpi=300)
    plt.rc('font',family='calibri') 
    so2_pc25 = []
    so2_pc75 = []
    nox_pc25 = []
    nox_pc75 = []
    pm_pc25 = []
    pm_pc75 = []
    co2_pc25 = []  
    co2_pc75 = [] 
    l_region = []
    l_ind = []    
    for item in [standard1,]:   
        itr = 0
        for region in ['EASTERN','CENTRAL','WESTERN','NATIONAL']:
            for ind in [22,25,26,30,31,32]:
                data_plot_pm = potential_pm[(potential_pm['region']==region)&(potential_pm['ind']==ind)]
                data_plot_so2 = potential_so2[(potential_so2['region']==region)&(potential_so2['ind']==ind)]
                data_plot_nox = potential_nox[(potential_nox['region']==region)&(potential_nox['ind']==ind)]
                data_plot_co2 = potential_co2[(potential_co2['region']==region)&(potential_co2['ind']==ind)]
    
                itr = itr + 1
                if item == standard1:
                    ax1 = fig.add_subplot(4,4,1) 
                    ax2 = fig.add_subplot(4,4,2) 
                    ax3 = fig.add_subplot(4,4,3) 
                    ax4 = fig.add_subplot(4,4,4)  
                g1= ax1.boxplot(data_plot_so2[item], whis=(10,90),)
                g2= ax2.boxplot(data_plot_nox[item], whis=(10,90),)
                g3= ax3.boxplot(data_plot_pm[item], whis=(10,90),)
                g4= ax4.boxplot(data_plot_co2[item], whis=(10,90),)             
                iqr1 = g1['boxes'][0]
                iqr2 = g2['boxes'][0]
                iqr3 = g3['boxes'][0]
                iqr4 = g4['boxes'][0]     
                so2_pc25.append(iqr1.get_ydata().min())
                so2_pc75.append(iqr1.get_ydata().max())
                nox_pc25.append(iqr2.get_ydata().min())
                nox_pc75.append(iqr2.get_ydata().max()) 
                pm_pc25.append(iqr3.get_ydata().min())
                pm_pc75.append(iqr3.get_ydata().max())
                co2_pc25.append(iqr4.get_ydata().min())
                co2_pc75.append(iqr4.get_ydata().max())  
                l_region.append(region)
                l_ind.append(ind_map[ind])
    
    result = pd.DataFrame()
    result['region'] = l_region
    result['ind'] = l_ind
    result['so2_25'] = so2_pc25
    result['so2_75'] = so2_pc75
    result['nox_25'] = nox_pc25
    result['nox_75'] = nox_pc75
    result['pm_25'] = pm_pc25
    result['pm_75'] = pm_pc75
    result['co2_25'] = co2_pc25
    result['co2_75'] = co2_pc75
    
    result.to_excel(r'.\final-result\direct-ei\direct_iqr_%s.xlsx' %s,index=None)
    



# =============================================================================
# Indirect co-benefit： scale structure adjustment
# =============================================================================
ind_map = {22:'Paper.',
           25:"Petroleum.",
           26:'Chemical.',
           30:'Non-metallic.',
           31:'Ferrous.',
           32:'Non-ferrous.',
           44:'Coal-fired Plants'}
ind_marker = {22:'p',
             25:'s',
             26:'P',
             30:'^',
             31:'X',
             32:'v',
             44:'o'}
ind_color = {22:'firebrick',
           25:"blue",
           26:'green',
           30:'purple',
           31:'darkorange',
           32:'deepskyblue',
           44:'gray'}
industry_color = {ind_map[22]:'firebrick',
           ind_map[25]:"blue",
           ind_map[26]:'green',
           ind_map[30]:'purple',
           ind_map[31]:'darkorange',
           ind_map[32]:'deepskyblue',
           ind_map[44]:'gray'} 

def indirect_scale(temp, temp0, pol, label,itr):
    for region in ['EASTERN','CENTRAL','WESTERN','NATIONAL']:
        record = pd.DataFrame()
        record_ele = pd.DataFrame()
        record['shutdownRate'] = X
        record_ele['shutdownRate'] = X
        itr = itr + 1
        ax1  = fig.add_subplot(4,4,itr)    
        for ind in [22,25,26,30,31,32,44]:        
            if ind ==44:            
                if region == 'NATIONAL':
                    data = temp0
                else:
                    data = temp0[temp0['region']==region]
            else:
                if region == 'NATIONAL':
                    data=temp[temp['ind2code']==ind]
                else:
                    data=temp[(temp['ind2code']==ind)&(temp['region']==region)]
            if ind !=44:        
                mag = 'totalproduct_modify'      
            else:
                mag = 'supply'
            l = [] 
            total = data[pol].sum()

            for x in X:
                bottom = data[mag].quantile(x/100)
                up = data[mag].quantile((100-x)/100)
                f = data.sort_values([mag],ascending=True)
                f['scale_sort'] = range(len(f))          
                shut_id = f[f[mag]<= bottom]['scale_sort'].max()+1
                expand_id = f[f[mag]>=up]['scale_sort'].min()-1
                
                shut_group = f[f['scale_sort']<=shut_id]
                expand_group = f[f['scale_sort']>=expand_id]     
                if ind != 44:
                    ele_delta = expand_group['stdele'].sum()*(shut_group[mag].sum()/expand_group[mag].sum()) - shut_group['stdele'].sum() 
                    if region == 'NATIONAL':
                        ratio = (ele_delta/temp0['supply'].sum())/0.94
                        delta = ratio * temp0[pol].sum() -shut_group[pol].sum() +  expand_group[pol].sum()*(shut_group[mag].sum()/expand_group[mag].sum()) 
                    else:
                        ratio = (ele_delta/temp0[temp0['region']==region]['supply'].sum())/0.94
                        delta = ratio * temp0[temp0['region']==region][pol].sum()-shut_group[pol].sum() +  expand_group[pol].sum()*(shut_group[mag].sum()/expand_group[mag].sum()) 

                else:    
                    delta = expand_group[pol].sum()*(shut_group[mag].sum()/expand_group[mag].sum())  -shut_group[pol].sum()                     
                potential = delta/total
                
                l.append(potential*100)          
            if ind == 22:
                l1, = ax1.plot(X,l,color=ind_color[ind],linestyle = '-',
                          marker=ind_marker[ind])
            if ind == 25:
                l2, = ax1.plot(X,l,color=ind_color[ind],linestyle = '-',
                          marker=ind_marker[ind])
            if ind == 26:
                l3, = ax1.plot(X,l,color=ind_color[ind],linestyle = '-',
                          marker=ind_marker[ind])
            if ind == 30:
                l4, = ax1.plot(X,l,color=ind_color[ind],linestyle = '-',
                          marker=ind_marker[ind])
            if ind == 31:
                l5, = ax1.plot(X,l,color=ind_color[ind],linestyle = '-',
                          marker=ind_marker[ind])
            if ind == 32:
                l6, = ax1.plot(X,l,color=ind_color[ind],linestyle = '-',
                          marker=ind_marker[ind])    
            if ind == 44:
                l7, = ax1.plot(X,l,color=ind_color[ind],linestyle = '-',
                          marker=ind_marker[ind])   
            ax1.axhline(y=0,ls="--",c="gray",alpha=0.3)
            record[str(ind)] = l
     
        record.to_excel(r'.\final-result\indirect-scale\%s_%s.xlsx'% (label,region),index=None,encoding='utf-8')
        
        ax1.set_xticks([5,10,15,20,25,30])
        if label != 'CO2':
            ax1.set_ylim([-25,5])
            ax1.set_yticks([-25,-20,-15,-10,-5,0,5])
            
        else:
            ax1.set_ylim([-6,3])
            ax1.set_yticks([-6,-4,-2,0,2])
            
        ax1.set_ylabel(label+' (%)',fontsize=28)    
        if itr <5:
            ax1.set_title(region,fontsize=28)
        if itr ==1:
            ax1.text(0,6.5,'a' , fontdict={'size': '32', 'color': 'black','weight':'bold'})
        if itr ==5:
            ax1.text(0,6.5,'b' , fontdict={'size': '32', 'color': 'black','weight':'bold'})
        if itr ==9:
            ax1.text(0,6.5,'c' , fontdict={'size': '32', 'color': 'black','weight':'bold'})            
        if itr ==13:
            ax1.text(0,3,'d' , fontdict={'size': '32', 'color': 'black','weight':'bold'})
        if itr == 16:
            plt.legend((l1,l2,l3,l4,l5,l6,l7),('Paper.',"Petroleum.",'Chemical.','Non-metallic.','Ferrous.','Non-ferrous.','Coal-fired Power Plants'),
                      loc='lower left',frameon=False, ncol=4,columnspacing=1,fontsize=24,
                      bbox_to_anchor=(-3.5,-0.73))
            plt.text(-52,-8.5,'Assumed Percentile',fontsize=24)
    
frame = pd.read_excel(r'.\data\dataset20201029.xlsx',sheet_name='non-power')

condition =(frame['totalproduct_modify']>0) &  (frame['fossil']>0) 
df = frame[condition]   
df['ind2code'] = (df['industry_code']/100).astype(int)
ind2_list = list(set(df['ind2code']))
ind2_list.sort()
indcond =  {22,25,26,30,31,32}
df = df[df['ind2code'].isin(indcond)]
frame = pd.read_excel(r'.\data\dataset20201029.xlsx',sheet_name='power')

condition = (frame['coal_gross']>0)  & (frame['generation']>0)
df_ele = frame[condition] 

X = np.arange(5, 35, 5)
plt.rcParams.update({'font.size': 24})
plt.rc('font',family='calibri') 
fm._rebuild()
fig = plt.figure(figsize=(25,20), frameon = False, dpi=300)

temp = df[df['year']==2014]
temp0 = df_ele[df_ele['year']==2014]
indirect_scale(temp, temp0, 'so2emit', 'SO2',0)
indirect_scale(temp, temp0, 'noxemit', 'NOx',4)

temp = df[df['year']==2013]
temp0 = df_ele[df_ele['year']==2013]
indirect_scale(temp, temp0, 'smokedustemit', 'PM',8)

temp = df[df['year']==2014]
temp0 = df_ele[df_ele['year']==2014]
indirect_scale(temp, temp0, 'co2EmitDirect', 'CO2',12)

fig.subplots_adjust(hspace=0.4, wspace=0.4)

fig.savefig(r'.\final-result\indirect-scale\indirect-struct-3pol.png',
            dpi=300,bbox_inches="tight")
 


# =============================================================================
# indrect co-benefit:electrification
# =============================================================================
ind_map = {22:'Paper.',
           25:"Petroleum.",
           26:'Chemical.',
           30:'Non-metallic.',
           31:'Ferrous.',
           32:'Non-ferrous.',
           44:'Coal-fired Plants'}
ind_marker = {22:'p',
             25:'s',
             26:'P',
             30:'^',
             31:'X',
             32:'v',
             44:'o'}
ind_color = {22:'firebrick',
           25:"blue",
           26:'green',
           30:'purple',
           31:'darkorange',
           32:'deepskyblue',
           44:'gray'}
industry_color = {ind_map[22]:'firebrick',
           ind_map[25]:"blue",
           ind_map[26]:'green',
           ind_map[30]:'purple',
           ind_map[31]:'darkorange',
           ind_map[32]:'deepskyblue',
           ind_map[44]:'gray'} 
mark = {1:'a',2:'b',3:'c',4:'d'}


def indirect_electrification(temp, temp0, target):
    X = np.arange(5, 35, 5)
    plt.rcParams.update({'font.size': 24})
    plt.rc('font',family='calibri') 
    fm._rebuild()
    
    fig = plt.figure(figsize=(25,20), frameon = False, dpi=300)
    itr = 0    
    for region in ['EASTERN','CENTRAL','WESTERN','NATIONAL']:
        record1 = pd.DataFrame()
        record2 = pd.DataFrame()
        record3 = pd.DataFrame() 
        record4 = pd.DataFrame() 
        record1['Percentage'] = X    
        record2['Percentage'] = X  
        record3['Percentage'] = X
        record4['Percentage'] = X       
        itr = itr + 1
        ax1 = fig.add_subplot(6,4,itr)  
        ax2 = fig.add_subplot(6,4,itr+4) 
        ax3 = fig.add_subplot(6,4,itr+8)
        ax4 = fig.add_subplot(6,4,itr+12)
    
        for ind in [22,25,26,30,31,32]:
            l_so2 = []
            l_co2 = []
            l_ele = []
            l_nox = []
            l_pm = []
            if region == 'NATIONAL':
                data=temp[(temp['ind2code']==ind)&(temp['year']==2014)]
                data0 = temp0[temp0['year']==2014]
                data_pm = temp[(temp['ind2code']==ind)&(temp['year']==2013)]
                data0_pm = temp0[(temp0['year']==2013)]
                
            else:
                data=temp[(temp['ind2code']==ind)&(temp['region']==region)&(temp['year']==2014)]
                data0=temp0[(temp0['region']==region)&(temp0['year']==2014)]
                data_pm = temp[(temp['ind2code']==ind)&(temp['year']==2013)&(temp['region']==region)]
                data0_pm = temp0[(temp0['region']==region)&(temp0['year']==2013)]
    
            for x in X:
                total_so2 = data['so2emit'].sum() 
                total_co2 = data['co2EmitDirect'].sum() 
                total_nox = data['noxemit'].sum()
                total_pm = data_pm['smokedustemit'].sum() 

                rate = x/100
                expand_group = data0
                
                expand_group_pm = data0_pm          
                
                minus_fossil = rate * data['fossil'].sum()  * 0.7 ###锅炉效率
                minus_fossil_pm = rate * data_pm['fossil'].sum()  * 0.7
                minus_so2 = rate * total_so2
                minus_nox = rate * total_nox
                minus_pm = rate * total_pm
                minus_co2 = rate * total_co2
                
                add_ele = (minus_fossil/1.229)/0.94
                add_ele_pm = (minus_fossil_pm/1.229)/0.94
                
                expand_group['supply'] = expand_group['generation']*(1-expand_group['cons_rate']/100)
                add_so2 = expand_group['so2emit'].sum() *  add_ele * (1-target/100)/ (expand_group['supply'].sum())
                add_co2 = expand_group['co2EmitDirect'].sum() *  add_ele * (1-target/100)/ expand_group['supply'].sum()
                add_nox = expand_group['noxemit'].sum() *  add_ele * (1-target/100)/ expand_group['supply'].sum()
                add_pm = expand_group_pm['smokedustemit'].sum() *  add_ele_pm * (1-target/100)/ expand_group_pm['supply'].sum()
                
                
                potential_so2 = (add_so2 - minus_so2)/total_so2
                potential_co2 = (add_co2 - minus_co2)/total_co2
                potential_nox = (add_nox - minus_nox )/total_nox
                potential_pm = (add_pm - minus_pm )/total_pm
                     
                l_so2.append(potential_so2*100)
                l_nox.append(potential_nox*100)
                l_pm.append(potential_pm*100)        
                l_co2.append(potential_co2*100) 
                
            ax1.plot(X,l_so2,color=ind_color[ind],linestyle = '-',
                     marker=ind_marker[ind])
    
            ax2.plot(X,l_nox,color=ind_color[ind],linestyle = '-',
                     marker=ind_marker[ind])
            ax3.plot(X,l_pm,color=ind_color[ind],linestyle = '-',
                     marker=ind_marker[ind])  
            if ind == 22:
                l1, = ax4.plot(X,l_co2,color=ind_color[ind],linestyle = '-',
                          marker=ind_marker[ind])
            if ind == 25:
                l2, = ax4.plot(X,l_co2,color=ind_color[ind],linestyle = '-',
                          marker=ind_marker[ind])
            if ind == 26:
                l3, = ax4.plot(X,l_co2,color=ind_color[ind],linestyle = '-',
                          marker=ind_marker[ind])
            if ind == 30:
                l4, = ax4.plot(X,l_co2,color=ind_color[ind],linestyle = '-',
                          marker=ind_marker[ind])
            if ind == 31:
                l5, = ax4.plot(X,l_co2,color=ind_color[ind],linestyle = '-',
                          marker=ind_marker[ind])
            if ind == 32:
                l6, = ax4.plot(X,l_co2,color=ind_color[ind],linestyle = '-',
                          marker=ind_marker[ind])
            
            ax1.set_xticks([5,10,15,20,25,30])
            ax2.set_xticks([5,10,15,20,25,30]) 
            ax3.set_xticks([5,10,15,20,25,30]) 
    
                    
            ax4.set_xticks([5,10,15,20,25,30]) 
            
            ax1.axhline(y=0,ls="--",c="gray",alpha=0.3)
            ax2.axhline(y=0,ls="--",c="gray",alpha=0.3)
            ax3.axhline(y=0,ls="--",c="gray",alpha=0.3)
            ax4.axhline(y=0,ls="--",c="gray",alpha=0.3)
            
            record1[str(ind)] = l_so2
            record2[str(ind)] = l_nox
            record3[str(ind)] = l_pm        
            record4[str(ind)] = l_co2      
      
            if target == 30:
                ax1.set_ylim([-41,10])
                ax2.set_ylim([-150,150])
                ax3.set_ylim([-41,10])
                ax4.set_ylim([-20,20])        
                ax1.set_yticks([-40,-30,-20,-10,0,10])
                ax2.set_yticks([-150,-75,0,75,150]) 
                ax3.set_yticks([-40,-30,-20,-10,0,10]) 
                ax4.set_yticks([-20,-10,0,10,20])    
                if itr ==1: 
                    ax1.text(-3,10,mark[1] , fontdict={'size': '32', 'color': 'black','weight':'bold'}) 
                    ax2.text(-3,150,mark[2] , fontdict={'size': '32', 'color': 'black','weight':'bold'}) 
                    ax3.text(-3,10,mark[3] , fontdict={'size': '32', 'color': 'black','weight':'bold'}) 
                    ax4.text(-3,20,mark[4] , fontdict={'size': '32', 'color': 'black','weight':'bold'}) 
            if target == 50:
                ax1.set_ylim([-41,10])
                ax2.set_ylim([-50,50])
                ax3.set_ylim([-41,10])
                ax4.set_ylim([-4,4])        
                ax1.set_yticks([-40,-30,-20,-10,0,10])
                ax2.set_yticks([-50,-25,0,25,50]) 
                ax3.set_yticks([-40,-30,-20,-10,0,10]) 
                ax4.set_yticks([-4,-2,0,2,4])   
                if itr ==1: 
                    ax1.text(-3,10,mark[1] , fontdict={'size': '32', 'color': 'black','weight':'bold'}) 
                    ax2.text(-3,50,mark[2] , fontdict={'size': '32', 'color': 'black','weight':'bold'}) 
                    ax3.text(-3,10,mark[3] , fontdict={'size': '32', 'color': 'black','weight':'bold'}) 
                    ax4.text(-3,4,mark[4] , fontdict={'size': '32', 'color': 'black','weight':'bold'}) 
            if target == 70:
            
                ax1.set_ylim([-41,10])
                ax2.set_ylim([-41,10])
                ax3.set_ylim([-41,10])
                ax4.set_ylim([-41,10])        
                ax1.set_yticks([-40,-30,-20,-10,0,10])
                ax2.set_yticks([-40,-30,-20,-10,0,10]) 
                ax3.set_yticks([-40,-30,-20,-10,0,10]) 
                ax4.set_yticks([-40,-30,-20,-10,0,10])   
                if itr ==1: 
                    ax1.text(-3,10,mark[1] , fontdict={'size': '32', 'color': 'black','weight':'bold'}) 
                    ax2.text(-3,10,mark[2] , fontdict={'size': '32', 'color': 'black','weight':'bold'}) 
                    ax3.text(-3,10,mark[3] , fontdict={'size': '32', 'color': 'black','weight':'bold'}) 
                    ax4.text(-3,10,mark[4] , fontdict={'size': '32', 'color': 'black','weight':'bold'}) 
                
            ax1.set_ylabel('SO2 (%)',fontsize=24)
            ax2.set_ylabel('NOx (%)',fontsize=24)
            ax3.set_ylabel('PM (%)',fontsize=24)
            ax4.set_ylabel('CO2 (%)',fontsize=24)
            ax1.set_title(region_map[region])

            
            record1.to_excel(r'.\final-result\indirect-electrification\so2_%s_%s.xlsx'% (target,region),index=None)
            record2.to_excel(r'.\final-result\indirect-electrification\nox_%s_%s.xlsx'%(target,region),index=None)
            record3.to_excel(r'.\final-result\indirect-electrification\pm_%s_%s.xlsx'%(target,region),index=None)
            record4.to_excel(r'.\final-result\indirect-electrification\co2_%s_%s.xlsx'%(target,region),index=None)
        
            
            fig.subplots_adjust(hspace=0.4, wspace=0.4)   



    plt.legend((l1,l2,l3,l4,l5,l6),('Paper',"Petroleum",'Chemical','Non-metallic','Ferrous','Non-ferrous',),loc='lower left',frameon=False, 
              bbox_to_anchor=(-3.9,-1.03),ncol=6,columnspacing=1,fontsize=24)
    if target == 30:
        plt.text(-55,-38,'Assumed Percentage (%)',fontsize=24)
    if target == 50:
        plt.text(-55,-7,'Assumed Percentage (%)',fontsize=24)
    if target == 70:
        plt.text(-55,-64,'Assumed Percentage (%)',fontsize=24)

    fig.savefig(r'.\final-result\indirect-electrification\indirect-elect-3pol-%s.png'%target,
                dpi=300,bbox_inches="tight")

frame = pd.read_excel(r'.\data\dataset20201029.xlsx',sheet_name='power')

condition =(frame['coal_gross']>0)  & (frame['generation']>0) 
df = frame[condition]   
temp0 = df.copy()

frame = pd.read_excel(r'.\data\dataset20201029.xlsx',sheet_name='non-power')
condition = (frame['totalproduct_modify']>0) &  (frame['fossil']>0) 
df = frame[condition]   
df['ind2code'] = (df['industry_code']/100).astype(int)
ind2_list = list(set(df['ind2code']))
ind2_list.sort()
temp = df.copy()

indirect_electrification(temp,temp0,30)
indirect_electrification(temp,temp0,50)
indirect_electrification(temp,temp0,70)