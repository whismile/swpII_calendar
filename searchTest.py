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