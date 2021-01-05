#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup as bs
from tqdm import tqdm, tqdm_notebook
import pandas as pd


# In[2]:


headers = {'content-type': 'application/json',
           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'}


# In[3]:


soup = bs(requests.get('https://coling2020.org/pages/accepted_papers_main_conference',headers = headers).text, 'lxml')


# In[4]:


paper_list = soup.find('ul',{'id':'list_of_papers'}).find_all('li')


# In[5]:


abstract_list = soup.find('ul',{'id':'list_of_papers'}).find_all('div',{'class':'modal fade'})


# In[6]:


assert len(paper_list) == len(abstract_list)


# In[8]:


df_list = []
for i in tqdm_notebook(range(len(paper_list))):
    title = paper_list[i].find('strong').text
    authors = paper_list[i].find('span',{'class':'text-muted'}).text
    abstract = abstract_list[i].find('div',{'class':'modal-body'}).find_all('p')[-1].text.lstrip('\n').lstrip()
    try:
        arxiv = bs(requests.get(f'http://export.arxiv.org/api/query?search_query=ti:{title}').text)
        url = arxiv.find('entry').find('id').text
    except Exception as e:
        print(e)
        url = ''
    df_list.append(pd.DataFrame({'title':[title],'abstract':[abstract],'authors':[authors],'url':[url]}))


# In[11]:


pd.concat(df_list,ignore_index=True).to_csv('COLING_2020.csv',index=False)


# In[ ]:




