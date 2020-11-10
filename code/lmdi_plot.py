# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 21:57:01 2020

@author: thund
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt  
from scipy import stats, integrate
import seaborn as sns
from matplotlib import font_manager as fm, rcParams
from PIL import Image
import matplotlib.patches as mpatches
import matplotlib.lines as mlines

def pinjie(workspace,file1,file2,filename):
    Image.MAX_IMAGE_PIXELS = None
    f1 = Image.open(workspace + file1)
    f2 = Image.open(workspace + file2)
    adj = f1.size[0]/f2.size[0]
    s1 = f1.size[0]
    s2 = int(adj * f2.size[1])
    f2_new = f2.resize((s1, s2),Image.ANTIALIAS)
    result = Image.new('RGBA', (f1.size[0], f1.size[1]+f2_new.size[1]),255)
    result.paste(f1, (0, 0))
    result.paste(f2_new, (0, f1.size[1]))
    result.save(workspace + filename)
    
#change your workspace
os.chdir(r'C:\Users\18110\Desktop\NS')
#fig for lmdi will be saved to the following inventory
workspace = r'./final-result/lmdi/pic/'

sort = {'Eastern':1,
        'Central':2,
        'Western':3,
        'National':4}
title = {'EOP':'End-of-pipe Treatment',
         'EF':'Unabated Emission Factor',
         'ES':'Energy Structure',
         'EI':'Energy Intensity',
         'TP':'Total Product'}
title_ele = {'EOP':'End-of-pipe Treatment',
         'EF':'Unabated Emission Factor',
         'EI':'Energy Intensity',
         'TP':'Generation Activity'}
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
region_map = {'EASTERN':'Eastern',
              'CENTRAL':'Central',
              'WESTERN':'Western',
              'NATIONAL':'National'}
mark = {1:'a',2:'b',3:'c',4:'d',5:'e',
        6:'f',7:'g',8:'h',9:'i',10:'j',}
mark_ele = {1:'f',2:'g',3:'h',4:'i'}
scatter_size = 120
a = 0.7

# # lmdi plot for PM (2011 and 2013)
# =============================================================================
result = pd.read_excel(r'.\final-result\lmdi\2year-pm.xlsx')
result['region'] = result['region'].map(region_map)
for item in ['EOP','EF','ES','EI','TP']:
    temp = result[['ind','region',item]]
    temp['type'] = item
    temp.rename(columns={item:'Index'},inplace=True)
    if item == 'EOP':
        merge = temp
    else:
        merge = merge.append(temp) 
merge['type'] =merge['type'].map(title)
merge['type1'] = merge['region'] + merge['type'] 

plt.rcParams.update({'font.size': 18})
fig1 = plt.figure(figsize=(25,4), frameon = False, dpi=300)
plt.rc('font',family='arial') 
itr = 0
for type in list(title.values()):
    itr = itr+1
    ax0 = fig1.add_subplot(1,5,itr)
    for ind in [22,25,26,30,31,32]:
        data_plot = merge[(merge['ind']==ind)&(merge['type']==type)]
        if ind == 22:
            l1 = ax0.scatter(x='region',y = 'Index',data=data_plot,color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)
        if ind == 25:
            l2 = ax0.scatter(x='region',y = 'Index',data=data_plot,
                              color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)          
        if ind == 26:
            l3 = ax0.scatter(x='region',y = 'Index',data=data_plot,
                              color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)
        if ind == 30:
            l4 = ax0.scatter(x='region',y = 'Index',data=data_plot,
                              color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)     
        if ind == 31:
            l5 = ax0.scatter(x='region',y = 'Index',data=data_plot,
                              color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)
        if ind == 32:
            l6 = ax0.scatter(x='region',y = 'Index',data=data_plot,
                              color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)   
    ax0.axhline(y=1,ls="--",c="gray",alpha=0.3)
    ax0.set_title(type,fontsize=20)
    if itr ==1:
        ax0.set_yticks([0,0.5,1.0,1.5,2.0,])
    else:
        ax0.set_yticks([0,0.5,1.0,1.5,2.0,])
        ax0.set_yticklabels([0,0.5,1.0,1.5,2.0,], fontsize=0)        
    ax0.set_ylim([0,2.2])
    ax0.set_ylabel('')
    ax0.set_xlabel('')
    if itr ==1:
        ax0.set_ylabel('Non-power Sectors',fontsize=20)
    ax0.text(-0.5,2.3,mark[itr] , fontdict={'size': '28', 'color': 'black','weight':'bold'})
fig1.subplots_adjust(hspace=0.2, wspace=0.15)
fig1.savefig(r'.\final-result\lmdi\pic\temp\pm_2year_non_power.png',bbox_inches="tight")


result = pd.read_excel(r'.\final-result\lmdi\power-2year-pm.xlsx')
result['region'] = result['region'].map(region_map)
result.rename(columns = title_ele,inplace=True)
result['region_sort'] = result['region'].map(sort)
result = result.sort_values(by="region_sort" , ascending=True)
plt.rcParams.update({'font.size': 18})
fig2 = plt.figure(figsize=(25,4), frameon = False, dpi=300)
plt.rc('font',family='arial') 
itr = 0
for type in list(title_ele.values()):
    itr = itr+1
    ax0 = fig2.add_subplot(1,4,itr)
    data_plot = result.copy()    

    l7 = ax0.scatter(result['region'],result[type],color='gray',s=scatter_size)
    ax0.axhline(y=1,ls="--",c="gray",alpha=0.3)
    if itr ==1:   
        ax0.set_yticks([0.5,1.0,1.5,2.0,2.5])
    else:
        ax0.set_yticks([0.5,1.0,1.5,2.0,2.5])
        ax0.set_yticklabels([0.5,1.0,1.5,2.0,2.5], fontsize=0)  
        
    ax0.set_ylim([0.6,2.5])
    ax0.set_title(type,fontsize=20)
    ax0.set_ylabel('')
    if itr ==1:
        ax0.set_ylabel('Coal-fired Power Plants',fontsize=20)
    ax0.text(-0.5,2.65,mark_ele[itr] , fontdict={'size': '28', 'color': 'black','weight':'bold'})
    ax0.set_xlabel('')
fig2.subplots_adjust(hspace=0.2, wspace=0.15)

plt.legend((l1,l2,l3,l4,l5,l6,l7),
           ('Paper',"Petroleum",'Chemical','Non-metallic','Ferrous','Non-ferrous','Coal-fired Power Plants'),
           ncol=4,loc='lower left', 
            bbox_to_anchor=(-3.6,-0.5),fancybox=False, shadow=False,frameon=False)
plt.savefig(r'.\final-result\lmdi\pic\temp\pm_2year_power.png',bbox_inches="tight")
file1 = "temp/pm_2year_non_power.png"
file2 = "temp/pm_2year_power.png"
pinjie(workspace,file1,file2,'2year_pm.png')



# # lmdi plot for SO2 (2011 and 2014)
# =============================================================================
result = pd.read_excel(r'.\final-result\lmdi\2year-so2.xlsx')
result['region'] = result['region'].map(region_map)
for item in ['EOP','EF','ES','EI','TP']:
    temp = result[['ind','region',item]]
    temp['type'] = item
    temp.rename(columns={item:'Index'},inplace=True)
    if item == 'EOP':
        merge = temp
    else:
        merge = merge.append(temp)
merge['type'] =merge['type'].map(title)
merge['type1'] = merge['region'] + merge['type'] 

plt.rcParams.update({'font.size': 18})
fig1 = plt.figure(figsize=(25,4), frameon = False, dpi=300)
plt.rc('font',family='arial') 
itr = 0
for type in list(title.values()):
    itr = itr+1
    ax0 = fig1.add_subplot(1,5,itr)
    for ind in [22,25,26,30,31,32]:
        data_plot = merge[(merge['ind']==ind)&(merge['type']==type)]
        if ind == 22:
            l1 = ax0.scatter(x='region',y = 'Index',data=data_plot,color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)
        if ind == 25:
            l2 = ax0.scatter(x='region',y = 'Index',data=data_plot,
                              color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)          
        if ind == 26:
            l3 = ax0.scatter(x='region',y = 'Index',data=data_plot,
                              color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)
        if ind == 30:
            l4 = ax0.scatter(x='region',y = 'Index',data=data_plot,
                              color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)     
        if ind == 31:
            l5 = ax0.scatter(x='region',y = 'Index',data=data_plot,
                              color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)
        if ind == 32:
            l6 = ax0.scatter(x='region',y = 'Index',data=data_plot,
                              color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)          
    ax0.axhline(y=1,ls="--",c="gray",alpha=0.3)
    ax0.set_title(type,fontsize=20)
    if itr ==1:
        ax0.set_yticks([0.3,1.0,1.7,2.4])
    else:
        ax0.set_yticks([0.3,1.0,1.7,2.4])
        ax0.set_yticklabels([0.3,1.0,1.7,2.4], fontsize=0)
    ax0.set_ylim([0,2.5])
    ax0.set_ylabel('')

    if itr ==1:
        ax0.set_ylabel('Non-power Sectors',fontsize=20)
    ax0.text(-0.5,2.6,mark[itr] , fontdict={'size': '28', 'color': 'black','weight':'bold'})

fig1.savefig(r'.\final-result\lmdi\pic\temp\so2_2year_non_power.png',dpi=300,bbox_inches="tight")

result = pd.read_excel(r'.\final-result\lmdi\power-2year-so2.xlsx')
result['region'] = result['region'].map(region_map)
result.rename(columns = title_ele,inplace=True)
result['region_sort'] = result['region'].map(sort)
result = result.sort_values(by="region_sort" , ascending=True)
plt.rcParams.update({'font.size': 18})
fig2 = plt.figure(figsize=(25,4), frameon = False, dpi=300)
plt.rc('font',family='arial') 
itr = 0
for type in list(title_ele.values()):
    itr = itr+1
    ax0 = fig2.add_subplot(1,4,itr)
    data_plot = result.copy()    
    l7 = ax0.scatter(result['region'],result[type],color='gray',s=scatter_size,)
    
    ax0.axhline(y=1,ls="--",c="gray",alpha=0.3)
    if itr ==1:
        ax0.set_yticks([0.4,0.7,1.0,1.3])
    else:
        ax0.set_yticks([0.4,0.7,1.0,1.3])
        ax0.set_yticklabels([0.4,0.7,1.0,1.3], fontsize=0)
    ax0.set_ylim([0.5,1.5])
    ax0.set_title(type,fontsize=20)
    ax0.set_ylabel('')
    if itr ==1:
        ax0.set_ylabel('Coal-fired Power Plants',fontsize=20)
    ax0.text(-0.5,1.53,mark_ele[itr] , fontdict={'size': '28', 'color': 'black','weight':'bold'})
fig2.subplots_adjust(hspace=0.2, wspace=0.15)

plt.legend((l1,l2,l3,l4,l5,l6,l7),
           ('Paper',"Petroleum",'Chemical','Non-metallic','Ferrous','Non-ferrous','Coal-fired Power Plants'),
           ncol=4,loc='lower left', 
            bbox_to_anchor=(-3.6,-0.5),fancybox=False, shadow=False,frameon=False)

plt.savefig(r'.\final-result\lmdi\pic\temp\so2_2year_power.png',dpi=300,bbox_inches="tight")
file1 = "temp/so2_2year_non_power.png"
file2 = "temp/so2_2year_power.png"
pinjie(workspace,file1,file2,'2year_so2.png')


# # lmdi plot for NOX (2011 and 2014)
# =============================================================================
result = pd.read_excel(r'.\final-result\lmdi\2year-nox.xlsx')
result['region'] = result['region'].map(region_map)
for item in ['EOP','EF','ES','EI','TP']:
    temp = result[['ind','region',item]]
    temp['type'] = item
    temp.rename(columns={item:'Index'},inplace=True)
    if item == 'EOP':
        merge = temp
    else:
        merge = merge.append(temp)
merge['type'] =merge['type'].map(title)    
merge['type1'] = merge['region'] + merge['type'] 

plt.rcParams.update({'font.size': 18})
fig1 = plt.figure(figsize=(25,4), frameon = False, dpi=300)
plt.rc('font',family='arial') 
itr = 0
for type in list(title.values()):
    itr = itr+1
    ax0 = fig1.add_subplot(1,5,itr)
    for ind in [22,25,26,30,31,32]:
        data_plot = merge[(merge['ind']==ind)&(merge['type']==type)]
        if ind == 22:
            l1 = ax0.scatter(x='region',y = 'Index',data=data_plot,color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)
        if ind == 25:
            l2 = ax0.scatter(x='region',y = 'Index',data=data_plot,
                              color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)          
        if ind == 26:
            l3 = ax0.scatter(x='region',y = 'Index',data=data_plot,
                              color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)
        if ind == 30:
            l4 = ax0.scatter(x='region',y = 'Index',data=data_plot,
                              color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)     
        if ind == 31:
            l5 = ax0.scatter(x='region',y = 'Index',data=data_plot,
                              color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)
        if ind == 32:
            l6 = ax0.scatter(x='region',y = 'Index',data=data_plot,
                              color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)   
    ax0.axhline(y=1,ls="--",c="gray",alpha=0.3)
    ax0.set_title(type,fontsize=20)
    if itr ==1:
        ax0.set_yticks([0,0.5,1.0,1.5,2.0,])
    else:
        ax0.set_yticks([0,0.5,1.0,1.5,2.0,])
        ax0.set_yticklabels([0,0.5,1.0,1.5,2.0,], fontsize=0)
    ax0.set_ylim([0,2.1])
    ax0.set_ylabel('')
    if itr ==1:
        ax0.set_ylabel('Non-power Sectors',fontsize=20)
    ax0.text(-0.5,2.2,mark[itr] , fontdict={'size': '28', 'color': 'black','weight':'bold'})
fig1.savefig(r'.\final-result\lmdi\pic\temp\nox_2year_non_power.png',dpi=300,bbox_inches="tight")

result = pd.read_excel(r'.\final-result\lmdi\power-2year-nox.xlsx')
result['region'] = result['region'].map(region_map)
result.rename(columns = title_ele,inplace=True)
result['region_sort'] = result['region'].map(sort)
result = result.sort_values(by="region_sort" , ascending=True)
plt.rcParams.update({'font.size': 18})
fig2 = plt.figure(figsize=(25,4), frameon = False, dpi=300)
plt.rc('font',family='arial') 
itr = 0
for type in list(title_ele.values()):
    itr = itr+1
    ax0 = fig2.add_subplot(1,4,itr)
    data_plot = result.copy()    
    l7 = ax0.scatter(result['region'],result[type],color='gray',s=scatter_size,)
    ax0.axhline(y=1,ls="--",c="gray",alpha=0.3)
    if itr ==1:
        ax0.set_yticks([0.4,0.7,1.0,1.3])
    else:
        ax0.set_yticks([0.4,0.7,1.0,1.3])
        ax0.set_yticklabels([0.4,0.7,1.0,1.3], fontsize=0)
    ax0.set_ylim([0.5,1.5])
    ax0.set_title(type,fontsize=20)
    ax0.set_ylabel('')
    if itr ==1:
        ax0.set_ylabel('Coal-fired Power Plants',fontsize=20)
    ax0.text(-0.5,1.53,mark_ele[itr] , fontdict={'size': '28', 'color': 'black','weight':'bold'})
fig2.subplots_adjust(hspace=0.2, wspace=0.15)

plt.legend((l1,l2,l3,l4,l5,l6,l7),
           ('Paper',"Petroleum",'Chemical','Non-metallic','Ferrous','Non-ferrous','Coal-fired Power Plants'),
           ncol=4,loc='lower left', 
            bbox_to_anchor=(-3.6,-0.5),fancybox=False, shadow=False,frameon=False)
plt.savefig(r'.\final-result\lmdi\pic\temp\nox_2year_power.png',dpi=300,bbox_inches="tight")

file1 = "temp/nox_2year_non_power.png"
file2 = "temp/nox_2year_power.png"
pinjie(workspace,file1,file2,'2year_nox.png')



# lmdi plot for so2 dynamic (2011-2014)
# =============================================================================
result = pd.read_excel(r'.\final-result\lmdi\dynamic-so2.xlsx')
result = result[result['region']=='NATIONAL']
result1 = pd.read_excel(r'.\final-result\lmdi\power-dynamic-so2.xlsx')
result1 = result1[result1['region']=='NATIONAL']

plt.rcParams.update({'font.size': 18})
fig1 = plt.figure(figsize=(25,4), frameon = False, dpi=300)
plt.rc('font',family='arial') 
itr = 1
for item in ['EOP','EF','ES','EI','TP']:
    ax0 = fig1.add_subplot(1,5,itr)
    for ind in [22,25,26,30,31,32]:
        data_plot = result[result['ind']==ind]
        if ind == 22:
            l1 = ax0.scatter(x='year',y = item,data=data_plot,color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)
        if ind == 25:
            l2 = ax0.scatter(x='year',y = item,data=data_plot,
                              color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)          
        if ind == 26:
            l3 = ax0.scatter(x='year',y = item,data=data_plot,
                              color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)
        if ind == 30:
            l4 = ax0.scatter(x='year',y = item,data=data_plot,
                              color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)     
        if ind == 31:
            l5 = ax0.scatter(x='year',y = item,data=data_plot,
                              color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)
        if ind == 32:
            l6 = ax0.scatter(x='year',y = item ,data=data_plot,
                              color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)   
    ax0.axhline(y=1,ls="--",c="gray",alpha=0.3)
    ax0.set_title(title[item],fontsize=20)
    ax0.set_xticks([2012,2013,2014])
    ax0.set_ylim([0,2])
    if itr ==1:
        ax0.set_yticks([0.2,0.6,1.0,1.4,1.8])
    else:
        ax0.set_yticks([0.2,0.6,1.0,1.4,1.8])
        ax0.set_yticklabels([0.2,0.6,1.0,1.4,1.8], fontsize=0)
    ax0.text(2011.7,2.1,mark[itr] , fontdict={'size': '28', 'color': 'black','weight':'bold'})
    if itr == 1:      
        ax0.set_ylabel('Non-power Sectors',fontsize=20)
    itr = itr + 1
fig1.savefig(r'.\final-result\lmdi\pic\temp\so2_dynamic_non_power.png',dpi=300,bbox_inches="tight")


plt.rcParams.update({'font.size': 18})
fig2 = plt.figure(figsize=(25,4), frameon = False, dpi=300)
plt.rc('font',family='arial') 
itr = 1
for item in list(title_ele.keys()):
    ax1 = fig2.add_subplot(1,4,itr)
    data_plot = result1[result1['year']>2011]
    l7 = ax1.scatter(x='year',y = item,data=data_plot,color='gray',s=scatter_size)
          
    ax1.set_title(title_ele[item],fontsize=20)
    ax1.set_xticks([2012,2013,2014])
    ax1.axhline(y=1,ls="--",c="gray",alpha=0.3)
    ax1.set_ylim([0.6,1.1])
    if itr ==1:
        ax1.set_yticks([0.7,0.8,0.9,1.0,])
    else:
        ax1.set_yticks([0.7,0.8,0.9,1.0,])
        ax1.set_yticklabels([0.7,0.8,0.9,1.0,], fontsize=0)
    ax1.text(2011.7,1.11,mark_ele[itr] , fontdict={'size': '28', 'color': 'black','weight':'bold'})
    if itr ==1:
        ax1.set_ylabel('Coal-fired Power Plants',fontsize=20)
    itr = itr + 1

plt.legend((l1,l2,l3,l4,l5,l6,l7),
           ('Paper',"Petroleum",'Chemical','Non-metallic','Ferrous','Non-ferrous','Coal-fired Power Plants'),
           ncol=4,loc='lower left', 
            bbox_to_anchor=(-3.6,-0.5),fancybox=False, shadow=False,frameon=False)

fig2.savefig(r'.\final-result\lmdi\pic\temp\so2_dynamic_power.png',dpi=300,bbox_inches="tight")

file1 = "temp/so2_dynamic_non_power.png"
file2 = "temp/so2_dynamic_power.png"
pinjie(workspace,file1,file2,'dynamic_so2.png')


# lmdi plot for nox dynamic (2011-2014)
# =============================================================================

result = pd.read_excel(r'.\final-result\lmdi\dynamic-nox.xlsx')
result = result[result['region']=='NATIONAL']
result1 = pd.read_excel(r'.\final-result\lmdi\power-dynamic-nox.xlsx')
result1 = result1[result1['region']=='NATIONAL']
plt.rcParams.update({'font.size': 18})
fig1 = plt.figure(figsize=(25,4), frameon = False, dpi=300)
plt.rc('font',family='arial') 
itr = 1
for item in ['EOP','EF','ES','EI','TP']:
    ax0 = fig1.add_subplot(1,5,itr)
    for ind in [22,25,26,30,31,32]:
        data_plot = result[result['ind']==ind]
        if ind == 22:
            l1 = ax0.scatter(x='year',y = item,data=data_plot,color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)
        if ind == 25:
            l2 = ax0.scatter(x='year',y = item,data=data_plot,
                              color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)          
        if ind == 26:
            l3 = ax0.scatter(x='year',y = item,data=data_plot,
                              color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)
        if ind == 30:
            l4 = ax0.scatter(x='year',y = item,data=data_plot,
                              color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)     
        if ind == 31:
            l5 = ax0.scatter(x='year',y = item,data=data_plot,
                              color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)
        if ind == 32:
            l6 = ax0.scatter(x='year',y = item ,data=data_plot,
                              color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)   

    ax0.axhline(y=1,ls="--",c="gray",alpha=0.3)
    ax0.set_title(title[item],fontsize=20)
    ax0.set_xticks([2012,2013,2014])
    ax0.set_ylim([0,2])
    if itr ==1:
        ax0.set_yticks([0.2,0.6,1.0,1.4,1.8])
    else:
        ax0.set_yticks([0.2,0.6,1.0,1.4,1.8])
        ax0.set_yticklabels([0.2,0.6,1.0,1.4,1.8], fontsize=0)
    ax0.text(2011.7,2.1,mark[itr] , fontdict={'size': '28', 'color': 'black','weight':'bold'})
    if itr == 1:      
        ax0.set_ylabel('Non-power Sectors',fontsize=20)
    itr = itr + 1
