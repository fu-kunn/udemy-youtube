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

df_video = video_search(youtube, q='Python 自動化', max_results=30)
print(df_video[:3])