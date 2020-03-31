from datetime import datetime, timedelta

import config
from util import MAIN_SUMMARY_INIT, excel_date, get_xlsx, jst, dumps_json

from typing import Dict


class DataJson:
    def __init__(self):
        # self.patients_file = get_xlsx(config.patients_xlsx, "patients.xlsx")
        self.patients_and_inspections_file = get_xlsx(
            config.patients_and_inspections_xlsx, "patients_and_inspections.xlsx"
        )
        # self.patients_sheet = self.patients_file["Sheet1"]
        # self.inspections_file = get_xlsx(config.inspections_xlsx, "inspections.xlsx")
        # self.inspections_sheet = self.inspections_file["モトデータ"]
        # self.main_summary_sheet = self.inspections_file["総括表"]
        self.patients_sheet = self.patients_and_inspections_file["【公開OK】府HP用(陽性者ベース)"]
        self.inspections_sheet = self.patients_and_inspections_file["【公開OK】コロナサイト用（日付ベース）"]
        self.main_summary_sheet = self.patients_and_inspections_file["【公開OK】ピポット集計"]
        self.contacts1_file = get_xlsx(config.contacts1_xlsx, "contacts1.xlsx")
        self.contacts1_sheet = self.contacts1_file["Sheet1"]
        self.contacts2_file = get_xlsx(config.contacts2_xlsx, "contacts2.xlsx")
        self.contacts2_sheet = self.contacts2_file["Sheet1"]
        self.patients_count = 3
        self.inspections_count = 3
        self.contacts1_count = 3
        self.contacts2_count = 4
        self._data_json = {}
        self._patients_json = {}
        self._patients_summary_json = {}
        self._inspections_summary_json = {}
        self._contacts1_summary_json = {}
        self._contacts2_summary_json = {}
        self._treated_summary_json = {}
        self._main_summary_json = {}
        self.last_update = datetime.today().astimezone(jst).strftime("%Y/%m/%d %H:%M")
        self.get_patients()
        self.get_inspections()
        self.get_contacts1()
        self.get_contacts2()

    def data_json(self):
        if not self._data_json:
            self.make_data()
        return self._data_json

    def patients_json(self) -> Dict:
        if not self._patients_json:
            self.make_patients()
        return self._patients_json

    def patients_summary_json(self) -> Dict:
        if not self._patients_summary_json:
            self.make_patients_summary()
        return self._patients_summary_json

    def inspections_summary_json(self) -> Dict:
        if not self._inspections_summary_json:
            self.make_inspections_summary()
        return self._inspections_summary_json

    def contacts1_summary_json(self) -> Dict:
        if not self._contacts1_summary_json:
            self.make_contacts1_summary()
        return self._contacts1_summary_json

    def contacts2_summary_json(self) -> Dict:
        if not self._contacts2_summary_json:
            self.make_contacts2_summary()
        return self._contacts2_summary_json

    def treated_summary_json(self) -> Dict:
        if not self._treated_summary_json:
            self.make_treated_summary()
        return self._treated_summary_json

    def main_summary_json(self) -> Dict:
        if not self._main_summary_json:
            self.make_main_summary()
        return self._main_summary_json

    def make_patients(self) -> None:
        self._patients_json = {
            "date": self.get_patients_last_update(),
            "data": []
        }
        for i in range(3, self.patients_count):
            data = {}
            release_date = excel_date(self.patients_sheet.cell(row=i, column=2).value)
            data["No"] = self.patients_sheet.cell(row=i, column=1).value
            data["リリース日"] = release_date.isoformat() + ".000Z"
            data["曜日"] = 43854
            data["居住地"] = self.patients_sheet.cell(row=i, column=5).value
            if self.patients_sheet.cell(row=i, column=5).value != "大阪府外":
                data["居住地"] = "大阪府" + data["居住地"]
            data["年代"] = str(self.patients_sheet.cell(row=i, column=3).value) + (
                "代" if isinstance(self.patients_sheet.cell(row=i, column=3).value, int) else ""
            )
            data["性別"] = self.patients_sheet.cell(row=i, column=4).value
            data["退院"] = "○" if "退院" in str(self.patients_sheet.cell(row=i, column=8).value) else ""
            data["date"] = release_date.strftime("%Y-%m-%d")
            self._patients_json["data"].append(data)

    def make_patients_summary(self) -> None:
        self._patients_summary_json = {
            "date": self.get_inspections_last_update(),
            "data": []
        }

        for i in range(3, self.inspections_count):
            data = {}
            date = excel_date(self.inspections_sheet.cell(row=i, column=1).value)
            data["日付"] = date.isoformat() + ".000Z"
            data["小計"] = self.inspections_sheet.cell(row=i, column=3).value
            self._patients_summary_json["data"].append(data)

    def make_inspections_summary(self) -> None:
        self._inspections_summary_json = {
            "date": self.get_inspections_last_update(),
            "data": []
        }
        for i in range(3, self.inspections_count):
            data = {}
            date = excel_date(self.inspections_sheet.cell(row=i, column=1).value)
            data["日付"] = date.isoformat() + ".000Z"
            data["小計"] = self.inspections_sheet.cell(row=i, column=2).value
            self._inspections_summary_json["data"].append(data)

    def make_contacts1_summary(self) -> None:
        self._contacts1_summary_json = {
            "date": self.get_contacts1_last_update(),
            "data": []
        }

        for i in range(3, self.contacts1_count):
            data = {}
            date = self.contacts1_sheet.cell(row=i, column=1).value + timedelta(hours=8)
            data["日付"] = date.isoformat() + ".000Z"
            data["小計"] = self.contacts1_sheet.cell(row=i, column=2).value
            self._contacts1_summary_json["data"].append(data)

    def make_contacts2_summary(self) -> None:
        self._contacts2_summary_json = {
            "date": self.get_contacts2_last_update(),
            "data": {
                "府管轄保健所": [],
                "政令中核市保健所": []
            },
            "labels": []
        }

        for i in range(4, self.contacts2_count):
            date = self.contacts2_sheet.cell(row=i, column=1).value
            self._contacts2_summary_json["data"]["府管轄保健所"].append(self.contacts2_sheet.cell(row=i, column=2).value)
            self._contacts2_summary_json["data"]["政令中核市保健所"].append(self.contacts2_sheet.cell(row=i, column=3).value)
            self._contacts2_summary_json["labels"].append(date.strftime("%m/%d"))

    def make_treated_summary(self) -> None:
        self._treated_summary_json = {
            "date": self.get_inspections_last_update(),
            "data": []
        }

        for i in range(3, self.inspections_count):
            data = {}
            date = excel_date(self.inspections_sheet.cell(row=i, column=1).value)
            data["日付"] = date.isoformat() + ".000Z"
            data["小計"] = self.inspections_sheet.cell(row=i, column=8).value
            self._treated_summary_json["data"].append(data)

    def make_main_summary(self) -> None:
        self._main_summary_json = MAIN_SUMMARY_INIT
        all_inspections = 0
        all_patients = 0
        all_discharges = 0
        for i in range(3, self.inspections_count):
            all_inspections += self.inspections_sheet.cell(row=i, column=2).value
            all_patients += self.inspections_sheet.cell(row=i, column=3).value
            all_discharges += self.inspections_sheet.cell(row=i, column=8).value
        self._main_summary_json["value"] = all_inspections
        self._main_summary_json["children"][0]["value"] = all_patients
        self._main_summary_json["children"][0]["children"][0]["value"] = (
            self.main_summary_sheet.cell(row=5, column=2).value + self.main_summary_sheet.cell(row=6, column=2).value
        )
        self._main_summary_json["children"][0]["children"][0]["children"][0]["value"] = (
            self.main_summary_sheet.cell(row=13, column=2).value +
            self.main_summary_sheet.cell(row=15, column=2).value
        )
        self._main_summary_json["children"][0]["children"][0]["children"][1]["value"] = \
            self.main_summary_sheet.cell(row=14, column=2).value
        self._main_summary_json["children"][0]["children"][1]["value"] = all_discharges
        self._main_summary_json["children"][0]["children"][2]["value"] = \
            self.main_summary_sheet.cell(row=16, column=2).value

    def make_data(self) -> None:
        self._data_json = {
            "patients": self.patients_json(),
            "patients_summary": self.patients_summary_json(),
            "inspections_summary": self.inspections_summary_json(),
            "contacts1_summary": self.contacts1_summary_json(),
            "contacts2_summary": self.contacts2_summary_json(),
            "treated_summary": self.treated_summary_json(),
            "lastUpdate": self.last_update,
            "main_summary": self.main_summary_json()
        }

    def get_patients_last_update(self) -> str:
        date = self.patients_sheet.cell(row=1, column=1).value
        return self.patients_sheet.cell(row=1, column=1).value.strftime("%Y/%m/%d %H:%M")

    def get_inspections_last_update(self) -> str:
        return self.inspections_sheet.cell(row=1, column=1).value.strftime("%Y/%m/%d %H:%M")

    def get_contacts1_last_update(self) -> str:
        return self.contacts1_sheet.cell(row=1, column=1).value.strftime("%Y/%m/%d %H:%M")

    def get_contacts2_last_update(self) -> str:
        return self.contacts2_sheet.cell(row=1, column=1).value.strftime("%Y/%m/%d %H:%M")

    def get_patients(self) -> None:
        while self.patients_sheet:
            self.patients_count += 1
            value = self.patients_sheet.cell(row=self.patients_count, column=1).value
            if not value:
                break

    def get_inspections(self) -> None:
        while self.inspections_sheet:
            self.inspections_count += 1
            value = self.inspections_sheet.cell(row=self.inspections_count, column=1).value
            if value == "計":
                break

    def get_contacts1(self) -> None:
        while self.contacts1_sheet:
            self.contacts1_count += 1
            value = self.contacts1_sheet.cell(row=self.contacts1_count, column=1).value
            if not value:
                break

    def get_contacts2(self) -> None:
        while self.contacts2_sheet:
            self.contacts2_count += 1
            value = self.contacts2_sheet.cell(row=self.contacts2_count, column=1).value
            if not value:
                break


if __name__ == '__main__':
    dumps_json("data.json", DataJson().data_json())