fig1.savefig(r'.\final-result\lmdi\pic\temp\nox_dynamic_non_power.png',dpi=300,bbox_inches="tight")

plt.rcParams.update({'font.size': 18})
fig2 = plt.figure(figsize=(25,4), frameon = False, dpi=300)
plt.rc('font',family='arial') 
itr = 1
for item in list(title_ele.keys()):
    ax1 = fig2.add_subplot(1,4,itr)
    
    data_plot = result1[result1['year']>2011]
    l7 = ax1.scatter(x='year',y = item,data=data_plot,color='gray',s=scatter_size)
          
    ax1.set_title(title_ele[item],fontsize=20)
    ax1.set_xticks([2012,2013,2014])
    ax1.axhline(y=1,ls="--",c="gray",alpha=0.3)
    ax1.set_ylim([0.6,1.1])
    if itr ==1:
        ax1.set_yticks([0.7,0.8,0.9,1.0,])
    else:
        ax1.set_yticks([0.7,0.8,0.9,1.0,])
        ax1.set_yticklabels([0.7,0.8,0.9,1.0,], fontsize=0)
    ax1.text(2011.7,1.11,mark_ele[itr] , fontdict={'size': '28', 'color': 'black','weight':'bold'})
    if itr ==1:
        ax1.set_ylabel('Coal-fired Power Plants',fontsize=20)
    itr = itr + 1

plt.legend((l1,l2,l3,l4,l5,l6,l7),
           ('Paper',"Petroleum",'Chemical','Non-metallic','Ferrous','Non-ferrous','Coal-fired Power Plants'),
           ncol=4,loc='lower left', 
            bbox_to_anchor=(-3.6,-0.5),fancybox=False, shadow=False,frameon=False)

fig2.savefig(r'.\final-result\lmdi\pic\temp\nox_dynamic_power.png',dpi=300,bbox_inches="tight")

file1 = "temp/nox_dynamic_non_power.png"
file2 = "temp/nox_dynamic_power.png"
pinjie(workspace,file1,file2,'dynamic_nox.png')


# lmdi plot for pm dynamic (2011-2013)
# =============================================================================

result = pd.read_excel(r'.\final-result\lmdi\dynamic-pm.xlsx')
result = result[result['region']=='NATIONAL']
result1 = pd.read_excel(r'.\final-result\lmdi\power-dynamic-pm.xlsx')
result1 = result1[result1['region']=='NATIONAL']

plt.rcParams.update({'font.size': 18})
fig1 = plt.figure(figsize=(25,4), frameon = False, dpi=300)
plt.rc('font',family='arial') 
itr = 1
for item in ['EOP','EF','ES','EI','TP']:
    ax0 = fig1.add_subplot(1,5,itr)
    for ind in [22,25,26,30,31,32]:
        data_plot = result[result['ind']==ind]
        if ind == 22:
            l1 = ax0.scatter(x='year',y = item,data=data_plot,color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)
        if ind == 25:
            l2 = ax0.scatter(x='year',y = item,data=data_plot,
                              color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)          
        if ind == 26:
            l3 = ax0.scatter(x='year',y = item,data=data_plot,
                              color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)
        if ind == 30:
            l4 = ax0.scatter(x='year',y = item,data=data_plot,
                              color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)     
        if ind == 31:
            l5 = ax0.scatter(x='year',y = item,data=data_plot,
                              color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)
        if ind == 32:
            l6 = ax0.scatter(x='year',y = item ,data=data_plot,
                              color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)   
    ax0.axhline(y=1,ls="--",c="gray",alpha=0.3)
    ax0.set_title(title[item],fontsize=20)
    ax0.set_xticks([2012,2013])
    ax0.set_ylim([0,2])
    if itr ==1:
        ax0.set_yticks([0.2,0.6,1.0,1.4,1.8])
    else:
        ax0.set_yticks([0.2,0.6,1.0,1.4,1.8])
        ax0.set_yticklabels([0.2,0.6,1.0,1.4,1.8], fontsize=0)
    ax0.text(2011.85,2.1,mark[itr] , fontdict={'size': '28', 'color': 'black','weight':'bold'})
    if itr == 1:      
        ax0.set_ylabel('Non-power Sectors',fontsize=20)
    itr = itr + 1
fig1.savefig(r'.\final-result\lmdi\pic\temp\pm_dynamic_non_power.png',dpi=300,bbox_inches="tight")

plt.rcParams.update({'font.size': 18})
fig2 = plt.figure(figsize=(25,4), frameon = False, dpi=300)
plt.rc('font',family='arial') 
itr = 1
for item in list(title_ele.keys()):
    ax1 = fig2.add_subplot(1,4,itr)
    data_plot = result1[result1['year']>2011]
    l7 = ax1.scatter(x='year',y = item,data=data_plot,color='gray',s=scatter_size)      
    ax1.set_title(title_ele[item],fontsize=20)
    ax1.set_xticks([2012,2013])
    ax1.axhline(y=1,ls="--",c="gray",alpha=0.3)
    ax1.set_ylim([0.8,1.3])
    if itr ==1:
        ax1.set_yticks([0.9,1.0,1.1,1.2])
    else:
        ax1.set_yticks([0.9,1.0,1.1,1.2])
        ax1.set_yticklabels([0.9,1.0,1.1,1.2], fontsize=0)
    ax1.text(2011.85,1.31,mark_ele[itr] , fontdict={'size': '28', 'color': 'black','weight':'bold'})
    if itr ==1:
        ax1.set_ylabel('Coal-fired Power Plants',fontsize=20)
    itr = itr + 1


plt.legend((l1,l2,l3,l4,l5,l6,l7),
           ('Paper',"Petroleum",'Chemical','Non-metallic','Ferrous','Non-ferrous','Coal-fired Power Plants'),
           ncol=4,loc='lower left', 
            bbox_to_anchor=(-3.6,-0.5),fancybox=False, shadow=False,frameon=False)

fig2.savefig(r'.\final-result\lmdi\pic\temp\pm_dynamic_power.png',dpi=300,bbox_inches="tight")
file1 = "temp/pm_dynamic_non_power.png"
file2 = "temp/pm_dynamic_power.png"
pinjie(workspace,file1,file2,'dynamic_pm.png')



# =============================================================================
# # # # lmdi for base2009
# =============================================================================




# lmdi plot for pm  (2009 and 2014)
# =============================================================================
result = pd.read_excel(r'.\final-result\lmdi\base2009-2year-pm.xlsx')
result['region'] = result['region'].map(region_map)

for item in ['EOP','EF','ES','EI','TP']:
    temp = result[['ind','region',item]]
    temp['type'] = item
    temp.rename(columns={item:'Index'},inplace=True)
    if item == 'EOP':
        merge = temp
    else:
        merge = merge.append(temp)
