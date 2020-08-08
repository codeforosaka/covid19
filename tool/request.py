import codecs
import os
import requests
import urllib.parse
from json import dumps
from typing import Dict
from datetime import datetime, timezone, timedelta


class DataJson:
    def __init__(self):
        self.cert_txt = './tool/client.txt'
        self.token_param = 'X-Cybozu-API-Token'
        self.token_env = 'KINTONE_API_TOKEN_'
        self.url_records = 'https://pref-osaka.s.cybozu.com/k/v1/records.json?'
        # 全データ込
        self.data_json = {}
        # 陽性者の属性
        self.patients_json = {"date": "", "data": []}
        # 陽性者数
        self.patients_summary_json = {"date": "", "data": []}
        # 検査実施件数
        self.inspections_summary_json = {"date": "", "data": []}
        # 府民向け相談窓口への相談件数
        self.contacts1_summary_json = {"date": "", "data": []}
        # 新型コロナ受診相談センターへの相談件数
        self.contacts2_summary_json = {
            "date": "", "data": {"府管轄保健所": [], "政令中核市保健所": []}, "labels": []
        }
        # 感染経路不明者（リンク不明者）
        self.transmission_route_json = {
            "date": "", "data": {"感染経路不明者": [], "感染経路明確者": []}, "labels": []
        }
        # 退院・解除済累計
        self.treated_summary_json = {"date": "", "data": []}
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
        print(records)

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
        # 「更新日付」の取得
        records = self.get_kintone_records('825', '')
        for record in records['records']:
            d_date = datetime.strptime(record['日付']['value'], "%Y-%m-%d")
            self.update_json = d_date.strftime('%Y/%m/%d') + ' 00:00'

        # 「陽性者」の取得
        self.patients_json["date"] = self.update_json
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

        # 「検査件数等」の取得
        self.patients_summary_json["date"] = self.update_json
        self.inspections_summary_json["date"] = self.update_json
        self.transmission_route_json["date"] = self.update_json
        self.treated_summary_json["date"] = self.update_json
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

        # 検査実施人数、陽性患者数
        self.main_summary_json["value"] = treated_total
        self.main_summary_json["children"][0]["value"] = patients_total

        # 「府民向け相談窓口への相談件数」の取得
        self.contacts1_summary_json["date"] = self.update_json
        records = self.get_kintone_records('822', 'order by 日付 asc')
        for record in records['records']:
            data = {}
            data['日付'] = record['日付']['value'] + 'T08:00:00.000Z'
            data['小計'] = int(record['相談件数']['value'])
            self.contacts1_summary_json['data'].append(data)

        # 「新型コロナ受診相談センターへの相談件数」の取得
        self.contacts2_summary_json["date"] = self.update_json
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

        # 「療養の状況」の取得
        records = self.get_kintone_records('820', '')
        for record in records['records']:
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

        # jsonまとめ
        self.data_json = {
            "patients": self.patients_json,
            "patients_summary": self.patients_summary_json,
            "inspections_summary": self.inspections_summary_json,
            "contacts1_summary": self.contacts1_summary_json,
            "contacts2_summary": self.contacts2_summary_json,
            "transmission_route_summary": self.transmission_route_json,
            "treated_summary": self.treated_summary_json,
            "lastUpdate": self.lastUpdate_json,
            "main_summary": self.main_summary_json
        }
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

    def Excel_date(self, date1):
        temp = datetime(1899, 12, 30)
        delta = date1 - temp
        return float(delta.days) + (float(delta.seconds) / 86400)


if __name__ == "__main__":
    DataJson().dumps_json('data.json', DataJson().get_data())
