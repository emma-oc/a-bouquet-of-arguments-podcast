#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
import json
import requests
from bs4 import BeautifulSoup
import re
import datetime
from time import sleep

from config import *

def get_data(album_url, headers, output_path):

    # get html file and parse

    web_data = requests.get(album_url, 
                            headers = headers).text
    soup = BeautifulSoup(web_data, features="lxml")

    main_script = soup.find('script', text=re.compile('window\.__INITIAL_STATE__'))
    json_text = re.search(r'^\s*window\.__INITIAL_STATE__\s*=\s*({.*?})\s*;\s*$',
                          main_script.string, 
                          flags=re.DOTALL | re.MULTILINE).group(1)
    main_data = json.loads(json_text)

    # get numbers for our album
    total_play = main_data['store']['AlbumDetailPage']['albumInfo']['mainInfo']['playCount']
    subs = main_data['store']['AlbumDetailPage']['albumInfo']['mainInfo']['subscribeCount']
    num_fans = main_data['store']['AlbumDetailPage']['albumInfo']['anchorInfo']['anchorFansCount']
    tracks = main_data['store']['AlbumDetailPage']['albumInfo']['tracksInfo']['tracks']

    # get publish date for each track
    for track in tracks:
        track_url = 'https://www.ximalaya.com'+track['url']
        track_soup = BeautifulSoup(requests.get(track_url, headers = headers).text, features="lxml")
        track['publish_date'] = track_soup.find('span', {'class':'time _Td'}).text

    # final dataframe to save
    tracks_df = pd.DataFrame(tracks)
    tracks_df['album_total_play'] = total_play
    tracks_df['album_subs'] = subs
    tracks_df['num_fans'] = num_fans
    tracks_df['datapull_dt'] = datetime.date.today()

    tracks_df.to_csv(output_path+'ximalaya_data_{}.csv'.format(datetime.date.today()),encoding='utf_8_sig')
    print('data pull finished :)')


def main():
    crawled = False
    while not crawled:
        try:
            get_data(album_url, headers, output_path)
            crawled = True
        except:
            sleep(sleep_time)
            sleep_time *= 2 # if not successfull, double the sleep time
        

if __name__ == '__main__':
	main()