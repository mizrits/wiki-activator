from sydney import SydneyClient
import os
import asyncio
import requests
from pytrends.request import TrendReq
import datetime
import re
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
    s=os.environ["ACTIVATOR_BOT_NAME"]
    pw=os.environ["ACTIVATOR_BOT_PASSWORD"]
    p=datetime.datetime.now().strftime('話題/%Y年第%V週')
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
        "lgname": s,
        "lgpassword": pw,
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
        "title": p,
        "token": CSRF_TOKEN,
        "format": "json",
        "appendtext": post
    }
    R = S.post(API_ENDPOINT, data=PARAMS_3)
    print(R.json())
