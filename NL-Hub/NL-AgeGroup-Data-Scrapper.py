import re 
import warnings
import requests 
import numpy as np 
import pandas as pd 
from cgitb import html
from email import header
from datetime import datetime
from bs4 import BeautifulSoup
from collections import defaultdict
warnings.filterwarnings('ignore')
pd.options.display.max_rows = None
pd.options.display.max_columns = None

def convert_figures_inwords2_integers(textnum, numwords={}):
    if not numwords:
        units = [
                "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
                "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
                "sixteen", "seventeen", "eighteen", "nineteen",
                ]
        tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
        scales = ["hundred", "thousand", "million", "billion", "trillion"]
        numwords["and"] = (1, 0)
        for idx, word in enumerate(units):  numwords[word] = (1, idx)
        for idx, word in enumerate(tens):       numwords[word] = (1, idx * 10)
        for idx, word in enumerate(scales): numwords[word] = (10 ** (idx * 3 or 2), 0)
    ordinal_words = {'first':1, 'second':2, 'third':3, 'fifth':5, 'eighth':8, 'ninth':9, 'twelfth':12}
    ordinal_endings = [('ieth', 'y'), ('th', '')]
    textnum = textnum.lower()
    textnum = textnum.replace('-', ' ')
    current = result = 0
    curstring = ""
    onnumber = False
    for word in textnum.split():
        if word in ordinal_words:
            scale, increment = (1, ordinal_words[word])
            current = current * scale + increment
            if scale > 100:
                result += current
                current = 0
            onnumber = True
        else:
            for ending, replacement in ordinal_endings:
                if word.endswith(ending):
                    word = "%s%s" % (word[:-len(ending)], replacement)
            if word not in numwords:
                if onnumber:
                    curstring += repr(result + current) + " "
                curstring += word + " "
                result = current = 0
                onnumber = False
            else:
                scale, increment = numwords[word]
                current = current * scale + increment
                if scale > 100:
                    result += current
                    current = 0
                onnumber = True
    if onnumber:
        curstring += repr(result + current)

    return curstring


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'}
url = 'https://www.gov.nl.ca/releases/covid-19-news/'

EasternHealth_dict = {'date': [],'under 20' : [], '20-39': [], '40-49': [], '50-59': [], '60-69': [], '70': []}
CentralHealth_dict = {'date': [],'under 20' : [], '20-39': [], '40-49': [], '50-59': [], '60-69': [], '70': []}
WesternHealth_dict = {'date': [],'under 20' : [], '20-39': [], '40-49': [], '50-59': [], '60-69': [], '70': []}
LabradorGrenfellHealth_dict = {'date': [],'under 20' : [], '20-39': [], '40-49': [], '50-59': [], '60-69': [], '70': []}
Private_dict = {'date': [],'under 20' : [], '20-39': [], '40-49': [], '50-59': [], '60-69': [], '70': []}
skipped_links = {'date': [], 'link': []}
source = {'date': [], 'link': []}
req = requests.get(url, headers = headers)
soup = BeautifulSoup(req.text, 'html.parser')
page_content = soup.find("div", {"class": "this-weeks-news"})
page_content = page_content.find_all('a',{'rel':'bookmark'})
print('#+#'*36)
print(f'COVID-19 Data Update From Newfoundland and Labrador Downloading. This Will Take Time, Please Be Patient !!!')
print('#+#'*36)
print('')
for i in range(len(page_content)):
    if 'COVID-19 in Newfoundland and Labrador' in page_content[i].text:
        data_url = page_content[i]['href']
        data_info_link = requests.get(data_url, headers = headers) 
        link_soup = BeautifulSoup(data_info_link.text, 'html.parser')
        date = link_soup.find('p', {'class':'date'}).text
        date = date.replace(',','').split()
        date = datetime.strptime('-'.join(date), "%B-%d-%Y").date().strftime('%Y-%m-%d')
        link_content = link_soup.find('div', {'class':'entry-content'}).find_all('ul')
        if len(link_content) > 3:
            print(f'{date} -- COVID-19 Age-Group Structure Detected. Download Underway..,!!!')
            health_dict = [EasternHealth_dict, CentralHealth_dict, WesternHealth_dict, LabradorGrenfellHealth_dict, Private_dict]
            for ul in range(len(link_content[:5])):
                dictt = health_dict[ul]
                dictt['date'].append(date)
                source['date'].append(date)
                source['link'].append(data_url)
                ul_data = link_content[ul]
                ha_data = ul_data.text.split('\n')
                ha_data = [info for info in ha_data if info != '']
                stripwords = ['years of age','years of age.','years of age;','years of age; and','years of age and above.']
                if len(ha_data) != 6:
                    topup = ['0' for x in range(6 -len(ha_data))]
                    ha_data.extend(topup)
                for ageinfo in ha_data:
                    ageinfo = ageinfo.replace(';','')
                    for col, val in dictt.items():
                        if (col == 'date') | (col == 'source'):
                            continue
                        if col in ageinfo:
                            ageinfo = [ageinfo.replace(stripwords[j],'') for j in range(len(stripwords)) if stripwords[j] in ageinfo]
                            if len(ageinfo) != 0:
                                ageinfo = ageinfo[0]
                            else:
                                ageinfo = '0'
                            ageinfo = convert_figures_inwords2_integers(ageinfo)
                            dictt[col].append(ageinfo.split()[0])
                datelen = len(dictt[list(dictt.keys())[0]])
                for ky, vl in dictt.items():
                    if ky != 'date':
                        if len(dictt[ky]) < datelen:
                            ext = ['0' for x in range(datelen - len(dictt[ky]))]
                            vl.extend(ext)
                        else:
                            continue
        else:
            for kys, vls in skipped_links.items():
                if kys == 'date':
                    skipped_links[kys].append(date)
                if kys == 'link':
                    skipped_links[kys].append(data_url)

