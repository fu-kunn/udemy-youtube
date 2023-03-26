from apiclient.discovery import build
# from apiclient.errors import HttpError
# from oauth2client.tools import argparser

import os
import pandas as pd

# # .envファイルの内容を読み込見込む
from dotenv import load_dotenv
load_dotenv()


"""
■パラメータ
q:検索クエリ
part:リソースのプロパティをカンマ区切りでリスト化
viewCount:再生回数の多い順に並べる
video:動画
maxResults:検索結果の最大数
"""

def video_search(youtube, q='自動化', max_results=50):
# q = 'Python 自動化'
# max_results = 30

    response = youtube.search().list(
        q=q,
        part="id,snippet",
        order='viewCount',
        type='video',
        maxResults=max_results
    ).execute()

    # print(response)
    items_id = []
    items = response['items']
    for item in items:
        item_id = {}
        item_id['video_id'] = item['id']['videoId']
        item_id['channel_id'] = item['snippet']['channelId']
        items_id.append(item_id)

    df_video = pd.DataFrame(items_id)

    return df_video

DEVELOPER_KEY = os.environ['KEY']
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)


# 関数化
df_video = video_search(youtube, q='Python 自動化', max_results=30)

def get_results(df_video, threshold=5000):
    """
    ・uniqueで重複を削除
    ・tolistでレスポンスをリスト化
    """
    channel_ids = df_video['channel_id'].unique().tolist()


    """
    idはカンマ区切りリストの形式
    statisticsはチャンネルの統計情報
    fildsは特定のプロパティだけを返す
    　➡︎statisticsの中の特定の情報（登録者数）を返すように使う
    """

    subscriber_list = youtube.channels().list(
        id=','.join(channel_ids),
        part="statistics",
        fields='items(id, statistics(subscriberCount))'
    ).execute()

    subscribers = []
    for item in subscriber_list['items']:
        subscriber = {}
        if len(item['statistics']) > 0:
            subscriber['channel_id'] = item['id']
            subscriber['subscriber_count'] = int(item['statistics']['subscriberCount'])
        else:
            subscriber['channel_id'] = item['id']

        subscribers.append(subscriber)

    df_subscribers = pd.DataFrame(subscribers)
    df = pd.merge(left=df_video, right=df_subscribers, on='channel_id')
    df_extracted = df[df['subscriber_count'] < threshold]
    video_ids = df_extracted['video_id'].tolist()

    """
    snippet(title):動画のタイトル
    statistics(viewCount):チャンネルの再生回数
    """
    videos_list = youtube.videos().list(
        id=','.join(video_ids),
        part='snippet, statistics',
        fields='items(id, snippet(title), statistics(viewCount))'
    ).execute()

    videos_info = []
    items = videos_list['items']
    for item in items:
        video_info = {}
        video_info['video_id'] = item['id']
        video_info['title'] = item['snippet']['title']
        video_info['view_count'] = item['statistics']['viewCount']
        videos_info.append(video_info)

    df_videos_info = pd.DataFrame(videos_info)

    results = pd.merge(left=df_extracted, right=df_videos_info, on='video_id')
    # グラフの列順を変更
    results = results.loc[:, ['video_id', 'title', 'view_count', 'subscriber_count', 'channel_id']]

    return results

df_video = video_search(youtube, q='Python Excel', max_results=50)
test = get_results(df_video, threshold=1000)
print(test)