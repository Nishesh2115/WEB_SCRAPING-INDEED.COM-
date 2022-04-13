import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st

st.set_page_config(page_title="ok")
st.header("Webscraping project")
st.subheader("LET'S SEARCH SOME JOBS...")


def extract(page):
    headers={'User-Agnet' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36'}
    url=f'https://in.indeed.com/jobs?q=python%20developer&l=Pune,%20Maharashtra&start={page}&vjk=674f20bad0f2174e'
    r=requests.get(url,headers)
    soup = BeautifulSoup(r.content,'html.parser')
    return soup

def transform(soup):
    divs = soup.find_all('div',class_ = 'job_seen_beacon')
    for item in divs:
        title = item.find('span').text.strip()
        company = item.find('span',class_='companyName').text.strip()
        try:
            salary = item.find('div',class_='metadata salary-snippet-container').text.strip()
        except:
            salary = '' 
        summary = item.find('div',class_='job-snippet').text.strip().replace('\n','')
        
        
        job = {
            'title' : title,
            'company' : company,
            'salary' : salary,
            'summary' : summary
        }
        
        joblist.append(job)
    return


joblist = []

for i in range(0,40,10):
    print(f'getting page,{i}')
    c = extract(0)
    transform(c)
    
print(len(joblist))

df = pd.DataFrame(joblist)

st.dataframe(df)

print(df.head())
df.to_csv('jobs.csv')
