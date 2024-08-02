import requests

class WikiEditor:
    def __init__(self, api_endpoint, username, password, page_title, new_content, user_agent):
        self.api_endpoint = api_endpoint
        self.username = username
        self.password = password
        self.page_title = page_title
        self.new_content = new_content
        self.session = requests.Session()
        # ユーザーエージェントを設定
        self.headers = {
            'User-Agent': user_agent
        }

    def login(self):
        try:
            # ログイントークンを取得
            login_token = self.session.get(self.api_endpoint, headers=self.headers, params={
                'action': 'query',
                'meta': 'tokens',
                'type': 'login',
                'format': 'json'
            }).json()['query']['tokens']['logintoken']
            print(f"login token: {login_token}")
            # ログイン
            response = self.session.post(self.api_endpoint, headers=self.headers, data={
                'action': 'login',
                'lgname': self.username,
                'lgpassword': self.password,
                'lgtoken': login_token,
                'format': 'json'
            }).json()
            if response['login']['result'] != 'Success':
                raise WikiAPIError(f"ログインに失敗しました: {response['login']['reason']}")
            else:
                print(f"Login: {response['login']['result']}")
        except Exception as e:
            raise WikiAPIError(f"リクエスト中にエラーが発生しました: {e}")

    def edit_page(self):
        try:
            # 編集トークンを取得
            edit_token = self.session.get(self.api_endpoint, headers=self.headers, params={
                'action': 'query',
                'meta': 'tokens',
                'format': 'json'
            }).json()['query']['tokens']['csrftoken']
            print(f"edit token: {edit_token}")
            # ページを編集する
            response = self.session.post(self.api_endpoint, headers=self.headers, data={
                'action': 'edit',
                'title': self.page_title,
                'appendtext': self.new_content,
                'token': edit_token,
                'format': 'json'
            }).json()
            
            if 'error' in response:
                raise WikiAPIError(f"ページの編集に失敗しました: {response['error']['info']}")
            print(response)
            print("ページが正常に更新されました。")
        except Exception as e:
            raise WikiAPIError(f"リクエスト中にエラーが発生しました: {e}")

    def run(self):
        try:
            self.login()
            self.edit_page()
        finally:
            self.session.close()

class WikiAPIError(Exception):
    """カスタム例外クラス for Wiki APIエラー"""
    def __init__(self, message):
        super().__init__(message)