merge['type'] =merge['type'].map(title)
merge['type1'] = merge['region'] + merge['type'] 
plt.rcParams.update({'font.size': 18})
fig1 = plt.figure(figsize=(25,4), frameon = False, dpi=300)
plt.rc('font',family='arial') 
itr = 0
for type in list(title.values()):
    itr = itr+1
    ax0 = fig1.add_subplot(1,5,itr)
    for ind in [22,25,26,30,31,32]:
        data_plot = merge[(merge['ind']==ind)&(merge['type']==type)]
        if ind == 22:
            l1 = ax0.scatter(x='region',y = 'Index',data=data_plot,color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)
        if ind == 25:
            l2 = ax0.scatter(x='region',y = 'Index',data=data_plot,
                              color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)          
        if ind == 26:
            l3 = ax0.scatter(x='region',y = 'Index',data=data_plot,
                              color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)
        if ind == 30:
            l4 = ax0.scatter(x='region',y = 'Index',data=data_plot,
                              color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)     
        if ind == 31:
            l5 = ax0.scatter(x='region',y = 'Index',data=data_plot,
                              color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)
        if ind == 32:
            l6 = ax0.scatter(x='region',y = 'Index',data=data_plot,
                              color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)  
    ax0.axhline(y=1,ls="--",c="gray",alpha=0.3)
    ax0.set_title(type,fontsize=20)
    if itr ==1:
        ax0.set_yticks([0,0.5,1.0,1.5,2.0,])
    else:
        ax0.set_yticks([0,0.5,1.0,1.5,2.0,])
        ax0.set_yticklabels([0,0.5,1.0,1.5,2.0,], fontsize=0)
    ax0.set_ylim([0,2.2])
    ax0.set_ylabel('')
    if itr ==1:
        ax0.set_ylabel('Non-power Sectors',fontsize=20)
    ax0.text(-0.5,2.3,mark[itr] , fontdict={'size': '28', 'color': 'black','weight':'bold'})
fig1.savefig(r'.\final-result\lmdi\pic\temp\pm_2year_non_power.png',dpi=300,bbox_inches="tight")

result = pd.read_excel(r'.\final-result\lmdi\power-2year-pm.xlsx')
result['region'] = result['region'].map(region_map)
result.rename(columns = title_ele,inplace=True)
result['region_sort'] = result['region'].map(sort)
result = result.sort_values(by="region_sort" , ascending=True)
plt.rcParams.update({'font.size': 18})
fig2 = plt.figure(figsize=(25,4), frameon = False, dpi=300)
plt.rc('font',family='arial') 
itr = 0

for type in list(title_ele.values()):
    itr = itr+1
    ax0 = fig2.add_subplot(1,4,itr)
    data_plot = result.copy()    
    l7 = ax0.scatter(result['region'],result[type],color='gray',s=scatter_size,)
    ax0.axhline(y=1,ls="--",c="gray",alpha=0.3)
    if itr ==1:
        ax0.set_yticks([0.5,1.0,1.5,2.0,2.5])
    else:
        ax0.set_yticks([0.5,1.0,1.5,2.0,2.5])
        ax0.set_yticklabels([0.5,1.0,1.5,2.0,2.5], fontsize=0)
    ax0.set_ylim([0.6,2.5])
    ax0.set_title(type,fontsize=20)
    ax0.set_ylabel('')
    if itr ==1:
        ax0.set_ylabel('Coal-fired Power Plants',fontsize=20)

    ax0.text(-0.5,2.65,mark_ele[itr] , fontdict={'size': '28', 'color': 'black','weight':'bold'})

fig2.subplots_adjust(hspace=0.2, wspace=0.15)

plt.legend((l1,l2,l3,l4,l5,l6,l7),
           ('Paper',"Petroleum",'Chemical','Non-metallic','Ferrous','Non-ferrous','Coal-fired Power Plants'),
           ncol=4,loc='lower left', 
            bbox_to_anchor=(-3.6,-0.5),fancybox=False, shadow=False,frameon=False)
plt.savefig(r'.\final-result\lmdi\pic\temp\pm_2year_power.png',dpi=300,bbox_inches="tight")
file1 = "temp/pm_2year_non_power.png"
file2 = "temp/pm_2year_power.png"
pinjie(workspace,file1,file2,'base2009-2year-pm.png')


# lmdi plot for so2  (2009 and 2014)
# =============================================================================
result = pd.read_excel(r'.\final-result\lmdi\base2009-2year-so2.xlsx')
result['region'] = result['region'].map(region_map)
for item in ['EOP','EF','ES','EI','TP']:
    temp = result[['ind','region',item]]
    temp['type'] = item
    temp.rename(columns={item:'Index'},inplace=True)
    if item == 'EOP':
        merge = temp
    else:
        merge = merge.append(temp)
merge['type'] =merge['type'].map(title)
merge['type1'] = merge['region'] + merge['type'] 

plt.rcParams.update({'font.size': 18})
fig1 = plt.figure(figsize=(25,4), frameon = False, dpi=300)
plt.rc('font',family='arial') 

itr = 0
for type in list(title.values()):
    itr = itr+1
    ax0 = fig1.add_subplot(1,5,itr)
    for ind in [22,25,26,30,31,32]:
        data_plot = merge[(merge['ind']==ind)&(merge['type']==type)]
        if ind == 22:
            l1 = ax0.scatter(x='region',y = 'Index',data=data_plot,color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)
        if ind == 25:
            l2 = ax0.scatter(x='region',y = 'Index',data=data_plot,
                              color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)          
        if ind == 26:
            l3 = ax0.scatter(x='region',y = 'Index',data=data_plot,
                              color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)
        if ind == 30:
            l4 = ax0.scatter(x='region',y = 'Index',data=data_plot,
                              color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)     
        if ind == 31:
            l5 = ax0.scatter(x='region',y = 'Index',data=data_plot,
                              color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)
        if ind == 32:
            l6 = ax0.scatter(x='region',y = 'Index',data=data_plot,
                              color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)  
    ax0.axhline(y=1,ls="--",c="gray",alpha=0.3)
    ax0.set_title(type,fontsize=20)
    if itr ==1:
        ax0.set_yticks([0,0.5,1.0,1.5,2.0])
    else:
        ax0.set_yticks([0,0.5,1.0,1.5,2.0])
        ax0.set_yticklabels([0,0.5,1.0,1.5,2.0], fontsize=0)
    ax0.set_ylim([0,2.1])
    ax0.set_ylabel('')
    if itr ==1:
        ax0.set_ylabel('Non-power Sectors',fontsize=20)
    ax0.text(-0.5,2.2,mark[itr] , fontdict={'size': '28', 'color': 'black','weight':'bold'})

fig1.savefig(r'.\final-result\lmdi\pic\temp\so2_2year_non_power.png',dpi=300,bbox_inches="tight")

result = pd.read_excel(r'.\final-result\lmdi\power-2year-so2.xlsx')
result.rename(columns = title_ele,inplace=True)
result['region'] = result['region'].map(region_map)
result['region_sort'] = result['region'].map(sort)
result = result.sort_values(by="region_sort" , ascending=True)

plt.rcParams.update({'font.size': 18})
fig2 = plt.figure(figsize=(25,4), frameon = False, dpi=300)
plt.rc('font',family='arial') 
itr = 0
for type in list(title_ele.values()):
    itr = itr+1
    ax0 = fig2.add_subplot(1,4,itr)
    data_plot = result.copy()    
    l7 = ax0.scatter(result['region'],result[type],color='gray',s=scatter_size,)
    
    ax0.axhline(y=1,ls="--",c="gray",alpha=0.3)
    if itr ==1:
        ax0.set_yticks([0.4,0.7,1.0,1.3])
    else:
        ax0.set_yticks([0.4,0.7,1.0,1.3])
        ax0.set_yticklabels([0.4,0.7,1.0,1.3], fontsize=0)
    ax0.set_ylim([0.5,1.5])
    ax0.set_title(type,fontsize=20)
    ax0.set_ylabel('')
    if itr ==1:
        ax0.set_ylabel('Coal-fired Power Plants',fontsize=20)
    ax0.text(-0.5,1.53,mark_ele[itr] , fontdict={'size': '28', 'color': 'black','weight':'bold'})


