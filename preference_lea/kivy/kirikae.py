# -*- coding: utf-8 -*
import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Util import Padding
import pandas as pd
import numpy as np
import requests
import uuid
import time
import datetime

from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.uix.floatlayout import FloatLayout
from kivy.resources import resource_add_path
from kivy.properties import StringProperty
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.app import App


resource_add_path('./fonts')
LabelBase.register(DEFAULT_FONT, 'mplus-2c-regular.ttf')

Builder.load_file('bases.kv')
Builder.load_file('affiliates.kv')
Builder.load_file('exchanges.kv')
Builder.load_file('settings.kv')

mac_address = uuid.UUID(int=uuid.getnode()).hex[-12:]  # macアドレス
ind_num = pd.read_csv('docs/auth.csv')['number'][0]  # 個体番号

"""アフィリエイト用関数"""
aff_url = 'https://sc5h2rnr68.execute-api.ap-northeast-1.amazonaws.com/issue/affiliate/{function}/{mail-address}/{mac-address}'
aff_header = {'x-api-key': 'eC16HptGk67dCGiDQiXY6kEXIP2U0naE1hGxrpd0'}

"""継続用関数"""
con_url = 'https://f8hl5hhfe6.execute-api.ap-northeast-1.amazonaws.com/continue/continue/{cont-id}/{number}/{mac-address}'
con_header = {'x-api-key': '7p553i7H2H4hmaMjkSjKD7ikYUuLdqG97c8jioMb'}

def encrypt(raw):
    origin = '4yKxQ5hMcUJixcG4Z8Lc5ZPBr5McS65X'  # 共通鍵
    key = (hashlib.md5(origin.encode('utf-8')).hexdigest()).encode('utf-8')
    iv = Random.get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    data = Padding.pad(raw.encode('utf-8'), AES.block_size, 'pkcs7')
    return base64.b64encode(iv + cipher.encrypt(data))

"""checked"""
##############################被アフィリエイト登録類##############################
"""紹介ID登録画面"""
class Affiliated(FloatLayout):
    def auth_aff(self, affid):  # 紹介ID入力
        try:
            if affid == '':  # 紹介IDがない場合
                self.clear_widgets()
                self.add_widget(Information())  # 注意事項画面へ
            else:
                """アフィリエイトした側の成果登録"""
                params = {'function': affid,
                          'mail-address': 'x@x',
                          'mac-address': mac_address+'/'+ind_num}

                res = requests.get(aff_url, headers=aff_header, params=params)
                aff_id = res.content.decode('utf-8')

                if not aff_id == 'error':
                    pops = AffiliatedPopup()
                    pops.open()
                else:
                    pops = AffiliatedErrorPopup()
                    pops.open()
        except Exception as e:
            print(e)
            pops = AffiliatedErrorPopup()
            pops.open()


"""アフィリエイトIDポップアップ"""
class AffiliatedPopup(Popup):
    pass


"""アフィリエイトIDエラーポップアップ"""
class AffiliatedErrorPopup(Popup):
    pass


"""紹介される人のメールアドレス登録画面"""
class Affdmail(FloatLayout):
    def address_popup(self,address, verification):
        if str(address) == str(verification) and '@' in address:
            pops = AfdmailPopup()  # アフィリエイトされる側メールポップアップ
            pops.open()
        else:
            pops = AfdmailErrorPopup()
            pops.open()


"""アフィリエイトされる側エラーポップアップ"""
class AfdmailErrorPopup(Popup):
    pass


"""アフィリエイトされる側メールポップアップ"""
class AfdmailPopup(Popup):
    def register_address(self,address):
        try:
            params = {'function': 'afd',  # アフィリエイトされる側のデータ登録
                      'mail-address': address,
                      'mac-address': mac_address+'/'+ind_num}

            requests.get(aff_url, headers=aff_header, params=params)

        except Exception as e:
            print(e)
##############################被アフィリエイト登録類##############################


"""checked"""
##############################規約類##############################
"""注意事項画面"""
class Information(FloatLayout):
    """利用規約画面へ遷移"""
    def go_termofuse(self):
        self.clear_widgets()
        self.add_widget(TermOfUse())
    message = ''
    message_list = list(pd.read_csv('docs/message.csv')['message'])
    for i in message_list:
        message += ' {}\n'.format(i)


"""利用規約画面"""
class TermOfUse(FloatLayout):
    term_of_use = ''
    term_list = list(pd.read_csv('docs/term_of_use.csv')['message'])
    for i in term_list:
        term_of_use += ' {}\n'.format(i)

    def register_ini(self):
        pd.DataFrame([1], columns=['ini']).to_csv('docs/ini.csv', index=False)  # 起動済みを登録
##############################規約類##############################


##############################取引所選択##############################
"""取引所選択画面"""
class SelectExchange(FloatLayout):
    def fire_popup(self):
        pops = ExchangePopup()
        pops.open()


"""取引所選択ポップアップ"""
class ExchangePopup(Popup):
    def register_ex(self, exchange):
        pd.DataFrame([exchange], columns=['exchange']).to_csv('docs/exchange.csv', index=False)  # 取引所を登録
##############################取引所選択##############################

"""checked"""
##############################キー登録##############################
"""キー登録画面"""
class RegisterKey(FloatLayout):
    def key_popup(self, api_key, sct_key):
        try:
            if str(api_key) == '' or str(sct_key) == '':
                pops = KeyErrorPopup()
                pops.open()
            else:
                pops = KeyPopup()
                pops.open()
        except Exception as e:
            print(e)
            pops = KeyErrorPopup()
            pops.open()


"""キー登録ポップアップ"""
class KeyPopup(Popup):
    def register_keys(self, api_key, sct_key):
        api_key = api_key.replace('\n','').replace(' ','')
        sct_key = sct_key.replace('\n', '').replace(' ', '')
        enc_api = encrypt(api_key).decode('utf-8')
        sct_api = encrypt(sct_key).decode('utf-8')
        temp=np.array([enc_api,sct_api]).reshape(1,2)
        pd.DataFrame(temp,columns=['APIKEY','SCTKEY']).to_csv('docs/keys.csv', index=False)  # キーをcsvに登録


"""キー登録エラーポップアップ"""
class KeyErrorPopup(Popup):
    pass
##############################キー登録##############################


"""checked"""
##############################ホーム##############################
"""ホーム画面"""
class Home(FloatLayout):
    am_ex = pd.read_csv('docs/am_ex.csv')
    am = str(am_ex['amount'][0])
    ex = str(am_ex['expire'][0])
    tm = am_ex['tiem'][0]

    def refresh(self):
        try:
            am_ex = pd.read_csv('docs/am_ex.csv')
            am = str(am_ex['amount'][0])
            ex = str(am_ex['expire'][0])
            tm = am_ex['tiem'][0]
            if time.time() - tm > 0:
                header = {'x-api-key': 'SkJ3aMkpJ73c4OCmXIo63at4ENpnv5xc4AuzZneA'}
                url = 'https://0vvz2d31b7.execute-api.ap-northeast-1.amazonaws.com/auth/auth/{number}/{ex-date}/{mac-address}'
                auth_data = pd.read_csv('docs/auth.csv')  # 認証ファイル読み込み
                mac_address = uuid.UUID(int=uuid.getnode()).hex[-12:]  # macアドレス
                number = auth_data['number'][0]  # 個体番号

                params = {'number': number,
                          'ex_date': 'auth',
                          'mac-address': mac_address}

                res = requests.get(url, headers=header, params=params)  # 認証リクエスト
                am = float(res.content.decode('utf-8').split('/')[0])
                ex = int(res.content.decode('utf-8').split('/')[2])
                dx = datetime.datetime.fromtimestamp(ex)
                temp = np.array([am, str(dx)[:10], time.time()]).reshape(1, 3)
                pd.DataFrame(temp, columns=['amount', 'expire', 'tiem']).to_csv('docs/am_ex.csv', index=False) # 設定保存
                print(am)

                return str(am), str(dx)[:10]
            else:
                return str(am), str(0)
        except:
            pass

##############################ホーム##############################


"""checked"""
##############################取引設定##############################
"""設定画面"""
class Setting(FloatLayout):
    def register_setting(self, amount):
        if amount == '':
            pops = SettingErrorPopup()
            pops.open()
        else:
            pops = SettingPopup()
            pops.open()


"""取引量登録ポップアップ"""
class SettingPopup(Popup):
    def register_setting(self, amount, emergency):
        temp = np.array([amount, emergency]).reshape(1, 2)
        pd.DataFrame(temp, columns=['amount', 'emergency']).to_csv('docs/setting.csv', index=False) # 設定保存


"""取引量登録エラーポップアップ"""
class SettingErrorPopup(Popup):
    pass
##############################取引設定##############################


"""cheked"""
##############################アフィリエイト設定##############################
"""アフィリエイト画面"""
class Affiliate(FloatLayout):
    aff = pd.read_csv('docs/affiliate_id.csv')['id'][0]
    affiliate_id = '紹介IDは発行されていません' if aff == 0 else aff

    params = {'function': 'get',
              'mail-address': 'x@x',
              'mac-address': aff}
    try:
        if not aff == 0:
            res = requests.get(aff_url, headers=aff_header, params=params)

            len_of = res.content.decode('utf-8')
            if int(len_of) < 2:
                ratio = '35'
            elif 2 <= int(len_of) < 6:
                ratio = '40'
            elif 6 <= int(len_of) < 11:
                ratio = '50'
            else:
                ratio = '60'
        else:
            ratio = '35'
            len_of = str(0)
    except:
        ratio = '35'

    """紹介料詳細へ遷移"""
    def go_affdetail(self):
        self.clear_widgets()
        self.add_widget(Affdetail())

    """紹介ID発行画面へ遷移"""
    def go_issue(self):
        if self.affiliate_id == '紹介IDは発行されていません':
            self.clear_widgets()
            self.add_widget(Issue())
        else:
            self.clear_widgets()
            self.add_widget(Issued())


"""アフィリエイトID発行"""
class Issue(FloatLayout):
    def address_popup(self,address, verification):
        if address == verification and '@' in address:
            pops = AddressPopup()
            pops.open()
        else:
            pops = AddressErrorPopup()
            pops.open()


"""アフィリエイトID発済"""
class Issued(FloatLayout):
    pass


"""アフィリエイト料詳細"""
class Affdetail(FloatLayout):
    pass


"""アドレス確認ポップアップ"""
class AddressPopup(Popup):
    def register_address(self,address):
        params = {'function': 'init',
                  'mail-address': address,
                  'mac-address': mac_address}
        try:
            res = requests.get(aff_url, headers=aff_header, params=params)

            aff_id = res.content.decode('utf-8')
            if not aff_id == 'error':
                aff = pd.DataFrame([aff_id], columns=['id'])
                aff.to_csv('docs/affiliate_id.csv', index=False)
            else:
                print(aff_id)
        except Exception as e:
            print(e)


"""アドレスエラーポップアップ"""
class AddressErrorPopup(Popup):
    pass
##############################アフィリエイト設定##############################


##############################継続設定##############################
"""継続設定画面"""
class Continue(FloatLayout):
    def continue_popup(self, cont_id):
        params = {'number': ind_num,
                  'cont-id':cont_id,
                  'mac-address':mac_address}
        try:
            res = requests.get(con_url, headers=con_header, params=params)
            message = res.content.decode('utf-8')

            if message[:8] == 'succsess':
                amount = float(message.split(':')[1])
                auth_data = pd.read_csv('docs/auth.csv')
                ordered = auth_data['ordered'][0]
                number = auth_data['number'][0]
                temp = {'amount': amount,
                        'number': number,
                        'ordered': ordered}
                pd.DataFrame([temp]).to_csv('docs/auth.csv', index=False)
                pops = ContinuePopup()
                pops.open()
            else:
                pops = ContinueErrorPopup()
                pops.message = message
                pops.open()
        except Exception as e:
            print(e)
            pops = ContinueErrorPopup()
            pops.open()

"""継続画面ポップアップ"""
class ContinuePopup(Popup):
    pass

"""継続エラーポップアップ"""
class ContinueErrorPopup(Popup):
    pass

##############################継続設定##############################


"""パスワードが正しくない場合の画面"""
class WrongPass(FloatLayout):
    pass


class MainRoot(FloatLayout):
    def __init__(self, **kwargs):
        super(MainRoot, self).__init__(**kwargs)
        self.password = StringProperty()
        self.exchange = StringProperty()
        self.api_key = StringProperty()
        self.sct_key = StringProperty()
        self.amount = StringProperty()
        self.emergency = StringProperty()
        self.address = StringProperty()
        self.affdmail = StringProperty()
        self.affiliated_id = StringProperty()

    """パスワード認証、画面遷移"""
    def auth_password(self):
        if self.password == '':
            if pd.read_csv('docs/ini.csv')['ini'][0] == 1:
                """起動済みの場合"""
                self.clear_widgets()
                self.add_widget(Home())
            else:
                """初回起動の場合紹介コード入力へ"""
                self.clear_widgets()
                self.add_widget(Affiliated())
        else:
            """パスワードが違う場合"""
            self.clear_widgets()
            self.add_widget(WrongPass())

    """アフィリエイトされる人メールアドレス登録画面へ遷移"""
    def go_affdmail(self):
        self.clear_widgets()
        self.add_widget(Affdmail())  # 紹介される人のメールアドレス登録画面

    """キー登録画面へ遷移"""
    def go_resisterkey(self):
        self.clear_widgets()
        self.add_widget(RegisterKey())

    """ホーム画面へ遷移"""
    def go_home(self):
        self.clear_widgets()
        self.add_widget(Home())

    """取引所選択画面へ遷移"""
    def go_selectexchange(self):
        self.clear_widgets()
        self.add_widget(SelectExchange())

    """注意事項画面へ遷移"""
    def go_information(self):
        self.clear_widgets()
        self.add_widget(Information())

    """基本設定画面へ遷移"""
    def go_setting(self):
        self.clear_widgets()
        self.add_widget(Setting())

    """紹介画面へ遷移"""
    def go_affiliate(self):
        self.clear_widgets()
        self.add_widget(Affiliate())

    """継続画面へ遷移"""
    def go_continue(self):
        self.clear_widgets()
        self.add_widget(Continue())

class MainApp(App):
    def build(self):
        self.icon = 'rebellio-icon.png'
        self.title = 'Lea'
        return MainRoot()


if __name__ == "__main__":
    app = MainApp()
    app.run()