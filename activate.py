from sydney import SydneyClient
import os
import asyncio
import requests
from pytrends.request import TrendReq
import datetime
import re
import random
#os.environ["BING_COOKIES"] = "" //secrets

async def main() -> None:
    global post
    df = TrendReq(hl='ja-jp',tz=540).trending_searches(pn='japan')
    topic1=df.at[0,0]
    topic2=df.at[1,0]
    topic3=df.at[2,0]
    async with SydneyClient(style="creative") as sydney:
        response1 = await sydney.ask(topic1+"に関するニュース記事について要約して。要約文本文のみ")
        #print(response1)
        response2 = await sydney.ask(topic2+"に関するニュース記事について要約して。要約文本文のみ")
        #print(response2)
        response3 = await sydney.ask(topic3+"に関するニュース記事について要約して。要約文本文のみ")
        #print(response3)
        markdown="\n=={{subst:CURRENTYEAR}}-{{subst:CURRENTMONTH}}-{{subst:CURRENTDAY2}}のトレンド上位3つ==\n==="+topic1+"===\n"+response1+"\n\n==="+topic2+"===\n"+response2+"\n\n==="+topic3+"===\n"+response3
        postpre=re.sub('\[(.*)\]\((.*)\)', '[\\2 \\1]', markdown).replace('\n- ', '\n* ').replace("**", "'''")
        post=re.sub('\[\^(.*)\^\]', '', postpre)
        #print(post)


if __name__ == "__main__":
    asyncio.run(main())
    ##var
    u=os.environ["ACTIVATOR_BOT_NAME"]
    p=os.environ["ACTIVATOR_BOT_PASSWORD"]
    t=datetime.datetime.now().strftime('話題/%Y年第%V週')
    r=random.randint(1, 100) % 10
    if r == 0:
        s="今日もいろいろありましたねー。"
    elif r == 1:
        s="毎日様々な出来事が起き、忘れられる。。。"
    elif r == 2:
        s="日課の更新"
    elif r == 3:
        s="今日のニュース"
    elif r == 4:
        s="daily"
    elif r == 5:
        s="時の流れは速い"
    elif r == 6:
        s="日報"
    elif r == 7:
        s="今日の日報"
    elif r == 8:
        s="定期"
    else:
        s=""
    API_ENDPOINT = os.environ["ACTIVATOR_WIKIAPI"]
    ##access
    S = requests.Session()
    #fetch login token
    PARAMS_0 = {
        "action": "query",
        "meta": "tokens",
        "type": "login",
        "format": "json"
    }
    R = S.get(url=API_ENDPOINT, params=PARAMS_0)
    LOGIN_TOKEN = R.json()['query']['tokens']['logintoken']
    #login
    PARAMS_1 = {
        "action": "login",
        "lgname": u,
        "lgpassword": p,
        "lgtoken": LOGIN_TOKEN,
        "format": "json"
    }
    R = S.post(API_ENDPOINT, data=PARAMS_1)
    #fetch CSRF token
    PARAMS_2 = {
        "action": "query",
        "meta": "tokens",
        "format": "json"
    }
    R = S.get(url=API_ENDPOINT, params=PARAMS_2)
    CSRF_TOKEN = R.json()['query']['tokens']['csrftoken']
    #POST request to edit a page
    PARAMS_3 = {
        "action": "edit",
        "title": t,
        "token": CSRF_TOKEN,
        "format": "json",
        "appendtext": post,
        "summary": s
    }
    R = S.post(API_ENDPOINT, data=PARAMS_3)
    print(R.json())