fig2.subplots_adjust(hspace=0.2, wspace=0.15)

plt.legend((l1,l2,l3,l4,l5,l6,l7),
           ('Paper',"Petroleum",'Chemical','Non-metallic','Ferrous','Non-ferrous','Coal-fired Power Plants'),
           ncol=4,loc='lower left', 
            bbox_to_anchor=(-3.6,-0.5),fancybox=False, shadow=False,frameon=False)

plt.savefig(r'.\final-result\lmdi\pic\temp\so2_2year_power.png',dpi=300,bbox_inches="tight")
file1 = "temp/so2_2year_non_power.png"
file2 = "temp/so2_2year_power.png"
pinjie(workspace,file1,file2,'base2009-2year-so2.png')

# lmdi plot for nox  (2009 and 2014)
# =============================================================================
result = pd.read_excel(r'.\final-result\lmdi\base2009-2year-nox.xlsx')
result['region'] = result['region'].map(region_map)
for item in ['EOP','EF','ES','EI','TP']:
    temp = result[['ind','region',item]]
    temp['type'] = item
    temp.rename(columns={item:'Index'},inplace=True)
    if item == 'EOP':
        merge = temp
    else:
        merge = merge.append(temp)
merge['type'] =merge['type'].map(title)
merge['type1'] = merge['region'] + merge['type'] 

plt.rcParams.update({'font.size': 18})
fig1 = plt.figure(figsize=(25,4), frameon = False, dpi=300)
plt.rc('font',family='arial') 
itr = 0
for type in list(title.values()):
    itr = itr+1
    ax0 = fig1.add_subplot(1,5,itr)
    for ind in [22,25,26,30,31,32]:
        data_plot = merge[(merge['ind']==ind)&(merge['type']==type)]
        if ind == 22:
            l1 = ax0.scatter(x='region',y = 'Index',data=data_plot,color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)
        if ind == 25:
            l2 = ax0.scatter(x='region',y = 'Index',data=data_plot,
                              color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)          
        if ind == 26:
            l3 = ax0.scatter(x='region',y = 'Index',data=data_plot,
                              color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)
        if ind == 30:
            l4 = ax0.scatter(x='region',y = 'Index',data=data_plot,
                              color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)     
        if ind == 31:
            l5 = ax0.scatter(x='region',y = 'Index',data=data_plot,
                              color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)
        if ind == 32:
            l6 = ax0.scatter(x='region',y = 'Index',data=data_plot,
                              color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)  
    ax0.axhline(y=1,ls="--",c="gray",alpha=0.3)
    ax0.set_title(type,fontsize=20)
    if itr ==1:
        ax0.set_yticks([0,0.5,1.0,1.5,2.0,])
        
    else:
        ax0.set_yticks([0,0.5,1.0,1.5,2.0,])
        ax0.set_yticklabels([0,0.5,1.0,1.5,2.0,], fontsize=0)
    ax0.set_ylim([0,2.1])
    ax0.set_ylabel('')
    if itr ==1:
        ax0.set_ylabel('Non-power Sectors',fontsize=20)
    ax0.text(-0.5,2.2,mark[itr] , fontdict={'size': '28', 'color': 'black','weight':'bold'})
fig1.savefig(r'.\final-result\lmdi\pic\temp\nox_2year_non_power.png',dpi=300,bbox_inches="tight")

result = pd.read_excel(r'.\final-result\lmdi\power-2year-nox.xlsx')
result['region'] = result['region'].map(region_map)
result.rename(columns = title_ele,inplace=True)
result['region_sort'] = result['region'].map(sort)
result = result.sort_values(by="region_sort" , ascending=True)
plt.rcParams.update({'font.size': 18})
fig2 = plt.figure(figsize=(25,4), frameon = False, dpi=300)
plt.rc('font',family='arial') 
itr = 0

for type in list(title_ele.values()):
    itr = itr+1
    ax0 = fig2.add_subplot(1,4,itr)
    data_plot = result.copy()    
    l7 = ax0.scatter(result['region'],result[type],color='gray',s=scatter_size,)
    
    ax0.axhline(y=1,ls="--",c="gray",alpha=0.3)
    if itr ==1:
        ax0.set_yticks([0.4,0.7,1.0,1.3])
    else:
        ax0.set_yticks([0.4,0.7,1.0,1.3])
        ax0.set_yticklabels([0.4,0.7,1.0,1.3], fontsize=0)
    ax0.set_ylim([0.5,1.5])
    ax0.set_title(type,fontsize=20)
    ax0.set_ylabel('')
    if itr ==1:
        ax0.set_ylabel('Coal-fired Power Plants',fontsize=20)

    ax0.text(-0.5,1.53,mark_ele[itr] , fontdict={'size': '28', 'color': 'black','weight':'bold'})

fig2.subplots_adjust(hspace=0.2, wspace=0.15)

plt.legend((l1,l2,l3,l4,l5,l6,l7),
           ('Paper',"Petroleum",'Chemical','Non-metallic','Ferrous','Non-ferrous','Coal-fired Power Plants'),
           ncol=4,loc='lower left', 
            bbox_to_anchor=(-3.6,-0.5),fancybox=False, shadow=False,frameon=False)

plt.savefig(r'.\final-result\lmdi\pic\temp\nox_2year_power.png',dpi=300,bbox_inches="tight")
file1 = "temp/nox_2year_non_power.png"
file2 = "temp/nox_2year_power.png"
pinjie(workspace,file1,file2,'base2009-2year-nox.png')


# lmdi plot for so2 dynamic  (2009-2014)
# =============================================================================
result = pd.read_excel(r'.\final-result\lmdi\base2009-dynamic-so2.xlsx')
result = result[result['region']=='NATIONAL']

result1 = pd.read_excel(r'.\final-result\lmdi\power-dynamic-so2.xlsx')
result1 = result1[result1['region']=='NATIONAL']

plt.rcParams.update({'font.size': 18})
fig1 = plt.figure(figsize=(25,4), frameon = False, dpi=300)
plt.rc('font',family='arial') 
itr = 1
for item in ['EOP','EF','ES','EI','TP']:
    ax0 = fig1.add_subplot(1,5,itr)
    for ind in [22,25,26,30,31,32]:
        data_plot = result[result['ind']==ind]
        if ind == 22:
            l1 = ax0.scatter(x='year',y = item,data=data_plot,color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)
        if ind == 25:
            l2 = ax0.scatter(x='year',y = item,data=data_plot,
                              color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)          
        if ind == 26:
            l3 = ax0.scatter(x='year',y = item,data=data_plot,
                              color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)
        if ind == 30:
            l4 = ax0.scatter(x='year',y = item,data=data_plot,
                              color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)     
        if ind == 31:
            l5 = ax0.scatter(x='year',y = item,data=data_plot,
                              color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)
        if ind == 32:
            l6 = ax0.scatter(x='year',y = item ,data=data_plot,
                              color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)   
    ax0.axhline(y=1,ls="--",c="gray",alpha=0.3)
    ax0.set_title(title[item],fontsize=20)
    ax0.set_xticks([2010,2011,2012,2013,2014])
    ax0.set_ylim([0,2])
    if itr ==1:
        ax0.set_yticks([0.2,0.6,1.0,1.4,1.8])
    else:
        ax0.set_yticks([0.2,0.6,1.0,1.4,1.8])
        ax0.set_yticklabels([0.2,0.6,1.0,1.4,1.8], fontsize=0)
    ax0.text(2009,2.1,mark[itr] , fontdict={'size': '28', 'color': 'black','weight':'bold'})
    if itr == 1:      
        ax0.set_ylabel('Non-power Sectors',fontsize=20)
    itr = itr + 1
