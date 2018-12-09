'''
import os
import sys
import urllib.request
client_id = "UnZj1xS4GqQeIL6leYHC"
client_secret = "V5yUIZsSSd"
encText = urllib.parse.quote("옷")
url = "https://openapi.naver.com/v1/search/blog.json?query=" + encText # json 결과
# url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # xml 결과
request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id",client_id)
request.add_header("X-Naver-Client-Secret",client_secret)
response = urllib.request.urlopen(request)
rescode = response.getcode()
if(rescode==200):
    response_body = response.read()
    print(response_body.decode('utf-8'))
else:
    print("Error Code:" + rescode)
'''
import pickle

holiday = [
    (1, 1, "신정"),
    (2, 15, "설날"),
    (2, 16, "설날"),
    (2, 17, "설날"),
    (3, 1, "삼일절"),
    (5, 5, "어린이날"),
    (5, 7, "월"),
    (5, 22, "부처님오신날"),
    (6, 6, "현충일"),
    (8, 15, "광복절"),
    (9, 23, "추석"),
    (9, 24, "추석"),
    (9, 25, "추석"),
    (10, 3, "개천절"),
    (10, 9, "한글날"),
    (12, 25, "크리스마스")
]

with open('./holiday.txt', 'wb') as f:
    pickle.dump(holiday, f)