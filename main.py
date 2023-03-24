from apiclient.discovery import build
# from apiclient.errors import HttpError
# from oauth2client.tools import argparser

import os
# # .envファイルの内容を読み込見込む
from dotenv import load_dotenv
load_dotenv()


DEVELOPER_KEY = os.environ['KEY']
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# def youtube_search(options):
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

"""
■パラメータ
q:検索クエリ
part:リソースのプロパティをカンマ区切りでリスト化
viewCount:再生回数の多い順に並べる
video:動画
maxResults:検索結果の最大数
"""


q = 'Python 自動化'
max_results = 30

response = youtube.search().list(
    q=q,
    part="id,snippet",
    order='viewCount',
    type='video',
    maxResults=max_results
).execute()

# print(response)

items = response['items']
item = items[0]
print(item)