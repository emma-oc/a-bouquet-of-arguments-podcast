import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'sans-serif'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False #用来正常显示负号

from config import *


def update_figure(folder_path, master_path, file, figure_path):

    # read cumulative master dataset
    master_df = pd.read_csv(master_path, encoding='utf_8_sig')

    # get today's datapull
    today = str(datetime.date.today())
    today_df = pd.read_csv(file.format(today), index_col=0)
    today_df.sort_values('index', inplace=True)
    today_df['datapull_dt'] = pd.to_datetime(today_df['datapull_dt']).dt.date
    today_df['publish_date'] = pd.to_datetime(today_df['publish_date']).dt.date
    today_df['days_since_release'] = (today_df['datapull_dt'] - today_df['publish_date']).dt.days + 1

    # generate pivot table
    pvt_df = today_df[['title', 'playCount', 'days_since_release']].pivot(index='days_since_release', 
                                                                          columns='title', values='playCount')
    # merge master and latest datapoints
    merged = master_df.merge(pvt_df, left_index=True, right_index=True, how='outer')

    # final plotting
    for col in master_df.columns:
        merged[col] = merged[col+'_x'].fillna(merged[col+'_y'])


    fig = plt.figure(figsize=(12,5))
    ax = plt.subplot(111)
    merged[master_df.columns].plot(ax=ax)
    ax.set_xlabel('Days since release')
    ax.set_ylabel('Number of plays')
    ax.set_title('Episode Performance')
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    fig.tight_layout()
    plt.savefig(figure_path.format(today))

    # update master dataset
    merged[master_df.columns].to_csv(master_path, encoding='utf_8_sig', index=False)

    print('generated updated report :)')


def main():
    update_figure(folder_path, master_path, file, figure_path)

if __name__ == '__main__':
    main()