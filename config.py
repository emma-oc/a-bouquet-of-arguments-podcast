# replace the following with your own before running the script

import datetime

# email details
fromaddr = # your gmail addres
pwd = # RISK OF PASSWORD BREACH! DON'T PUBLISH THIS!!!
toaddr = # your recepients
Cc = # if any cc's

host = 'smtp.gmail.com'
port = 587

# email content
today = str(datetime.date.today())
# today = '2020-09-06'
filename = 'episode_performance_{}.pdf'.format(today)
filepath = # your path for the file to attach
subject = # your email subject title
body = # your email body

# set paths for local saved files
folder_path = # local saved folder
master_path = # master dataset
file = # daily snapshot of data refresh
figure_path = # daily refreshed file path

# data crawling
album_url = # url for your Ximalaya album to crawl
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
output_path = # path to your output folder

# parameters for failure retry
sleep_time = 60
num_retries = 5
