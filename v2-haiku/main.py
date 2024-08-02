import asyncio
import datetime
from ChatGPT import GetHaiku, HaikuError
from MediaWiki import WikiEditor, WikiAPIError

def main():
    # パラメータを設定
    API_ENDPOINT = "https://your.mediawiki.url/w/api.php"
    USERNAME = "username"
    PASSWORD = "password"
    PAGE_TITLE = "pagetitle"
    #NEW_CONTENT = "~~~~~"
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"

    try:
        # ChatGPTクラスで俳句を生成
        haiku = asyncio.run(GetHaiku().main())
        print("生成された俳句\n" + haiku)
        # WikiEditorクラスのインスタンスを作成して実行
        NEW_CONTENT = "\n=={{subst:LOCALMONTH}}月{{subst:LOCALDAY2}}日==\n" + haiku
        editor = WikiEditor(API_ENDPOINT, USERNAME, PASSWORD, PAGE_TITLE, NEW_CONTENT, USER_AGENT)
        editor.run()
    except HaikuError as he:
        print(f"HaikuError occurred: {he}")
    except WikiAPIError as we:
        print(f"WikiAPIError occurred: {we}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
