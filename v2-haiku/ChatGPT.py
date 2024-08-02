import asyncio
#import sys
from selenium_driverless import webdriver
from selenium_driverless.types.by import By

class GetHaiku:
    def __init__(self):
        self.result = None

    async def getHaiku(self):
        print("Connecting chatgpt.com...")
        options = webdriver.ChromeOptions()
        #options.add_argument('--headless') # ヘッドレスモード
        options.add_argument('--incognito')  # シークレットモード
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0')
        #options.add_argument('--disable-blink-features=AutomationControlled')	
        #options.add_experimental_option('excludeSwitches', ['enable-automation'])	
        #options.add_experimental_option('useAutomationExtension', False)
        #Q: 回答は全てコードブロック内にお願いします。オリジナルの俳句をいくつか作ってください。その際、俳句の先頭にアスタリスクを入れて、1つの俳句は1行で記述してください
        chat_url = "https://chatgpt.com/?q=%E5%9B%9E%E7%AD%94%E3%81%AF%E5%85%A8%E3%81%A6%E3%82%B3%E3%83%BC%E3%83%89%E3%83%96%E3%83%AD%E3%83%83%E3%82%AF%E5%86%85%E3%81%AB%E3%81%8A%E9%A1%98%E3%81%84%E3%81%97%E3%81%BE%E3%81%99%E3%80%82%E3%82%AA%E3%83%AA%E3%82%B8%E3%83%8A%E3%83%AB%E3%81%AE%E4%BF%B3%E5%8F%A5%E3%82%92%E3%81%84%E3%81%8F%E3%81%A4%E3%81%8B%E4%BD%9C%E3%81%A3%E3%81%A6%E3%81%8F%E3%81%A0%E3%81%95%E3%81%84%E3%80%82%E3%81%9D%E3%81%AE%E9%9A%9B%E3%80%81%E4%BF%B3%E5%8F%A5%E3%81%AE%E5%85%88%E9%A0%AD%E3%81%AB%E3%82%A2%E3%82%B9%E3%82%BF%E3%83%AA%E3%82%B9%E3%82%AF%E3%82%92%E5%85%A5%E3%82%8C%E3%81%A6%E3%80%811%E3%81%A4%E3%81%AE%E4%BF%B3%E5%8F%A5%E3%81%AF1%E8%A1%8C%E3%81%A7%E8%A8%98%E8%BF%B0%E3%81%97%E3%81%A6%E3%81%8F%E3%81%A0%E3%81%95%E3%81%84"
        
        try:
            async with webdriver.Chrome(options=options) as driver:
                await driver.get(chat_url, wait_load=True)
                await driver.sleep(10)
                element = await driver.find_element(By.XPATH, '/html/body/div[1]/div/div/main/div[1]/div[1]/div/div/div/div/div[3]/div/div/div[2]/div/div[1]/div/div/div/pre/div/div[2]/code', timeout=10)
                haiku = await element.text  # .text を await で取得
                #await driver.page_source
                #await driver.save_screenshot('screenshot.png')
        except Exception as e:
            print(f"Error occurred: {e}")
            raise  # 再度例外を投げて、外部での処理に任せる
        finally:
            if driver:
                await driver.quit()
        self.result = haiku

    async def main(self):
        try:
            await self.getHaiku()
            return self.result
        except Exception as e:
            raise HaikuError(f"俳句の生成中にエラーが発生しました: {e}")
            #sys.exit(1)

class HaikuError(Exception):
    """カスタム例外クラス for HAIKU エラー"""
    def __init__(self, message):
        super().__init__(message)

if __name__ == "__main__":
    haiku = asyncio.run(GetHaiku().main())
    print(haiku)