fig1.savefig(r'.\final-result\lmdi\pic\temp\so2_dynamic_non_power.png',dpi=300,bbox_inches="tight")

plt.rcParams.update({'font.size': 18})
fig2 = plt.figure(figsize=(25,4), frameon = False, dpi=300)
plt.rc('font',family='arial') 
itr = 1
for item in list(title_ele.keys()):
    print(itr)
    ax1 = fig2.add_subplot(1,4,itr)
    data_plot = result1[result1['year']>2011]
    l7 = ax1.scatter(x='year',y = item,data=data_plot,color='gray',s=scatter_size)
    ax1.set_title(title_ele[item],fontsize=20)
    ax1.set_xticks([2012,2013,2014])
    ax1.axhline(y=1,ls="--",c="gray",alpha=0.3)
    ax1.set_ylim([0.6,1.1])
    if itr ==1:
        ax1.set_yticks([0.7,0.8,0.9,1.0,])
    else:
        ax1.set_yticks([0.7,0.8,0.9,1.0,])
        ax1.set_yticklabels([0.7,0.8,0.9,1.0,], fontsize=0)
    ax1.text(2011.7,1.11,mark_ele[itr] , fontdict={'size': '28', 'color': 'black','weight':'bold'})
    if itr ==1:
        ax1.set_ylabel('Coal-fired Power Plants',fontsize=20)
    itr = itr + 1

plt.legend((l1,l2,l3,l4,l5,l6,l7),
           ('Paper',"Petroleum",'Chemical','Non-metallic','Ferrous','Non-ferrous','Coal-fired Power Plants'),
           ncol=4,loc='lower left', 
            bbox_to_anchor=(-3.6,-0.5),fancybox=False, shadow=False,frameon=False)

fig2.savefig(r'.\final-result\lmdi\pic\temp\so2_dynamic_power.png',dpi=300,bbox_inches="tight")
file1 = "temp/so2_dynamic_non_power.png"
file2 = "temp/so2_dynamic_power.png"
pinjie(workspace,file1,file2,'base2009-dynamic-so2.png')


# lmdi plot for nox dynamic  (2009-2014)
# =============================================================================
result = pd.read_excel(r'.\final-result\lmdi\base2009-dynamic-nox.xlsx')
result = result[result['region']=='NATIONAL']

result1 = pd.read_excel(r'.\final-result\lmdi\power-dynamic-nox.xlsx')
result1 = result1[result1['region']=='NATIONAL']

plt.rcParams.update({'font.size': 18})
fig1 = plt.figure(figsize=(25,4), frameon = False, dpi=300)
plt.rc('font',family='arial') 
itr = 1
for item in ['EOP','EF','ES','EI','TP']:
    ax0 = fig1.add_subplot(1,5,itr)
    for ind in [22,25,26,30,31,32]:
        data_plot = result[result['ind']==ind]
        if ind == 22:
            l1 = ax0.scatter(x='year',y = item,data=data_plot,color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)
        if ind == 25:
            l2 = ax0.scatter(x='year',y = item,data=data_plot,
                              color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)          
        if ind == 26:
            l3 = ax0.scatter(x='year',y = item,data=data_plot,
                              color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)
        if ind == 30:
            l4 = ax0.scatter(x='year',y = item,data=data_plot,
                              color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)     
        if ind == 31:
            l5 = ax0.scatter(x='year',y = item,data=data_plot,
                              color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)
        if ind == 32:
            l6 = ax0.scatter(x='year',y = item ,data=data_plot,
                              color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)  
    ax0.axhline(y=1,ls="--",c="gray",alpha=0.3)
    ax0.set_title(title[item],fontsize=20)
    ax0.set_xticks([2010,2011,2012,2013,2014])
    ax0.set_ylim([0,2])
    if itr ==1:
        ax0.set_yticks([0.2,0.6,1.0,1.4,1.8])
    else:
        ax0.set_yticks([0.2,0.6,1.0,1.4,1.8])
        ax0.set_yticklabels([0.2,0.6,1.0,1.4,1.8], fontsize=0)
    ax0.text(2009,2.1,mark[itr] , fontdict={'size': '28', 'color': 'black','weight':'bold'})
    if itr == 1:      
        ax0.set_ylabel('Non-power Sectors')
    itr = itr + 1
fig1.savefig(r'.\final-result\lmdi\pic\temp\nox_dynamic_non_power.png',dpi=300,bbox_inches="tight")

plt.rcParams.update({'font.size': 18})
fig2 = plt.figure(figsize=(25,4), frameon = False, dpi=300)
plt.rc('font',family='arial') 
itr = 1

for item in list(title_ele.keys()):
    print(itr)
    ax1 = fig2.add_subplot(1,4,itr)
    data_plot = result1[result1['year']>2011]
    l7 = ax1.scatter(x='year',y = item,data=data_plot,color='gray',s=scatter_size)    
    ax1.set_title(title_ele[item],fontsize=20)
    ax1.set_xticks([2012,2013,2014])
    ax1.axhline(y=1,ls="--",c="gray",alpha=0.3)
    ax1.set_ylim([0.6,1.1])
    if itr ==1:
        ax1.set_yticks([0.7,0.8,0.9,1.0,])
    else:
        ax1.set_yticks([0.7,0.8,0.9,1.0,])
        ax1.set_yticklabels([0.7,0.8,0.9,1.0,], fontsize=0)
    ax1.text(2011.7,1.11,mark_ele[itr] , fontdict={'size': '28', 'color': 'black','weight':'bold'})
    if itr ==1:
        ax1.set_ylabel('Coal-fired Power Plants')
    itr = itr + 1
plt.legend((l1,l2,l3,l4,l5,l6,l7),
           ('Paper',"Petroleum",'Chemical','Non-metallic','Ferrous','Non-ferrous','Coal-fired Power Plants'),
           ncol=4,loc='lower left', 
            bbox_to_anchor=(-3.6,-0.5),fancybox=False, shadow=False,frameon=False)
fig2.savefig(r'.\final-result\lmdi\pic\temp\nox_dynamic_power.png',dpi=300,bbox_inches="tight")
file1 = "temp/nox_dynamic_non_power.png"
file2 = "temp/nox_dynamic_power.png"
pinjie(workspace,file1,file2,'base2009-dynamic-nox.png')


