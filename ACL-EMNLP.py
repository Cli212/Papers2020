#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from tqdm import tqdm, tqdm_notebook


# In[5]:


conf_list = ['acl-2020','emnlp-2020']
headers = {'content-type': 'application/json',
           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'}


# In[6]:


for conf_name in conf_list:
    page = requests.get(f'https://www.aclweb.org/anthology/events/{conf_name}/',headers = headers)
    alias = conf_name.split('-')[1] + '-' + conf_name.split('-')[0] + '-main'
    soup = bs(page.text,'lxml')
    paper_list = soup.find('div',{'id':f'{alias}'}).find_all('p',{'class':'d-sm-flex align-items-stretch'})
    df_list = []
    for paper in tqdm_notebook(paper_list):
        detail_url = 'https://www.aclweb.org' + paper.find_all('span',{'class':'d-block'})[-1].find('a')['href']
        detail = bs(requests.get(detail_url,headers = headers).text,'lxml')
        title = detail.find('h2',{'id':'title'}).text
        authors = detail.find('p',{'class':'lead'}).text.replace('\n','')
        try:
            abstract = detail.find('div',{'class':'card-body acl-abstract'}).text.lstrip('Abstract')
        except:
            continue
        paper_url = detail.find('h2',{'id':'title'}).find('a')['href']
        df_list.append(pd.DataFrame({'title':[title],'abstract':[abstract],'authors':[authors],'link':[paper_url],'detail':[detail_url]}))
    pd.concat(df_list,ignore_index=True).to_csv(f'{conf_name}_papers.csv',index=False)


# In[17]:


filters = {'QA':'QA|question answering|Question Answering','Distillation':'distillation|Distillation|distill|Distill'}


# In[18]:


import os
for file in os.listdir():
    if file.endswith('.csv'):
        print(f'Processing {file}')
        df = pd.read_csv(file)
        for key in filters.keys():
            df.loc[df['abstract'].str.contains(filters[key])].to_csv(f'{file}_{key}.csv',index=False)


# In[ ]:




