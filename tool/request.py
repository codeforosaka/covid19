import codecs
import copy
import os
import pandas as pd
import requests
import urllib.parse
from json import dumps, load
from typing import Dict
from datetime import datetime, timezone, timedelta


class DataJson:
    def __init__(self):
        self.json_file = 'data.json'
        self.cert_txt = './tool/client.txt'
        self.token_param = 'X-Cybozu-API-Token'
        self.token_env = 'KINTONE_API_TOKEN_'
        self.url_records = 'https://pref-osaka.s.cybozu.com/k/v1/records.json?'
        # self.url_records = 'https://pref-osaka.cybozu.com/k/v1/records.json?'
        # 今のdata.json読み込み
        self.current_data_json = self.get_json(self.json_file)
        # 全データ込
        self.data_json = {}
        # 陽性者の属性
        self.patients_json = {"date": "", "data": []}
        self.patients_open_data_json = {"date": "", "data": []}
        # 陽性者数
        self.patients_summary_json = {"date": "", "data": []}
        # 検査実施件数
        self.inspections_summary_json = {"date": "", "data": []}
        # 各種サマリー（オープンデータ）
        self.summary_open_data_json = {"date": "", "data": []}
        # 府民向け相談窓口への相談件数
        self.contacts1_summary_json = {"date": "", "data": []}
        self.contacts1_open_data_json = {"date": "", "data": []}
        # 新型コロナ受診相談センターへの相談件数
        self.contacts2_summary_json = {
            "date": "", "data": {"府管轄保健所": [], "政令中核市保健所": []}, "labels": []
        }
        self.contacts2_open_data_json = {"date": "", "data": []}
        # 感染経路不明者（リンク不明者）
        self.transmission_route_json = {
            "date": "", "data": {"感染経路不明者": [], "感染経路明確者": []}, "labels": []
        }
        # 退院・解除済累計
        self.treated_summary_json = {"date": "", "data": []}
        # 発症日
        self.onset_summary_json = {"date": "", "data": []}
        self.onset_open_data_json = {"date": "", "data": []}
        # 最終更新
        jst = timezone(timedelta(hours=9), 'JST')
        self.lastUpdate_json = datetime.today().astimezone(jst).strftime(
            "%Y/%m/%d %H:%M"
        )
        # 検査陽性者の状況
        self.main_summary_json = {
            "attr": "検査実施人数", "value": 0,
            "children": [
                {"attr": "陽性患者数", "value": 0,
                    "children": [
                        {"attr": "入院／入院調整中", "value": 0,
                            "children": [
                                {"attr": "軽症・中等症", "value": 0},
                                {"attr": "重症", "value": 0}
                            ]},
                        {"attr": "退院", "value": 0},
                        {"attr": "死亡", "value": 0},
                        {"attr": "自宅療養", "value": 0},
                        {"attr": "宿泊療養", "value": 0},
                        {"attr": "療養等調整中", "value": 0},
                        {"attr": "入院調整中", "value": 0,
                            "children": [
                                {"attr": "入院待機中", "value": 0},
                                {"attr": "入院もしくは療養方法の調整中", "value": 0}
                            ]},
                        {"attr": "府外健康観察", "value": 0}
                    ]}
            ]
        }
        # 更新日
        self.update_json = ''
        self.update_onset_json = ''

    def get_kintone_records(self, app_id, query):
        # kintoneから一覧取得
        headers = {
            self.token_param: os.environ[self.token_env + app_id]
            }
        url = self.url_records + 'app=' + app_id
        if query != '':
            query_quote = urllib.parse.quote(query + ' limit 500')
            url += '&query=' + query_quote

        records = requests.get(url, cert=self.cert_txt, headers=headers).json()

        cnt = len(records['records'])
        offset = 0
        while cnt == 500:
            offset += 500
            url = self.url_records + 'app=' + app_id
            query_quote = urllib.parse.quote(
                query + ' limit 500 offset ' + str(offset)
            )
            url += '&query=' + query_quote
            tmp_records = requests.get(
                url, cert=self.cert_txt, headers=headers
            ).json()
            cnt = len(tmp_records['records'])
            for record in tmp_records['records']:
                records['records'].append(record)

        return records

    def get_data(self):
        print("処理開始")
        print("クライアント証明書作成START")
        # クライアント証明書作成
        client = os.environ['CLIENT']
        clientList = client.split('\\n')
        tmp = "\n".join(clientList)
        with open(self.cert_txt, 'w') as f:
            f.writelines(tmp)

        print("更新日付の取得START")
        # 「更新日付」の取得
        records = self.get_kintone_records('825', '')
        for record in records['records']:
            d_date = datetime.strptime(record['日付']['value'], "%Y-%m-%d")
            self.update_json = d_date.strftime('%Y/%m/%d') + ' 00:00'

        print("更新日付（発症日）の取得START")
        # 「更新日付」の取得
        records = self.get_kintone_records('1166', '')
        for record in records['records']:
            h_date = datetime.strptime(record['日付']['value'], "%Y-%m-%d")
            self.update_onset_json = h_date.strftime('%Y/%m/%d') + ' 00:00'

        print("陽性者の取得START")
        # 「陽性者」の取得
        self.patients_json["date"] = self.update_json
        self.patients_open_data_json["date"] = self.update_json
        records = self.get_kintone_records('818', 'order by 番号 asc')
        for record in records['records']:
            data = {}
            data["No"] = int(record['番号']['value'])
            data["リリース日"] = record['報道提供日']['value'] + 'T08:00:00.000Z'
            d_date = datetime.strptime(record['報道提供日']['value'], "%Y-%m-%d")
            data["曜日"] = int(self.Excel_date(d_date))
            data["居住地"] = record['居住地']['value']
            data["年代"] = str(record['年代']['value']) + (
                "代" if any(
                    x in record['年代']['value'] for x in ("0")
                ) else ""
            )
            data["性別"] = record['性別']['value']
            data["退院"] = "○" if any(
                    x in record['退院']['value'] for x in ("退院", "解除")
                ) else ""
            data["date"] = record['報道提供日']['value']
            self.patients_json["data"].append(data)
            # オープンデータ用
            data = {}
            data["番号"] = int(record['番号']['value'])
            data["報道提供日"] = record['報道提供日']['value']
            data["年代"] = record['年代']['value']
            data["性別"] = record['性別']['value']
            data["居住地"] = record['居住地']['value']
            data["退院・解除"] = "○" if any(
                    x in record['退院']['value'] for x in ("退院", "解除")
                ) else ""
            self.patients_open_data_json["data"].append(data)

        print("検査件数等の取得START")
        # 「検査件数等」の取得
        self.patients_summary_json["date"] = self.update_json
        self.inspections_summary_json["date"] = self.update_json
        self.transmission_route_json["date"] = self.update_json
        self.treated_summary_json["date"] = self.update_json
        self.summary_open_data_json["date"] = self.update_json
        records = self.get_kintone_records('821', 'order by 日付 asc')
        treated_total = 0
        patients_total = 0
        for record in records['records']:
            # 陽性者数
            data_patients = {}
            data_patients['日付'] = record['日付']['value'] + 'T08:00:00.000Z'
            data_patients['小計'] = int(record['陽性人数']['value'])
            self.patients_summary_json['data'].append(data_patients)
            # 検査実施件数
            data_inspections = {}
            data_inspections['日付'] = record['日付']['value'] + 'T08:00:00.000Z'
            data_inspections['小計'] = int(record['検査件数']['value'])
            self.inspections_summary_json['data'].append(data_inspections)
            # 感染経路不明者（リンク不明者）
            self.transmission_route_json['data']['感染経路不明者'].append(
                int(record['リンク不明者']['value'])
            )
            self.transmission_route_json['data']['感染経路明確者'].append(
                int(record['陽性人数']['value']) - int(record['リンク不明者']['value'])
            )
            d_date = datetime.strptime(record['日付']['value'], "%Y-%m-%d")
            self.transmission_route_json['labels'].append(
                f'{d_date.month}/{d_date.day}'
            )
            # 退院・解除済累計
            data_treated = {}
            data_treated['日付'] = record['日付']['value'] + 'T08:00:00.000Z'
            data_treated['小計'] = int(record['退院判明']['value'])
            self.treated_summary_json['data'].append(data_treated)
            # 検査実施人数
            treated_total += int(record['検査件数']['value'])
            # 陽性者数
            patients_total += int(record['陽性人数']['value'])
            # オープンデータ用
            data = {}
            data['日付'] = record['日付']['value']
            data['検査件数'] = int(record['検査件数']['value'])
            data['陽性人数'] = int(record['陽性人数']['value'])
            data['陽性累計'] = int(record['陽性累計']['value'])
            data['現在陽性者数'] = int(record['現在陽性者数']['value'])
            data['退院'] = int(record['退院']['value'])
            data['退院済累計'] = int(record['退院済累計']['value'])
            data['退院判明'] = int(record['退院判明']['value'])
            data['退院判明累計'] = int(record['退院判明累計']['value'])
            data['死亡'] = int(record['死亡']['value'])
            data['リンク不明者'] = int(record['リンク不明者']['value'])
            self.summary_open_data_json["data"].append(data)

        # 検査実施人数、陽性患者数
        self.main_summary_json["value"] = treated_total
        self.main_summary_json["children"][0]["value"] = patients_total

        print("府民向け相談窓口への相談件数の取得START")
        # 「府民向け相談窓口への相談件数」の取得
        records = self.get_kintone_records('822', 'order by 日付 asc')
        for record in records['records']:
            data = {}
            data['日付'] = record['日付']['value'] + 'T08:00:00.000Z'
            data['小計'] = int(record['相談件数']['value'])
            self.contacts1_summary_json['data'].append(data)
            d_date = datetime.strptime(record['日付']['value'], "%Y-%m-%d")
            self.contacts1_summary_json["date"] = d_date.strftime('%Y/%m/%d') + ' 00:00'
            # オープンデータ用
            data = {}
            data['日付'] = record['日付']['value']
            data['相談件数'] = int(record['相談件数']['value'])
            self.contacts1_open_data_json['data'].append(data)
            self.contacts1_open_data_json["date"] = record['日付']['value']

        print("新型コロナ受診相談センターへの相談件数START")
        # 「新型コロナ受診相談センターへの相談件数」の取得
        records = self.get_kintone_records('823', 'order by 日付 asc')
        for record in records['records']:
            self.contacts2_summary_json['data']['府管轄保健所'].append(
                int(record['府管轄保健所']['value'])
            )
            self.contacts2_summary_json['data']['政令中核市保健所'].append(
                int(record['政令中核市']['value'])
            )
            d_date = datetime.strptime(record['日付']['value'], "%Y-%m-%d")
            self.contacts2_summary_json['labels'].append(
                f'{d_date.month}/{d_date.day}'
            )
            d_date = datetime.strptime(record['日付']['value'], "%Y-%m-%d")
            self.contacts2_summary_json["date"] = d_date.strftime('%Y/%m/%d') + ' 00:00'
            # オープンデータ用
            data = {}
            data['日付'] = record['日付']['value']
            data['府管轄保健所'] = int(record['府管轄保健所']['value'])
            data['政令中核市'] = int(record['政令中核市']['value'])
            self.contacts2_open_data_json['data'].append(data)
            self.contacts2_open_data_json["date"] = record['日付']['value']

        print("検査陽性者の状況の取得START")
        # 「検査陽性者の状況」取得
        # 「症状」の取得
        records = self.get_kintone_records('816', '')
        for record in records['records']:
            # 軽症・中等症
            self.main_summary_json["children"][0]["children"][0]["children"][0]["value"] = (
                int(record['軽症']['value']) + int(record['無症状']['value'])
            )
            # 重症
            self.main_summary_json["children"][0]["children"][0]["children"][1]["value"] = \
                int(record['重症']['value'])
            # 退院
            self.main_summary_json["children"][0]["children"][1]["value"] = \
                int(record['退院']['value'])
            # 死亡
            self.main_summary_json["children"][0]["children"][2]["value"] = \
                int(record['死亡']['value'])

        print("入退院の状況の取得START")
        # 「入退院の状況」の取得
        records = self.get_kintone_records('819', '')
        for record in records['records']:
            # 入院／入院調整中
            self.main_summary_json["children"][0]["children"][0]["value"] = (
                int(record['入院中']['value'])
            )
            # 入院調整中
            self.main_summary_json["children"][0]["children"][6]["value"] = (
                int(record['入院待機中']['value']) +
                int(record['入院もしくは療養方法の調整中']['value'])
            )
            # 入院待機中
            self.main_summary_json["children"][0]["children"][6]["children"][0]["value"] = \
                int(record['入院待機中']['value'])
            # 入院もしくは療養方法の調整中
            self.main_summary_json["children"][0]["children"][6]["children"][1]["value"] = \
                int(record['入院もしくは療養方法の調整中']['value'])
            # 自宅療養
            self.main_summary_json["children"][0]["children"][3]["value"] = \
                int(record['自宅療養']['value'])
            # 宿泊療養
            self.main_summary_json["children"][0]["children"][4]["value"] = \
                int(record['宿泊療養']['value'])
            # 療養等調整中
            self.main_summary_json["children"][0]["children"][5]["value"] = \
                int(record['療養等調整中']['value'])
            # 府外健康観察
            self.main_summary_json["children"][0]["children"][7]["value"] = \
                int(record['府外健康観察']['value'])

        print("発症日の取得START")
        # 「発症日」の取得
        # 〜〜〜時点は「更新日付（発症日）」アプリの日付 - 1日とする
        self.onset_summary_json["date"] = self.update_onset_json
        self.onset_open_data_json["date"] = h_date.strftime('%Y-%m-%d')
        records = self.get_kintone_records('1161', 'order by 発症日 asc')
        for record in records['records']:
            data = {}
            g_date = datetime.strptime(record['発症日']['value'], "%Y-%m-%d")
            data['日付'] = g_date.strftime('%Y-%m-%d') + 'T08:00:00.000Z'
            data['小計'] = int(record['人数']['value'])
            self.onset_summary_json['data'].append(data)
            # オープンデータ用
            data = {}
            data['発症日'] = g_date.strftime('%Y-%m-%d')
            data['人数'] = int(record['人数']['value'])
            self.onset_open_data_json['data'].append(data)

        print("jsonまとめSTART")
        # jsonまとめ
        # まずは1個前の状態にする
        self.data_json = copy.copy(self.current_data_json)
        if self.patients_json['date'] != self.current_data_json['patients']['date']:
            # 更新日付が異なる場合
            print("「更新日時」変更あり")
            self.data_json['patients'] = self.patients_json
            self.data_json['patients_summary'] = self.patients_summary_json
            self.data_json['inspections_summary'] = self.inspections_summary_json
            self.data_json['contacts1_summary'] = self.contacts1_summary_json
            self.data_json['contacts2_summary'] = self.contacts2_summary_json
            self.data_json['transmission_route_summary'] = self.transmission_route_json
            self.data_json['treated_summary'] = self.treated_summary_json
            self.data_json['lastUpdate'] = self.lastUpdate_json
            self.data_json['main_summary'] = self.main_summary_json
            self.data_json['patients_open'] = self.patients_open_data_json
            self.data_json['summary_open'] = self.summary_open_data_json
            self.data_json['contacts1_open'] = self.contacts1_open_data_json
            self.data_json['contacts2_open'] = self.contacts2_open_data_json

        if self.onset_summary_json['date'] != self.current_data_json['onset_summary']['date']:
            print("「更新日時（発症日）」変更あり")
            self.data_json['onset_summary'] = self.onset_summary_json
            self.data_json['lastUpdate'] = self.lastUpdate_json
            self.data_json['onset_open'] = self.onset_open_data_json

        if self.data_json['lastUpdate'] == self.current_data_json['lastUpdate']:
            print("変更なし")

        os.remove(self.cert_txt)
        return self.data_json

    def dumps_json(self, file_name: str, json_data: Dict) -> None:
        with codecs.open("./data/" + file_name, "w", "utf-8") as f:
            f.write(
                dumps(
                    json_data,
                    ensure_ascii=False,
                    indent=4,
                    separators=(',', ': ')
                )
            )

    def dumps_open_json(self, file_name: str, json_data: Dict) -> None:
        df = pd.DataFrame(json_data['data'])
        df.to_csv("./static/data/" + file_name, encoding='shift-jis', index=False)

    def Excel_date(self, date1):
        temp = datetime(1899, 12, 30)
        delta = date1 - temp
        return float(delta.days) + (float(delta.seconds) / 86400)

    def get_json(self, file_name: str) -> Dict:
        with codecs.open("./data/" + file_name, "r", "utf-8") as f:
            return load(f)


if __name__ == "__main__":
    data = DataJson().get_data()
    if 'patients_open' in data:
        patients_open_data = data.pop('patients_open')
        DataJson().dumps_open_json('patients.csv', patients_open_data)

    if 'summary_open' in data:
        summary_open_data = data.pop('summary_open')
        DataJson().dumps_open_json('summary.csv', summary_open_data)

    if 'contacts1_open' in data:
        contacts1_open_data = data.pop('contacts1_open')
        DataJson().dumps_open_json('contacts1.csv', contacts1_open_data)

    if 'contacts2_open' in data:
        contacts2_open_data = data.pop('contacts2_open')
        DataJson().dumps_open_json('contacts2.csv', contacts2_open_data)

    if 'onset_open' in data:
        contacts2_open_data = data.pop('onset_open')
        DataJson().dumps_open_json('onset.csv', contacts2_open_data)

    DataJson().dumps_json('data.json', data)