# lmdi plot for pm dynamic  (2009-2013)
# =============================================================================
mark = {1:'a',2:'b',3:'c',4:'d',5:'e'}
result = pd.read_excel(r'.\final-result\lmdi\base2009-dynamic-pm.xlsx')
result = result[result['region']=='NATIONAL']
result1 = pd.read_excel(r'.\final-result\lmdi\power-dynamic-pm.xlsx')
result1 = result1[result1['region']=='NATIONAL']
plt.rcParams.update({'font.size': 18})
fig1 = plt.figure(figsize=(25,4), frameon = False, dpi=300)
plt.rc('font',family='arial') 
itr = 1
for item in ['EOP','EF','ES','EI','TP']:
    ax0 = fig1.add_subplot(1,5,itr)
    for ind in [22,25,26,30,31,32]:
        data_plot = result[result['ind']==ind]
        if ind == 22:
            l1 = ax0.scatter(x='year',y = item,data=data_plot,color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)
        if ind == 25:
            l2 = ax0.scatter(x='year',y = item,data=data_plot,
                              color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)          
        if ind == 26:
            l3 = ax0.scatter(x='year',y = item,data=data_plot,
                              color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)
        if ind == 30:
            l4 = ax0.scatter(x='year',y = item,data=data_plot,
                              color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)     
        if ind == 31:
            l5 = ax0.scatter(x='year',y = item,data=data_plot,
                              color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)
        if ind == 32:
            l6 = ax0.scatter(x='year',y = item ,data=data_plot,
                              color=ind_color[ind],s=scatter_size,marker=ind_marker[ind],alpha=a)  
    ax0.axhline(y=1,ls="--",c="gray",alpha=0.3)
    ax0.set_title(title[item],fontsize=20)
    ax0.set_xticks([2010,2011,2012,2013])
    ax0.set_ylim([0,2])
    if itr ==1:
        ax0.set_yticks([0.2,0.6,1.0,1.4,1.8])
    else:
        ax0.set_yticks([0.2,0.6,1.0,1.4,1.8])
        ax0.set_yticklabels([0.2,0.6,1.0,1.4,1.8], fontsize=0)
    ax0.text(2009.45,2.1,mark[itr] , fontdict={'size': '28', 'color': 'black','weight':'bold'})
    if itr == 1:      
        ax0.set_ylabel('Non-power Sectors')
    itr = itr + 1
fig1.savefig(r'.\final-result\lmdi\pic\temp\pm_dynamic_non_power.png',dpi=300,bbox_inches="tight")

plt.rcParams.update({'font.size': 18})
fig2 = plt.figure(figsize=(25,4), frameon = False, dpi=300)
plt.rc('font',family='arial') 
itr = 1
for item in list(title_ele.keys()):
    print(itr)
    ax1 = fig2.add_subplot(1,4,itr)
    
    data_plot = result1[result1['year']>2011]
    l7 = ax1.scatter(x='year',y = item,data=data_plot,color='gray',s=scatter_size)
          
    ax1.set_title(title_ele[item],fontsize=20)
    ax1.set_xticks([2012,2013])
    ax1.axhline(y=1,ls="--",c="gray",alpha=0.3)
    ax1.set_ylim([0.8,1.3])
    if itr ==1:
        ax1.set_yticks([0.9,1.0,1.1,1.2])
    else:
        ax1.set_yticks([0.9,1.0,1.1,1.2])
        ax1.set_yticklabels([0.9,1.0,1.1,1.2], fontsize=0)
    ax1.text(2011.85,1.31,mark_ele[itr] , fontdict={'size': '28', 'color': 'black','weight':'bold'})
    if itr ==1:
        ax1.set_ylabel('Coal-fired Power Plants')
    itr = itr + 1

plt.legend((l1,l2,l3,l4,l5,l6,l7),
           ('Paper',"Petroleum",'Chemical','Non-metallic','Ferrous','Non-ferrous','Coal-fired Power Plants'),
           ncol=4,loc='lower left', 
            bbox_to_anchor=(-3.6,-0.5),fancybox=False, shadow=False,frameon=False)
fig2.savefig(r'.\final-result\lmdi\pic\temp\pm_dynamic_power.png',dpi=300,bbox_inches="tight")
file1 = "temp/pm_dynamic_non_power.png"
file2 = "temp/pm_dynamic_power.png"
pinjie(workspace,file1,file2,'base2009-dynamic-pm.png')




###heatmap
for pol in ['so2','nox','pm']:
    result = pd.read_excel(r'.\final-result\lmdi\base2009-2year-%s.xlsx'%pol)
    result1 = pd.read_excel(r'.\final-result\lmdi\power-2year-%s.xlsx'%pol)
    ind_map = {22:'Paper',
                25:'Petroleum',
                26:'Chemical',
                30:'Non-metallic',
                31:'Ferrous',
                32:'Non-ferrous',
                44:'CPPs'}
    
    title = {'EOP':'EOP',
              'EF':'EF',
              'ES':'ES',
              'EI':'EI',
              'TP':'TP'}
    result.rename(columns=title,inplace = True)
    
    result1.rename(columns=title,inplace = True)
    
    result1['ind'] = 44
    result1['Energy Structure'] = None
    data = result.append(result1)
    data.index =range(len(data))
    
    factors = ['EOP','EF','ES','EI','TP']

    df = data[['ind','region'] + factors]
    
    
    df['Sector'] = df['ind'].map(ind_map)
    df.drop(['ind'],axis=1)
    
    plt.rcParams.update({'font.size': 20})
    fig = plt.figure(figsize=(25,6), frameon = False, dpi=300)
    plt.rc('font',family='arial') 
    
    itr = 0
    sectors = ['Paper','Petroleum','Chemical','Non-metallic','Ferrous','Non-ferrous','CPPs']
    
    for region in ['EASTERN','CENTRAL','WESTERN','NATIONAL']:
        itr = itr+1
        ax0 = fig.add_subplot(1,4,itr)
        dataset = pd.DataFrame()
        for factor in factors:
            l = []
            for sector in sectors:
                l.append(df[df['region']==region][df['Sector']==sector][factor].max())
            dataset[factor] = pd.Series(l,index=sectors)
       
        ax0.grid(False)

    
        if itr ==1:
            sns.heatmap(data=dataset,annot=False,center=1,cmap="RdBu_r",fmt='.2f',
                                  cbar_kws={"orientation":"vertical"}, ax = ax0,vmax=2,vmin=0,
                                  linewidths=1.6) 
            ax0.set_ylabel(str.upper(pol + '\n'),fontsize=24)
        else:

            sns.heatmap(data=dataset,annot=False,center=1,cmap="RdBu_r",fmt='.2f',
                                    cbar_kws={"orientation":"vertical"},ax = ax0,
                                    vmax=2,vmin=0,yticklabels = False,linewidths=1.6,) 
        # ax0.tick_params(labelsize=20)
        if pol=='so2':
            ax0.set_title(region)

    # ax0.text(-12.5,8.0,"Effect of Factors in Decompositions for %s"  %str.upper(pol), fontdict={'size': '24', 'color': 'black'})
    fig.subplots_adjust(hspace=0.3, wspace=0.18)
    # fig.savefig(r'C:\Users\18110\Desktop\协同\final-result\lmdi\pic\heatmap_%s.png'%pol,dpi=300,bbox_inches="tight")
    fig.savefig(r'.\final-result\lmdi\pic\heatmap_%s.png'%pol,bbox_inches="tight")
    
def pinjie(workspace,file1,file2,filename):
    Image.MAX_IMAGE_PIXELS = None
    f1 = Image.open(workspace + file1)
    f2 = Image.open(workspace + file2)
    adj = f1.size[0]/f2.size[0]
    s1 = f1.size[0]
    s2 = int(adj * f2.size[1])
    f2_new = f2.resize((s1, s2),Image.ANTIALIAS)
    result = Image.new('RGBA', (f1.size[0], f1.size[1]+f2_new.size[1]),255)
    result.paste(f1, (0, 0))
    result.paste(f2_new, (0, f1.size[1]))
    # 保存图片
    result.save(workspace + filename)
workspace = r'./final-result/lmdi/pic/'
file1 = "heatmap_so2.png"
file2 = "heatmap_nox.png"
pinjie(workspace,file1,file2,'so2_nox.png')

file1 = "so2_nox.png"
file2 = "heatmap_pm.png"
pinjie(workspace,file1,file2,'heatmap_used.png')