# creating dataframe for each RHA after download     
df1 = pd.DataFrame(EasternHealth_dict)
df1['health_authority'] = 'eastern_ha'

df2 = pd.DataFrame(CentralHealth_dict)
df2['health_authority'] = 'central_ha'

df3 = pd.DataFrame(WesternHealth_dict)
df3['health_authority'] = 'western_ha'

df4 = pd.DataFrame(LabradorGrenfellHealth_dict)
df4['health_authority'] = 'labradorgrenfell_ha'

df5 = pd.DataFrame(Private_dict)
df5['health_authority'] = 'private'

df6 = pd.DataFrame(skipped_links)

source = pd.DataFrame(source)

def df_name(data):
    name =[x for x in globals() if globals()[x] is data][0]
    return name

DF = [df1,df2,df3,df4, df5,df6,source]
for df in DF:
    if df_name(df) == 'df1':
        name = 'eha'
        # saving data for Eastern HA
        # df.to_csv('df'+'_'+name+'.csv', index=False)
        
    if df_name(df) == 'df2':
        name = 'cha'
        # saving data for central HA
        # df.to_csv('df'+'_'+name+'.csv', index=False)
        
    if df_name(df) == 'df3':
        name = 'wha'
        # saving data for Western HA
        # df.to_csv('df'+'_'+name+'.csv', index=False)
    if df_name(df) == 'df4':
        name = 'lgha'
        # saving data for Labrabor-Grenfell
        # df.to_csv('df'+'_'+name+'.csv', index=False)
        
    if df_name(df) == 'df5':
        name = 'pha'
        # saving data for the private rha
        # df.to_csv('df'+'_'+name+'.csv', index=False)
        
    if df_name(df) == 'source':
        name = 'datalinks'
        # df.to_csv('df'+'_'+name+'.csv', index=False)
RHA_Cases_By_AgeGroup = pd.concat([df1, df2,df3,df4,df5], axis=0)
# RHA_Cases_By_AgeGroup.to_csv('RHA_Cases_By_AgeGroup.csv',index=False)
print('')
print('#+#'*10)
print('Data Download Completed...!!!')
print('#+#'*10)
