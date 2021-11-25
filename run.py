import numpy as np
import pandas as pd
import tweepy
import json_lines
import re
import json
from urllib.parse import urlparse
import requests
import sys

def extra_link(text):
    pattern='http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    return re.findall(pattern,text)

def check_domain(url_list):
    if url_list:
        try:
            r=requests.head(url_list[0]) 
            link=r.headers['location']
            domain=urlparse(link).netloc
            return domain
        except:
            try: 
                link=requests.get(url_list[0]).url
                domain=urlparse(link).netlocA
                return domain
            except:
                return ''
    return ''

def main(targets):
    #EDA: find link/RT/ check number of unqiue author
    if 'EDA' in targets:
        df = pd.read_pickle("test/testdata/test.pkl")
        pattern_link='.*https://t.co.*'
        pattern_re='RT.*'
        series_a=df['text'].str.contains(pattern_re)  
        series_b=df['text'].str.contains(pattern_link)
        P_re=series_a.mean()
        P_url=series_b.mean()
        unqiue_author=len(df['author_id'].unique())

        with open('result.txt', 'w') as f:
            f.write('EDA:'+'\n')
            f.write('- the proportion of tweets that contain a URL is '+str(P_url)+'\n')
            f.write('- the number of unique users is '+str(unqiue_author)+'\n')
            f.write('- the proportion of the data that are retweets '+str(P_re)+'\n')
            f.write('\n')
        ax=df.groupby('author_id').count().groupby('text').count()['id'].plot()
        ax.figure.savefig('same_author.jpg')

    #checked misinformation
    if 'misinfo' in targets:
        misinfo=pd.read_csv('test/testdata/iffy.csv')
        domains=misinfo['Domain']
        link_list=df['text'].apply(extra_link)
        checked=link_list.apply(lambda x:check_domain(x))
        proportion_mis=checked.apply(lambda x: x in domains).mean()
        with open('result.txt', 'a') as f:
            f.write('Misinformation:'+'\n')
            f.write('- the proportion of misinformation is '+str(proportion_mis)+'\n')
            f.write('\n')

    #find the top popular tweets
    if 'top_tweets' in targets:
        df['retweet']=df['public_metrics'].apply(lambda x: x['retweet_count'])
        most_popular=df.sort_values('retweet').head(200)
        most_popular.to_csv('most_popular.csv')
    return 

if __name__ == '__main__':
    # run via:
    # python run.py EDA misinfo top_tweets
    targets = sys.argv[1:]
    main(targets)