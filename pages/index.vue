<template>
  <div class="MainPage">
    <page-header
      :icon="headerItem.icon"
      :title="headerItem.title"
      :date="headerItem.date"
    />
    <whats-new class="mb-4" :items="newsItems" />
    <static-info
      class="mb-4"
      :url="'http://www.pref.osaka.lg.jp/iryo/osakakansensho/corona-denwa.html'"
      :text="'自分や家族の症状に不安や心配があればまずは電話相談をどうぞ'"
    />
    <v-row class="DataBlock">
      <v-col cols="12" md="6" class="DataCard">
        <svg-card
          title="検査陽性者の状況"
          :title-id="'details-of-confirmed-cases'"
          :date="Data.inspections_summary.date"
        >
          <confirmed-cases-table v-bind="confirmedCases" />
        </svg-card>
      </v-col>
      <v-col cols="12" md="6" class="DataCard">
        <time-bar-chart
          title="陽性者数"
          :title-id="'number-of-confirmed-cases'"
          :chart-id="'time-bar-chart-patients'"
          :chart-data="patientsGraph"
          :date="Data.patients.date"
          :unit="'人'"
        />
      </v-col>
      <v-col cols="12" md="6" class="DataCard">
        <data-table
          :title="'陽性者の属性'"
          :title-id="'attributes-of-confirmed-cases'"
          :chart-data="patientsTable"
          :chart-option="{}"
          :date="Data.patients.date"
          :info="sumInfoOfPatients"
        />
      </v-col>
      <v-col cols="12" md="6" class="DataCard">
        <time-bar-chart
          title="陰性確認済（退院者累計）"
          :title-id="'number-of-treated'"
          :chart-id="'time-bar-chart-inspections'"
          :chart-data="treatedGraph"
          :date="Data.treated_summary.date"
          :note="'（注）退院者とは新型コロナウイルス感染症が治癒した者'"
          :unit="'人'"
        />
      </v-col>
      <v-col cols="12" md="6" class="DataCard">
        <time-bar-chart
          title="検査実施件数"
          :title-id="'number-of-tested'"
          :chart-id="'time-bar-chart-inspections'"
          :chart-data="inspectionsGraph"
          :date="Data.inspections_summary.date"
          :unit="'件'"
        />
      </v-col>
      <v-col cols="12" md="6" class="DataCard">
        <time-stacked-bar-chart
          title="新型コロナ受診相談センターへの相談件数"
          :title-id="'number-of-contacts２'"
          :chart-id="'time-stacked-bar-chart-inspections'"
          :chart-data="contacts2Graph"
          :date="Data.contacts2_summary.date"
          :items="contacts2Items"
          :labels="contacts2Labels"
          :unit="'件'"
        />
      </v-col>
      <v-col cols="12" md="6" class="DataCard">
        <time-bar-chart
          title="府民向け相談窓口への相談件数"
          :title-id="'number-of-contacts1'"
          :chart-id="'time-bar-chart-inspections'"
          :chart-data="contactsGraph"
          :date="Data.contacts1_summary.date"
          :unit="'件'"
        />
      </v-col>
      <v-col cols="12" md="6" class="DataCard">
        <time-stacked-bar-chart
          title="年代別陽性者数"
          :title-id="'number-of-ages'"
          :chart-id="'time-stacked-bar-chart-inspections2'"
          :chart-data="agesData.data"
          :date="Data.patients.date"
          :items="agesData.items"
          :labels="agesData.labels"
          :unit="'人'"
        />
      </v-col>
    </v-row>
  </div>
</template>

<script>
import PageHeader from '@/components/PageHeader.vue'
import TimeBarChart from '@/components/TimeBarChart.vue'
import TimeStackedBarChart from '@/components/TimeStackedBarChart.vue'
import WhatsNew from '@/components/WhatsNew.vue'
import StaticInfo from '@/components/StaticInfo.vue'
import Data from '@/data/data.json'
import DataTable from '@/components/DataTable.vue'
import formatGraph from '@/utils/formatGraph'
import formatTable from '@/utils/formatTable'
import formatConfirmedCases from '@/utils/formatConfirmedCases'
import News from '@/data/news.json'
import SvgCard from '@/components/SvgCard.vue'
import ConfirmedCasesTable from '@/components/ConfirmedCasesTable.vue'

export default {
  components: {
    PageHeader,
    TimeBarChart,
    WhatsNew,
    StaticInfo,
    DataTable,
    SvgCard,
    ConfirmedCasesTable,
    TimeStackedBarChart
  },
  data() {
    // 感染者数グラフ
    const patientsGraph = formatGraph(Data.patients_summary.data)
    // 感染者数
    const patientsTable = formatTable(Data.patients.data)
    // 検査実施状況
    const inspectionsGraph = formatGraph(Data.inspections_summary.data)
    // 検査陽性者の状況
    const confirmedCases = formatConfirmedCases(Data.main_summary)
    // 府民向け相談窓口相談件数
    const contactsGraph = formatGraph(Data.contacts1_summary.data)
    // 新型コロナ受診相談センターへの相談件数
    const contacts2Graph = [
      Data.contacts2_summary.data['府管轄保健所'],
      Data.contacts2_summary.data['政令中核市保健所']
    ]
    const contacts2Items = ['府管轄保健所', '政令中核市保健所']
    const contacts2Labels = Data.contacts2_summary.labels
    // 治療終了者数
    const treatedGraph = formatGraph(Data.treated_summary.data)

    const sumInfoOfPatients = {
      lText: patientsGraph[
        patientsGraph.length - 1
      ].cumulative.toLocaleString(),
      sText: patientsGraph[patientsGraph.length - 1].label + 'の累計',
      unit: '人'
    }

    const data = {
      Data,
      patientsTable,
      patientsGraph,
      inspectionsGraph,
      confirmedCases,
      contactsGraph,
      contacts2Graph,
      contacts2Items,
      contacts2Labels,
      treatedGraph,
      sumInfoOfPatients,
      headerItem: {
        icon: 'mdi-chart-timeline-variant',
        title: '大阪府の最新感染動向',
        date: Data.lastUpdate
      },
      newsItems: News.newsItems
    }
    return data
  },
  computed: {
    agesData() {
      const ageData = {
        labels: [],
        items: [
          '未就学児',
          '10代',
          '20代',
          '30代',
          '40代',
          '50代',
          '60代',
          '70代',
          '80代',
          '90代'
        ],
        data: [[], [], [], [], [], [], [], [], [], []]
      }

      const data = {}
      let lastDate = new Date()
      for (const i in Data.patients.data) {
        // eslint-disable-next-line no-prototype-builtins
        if (Data.patients.data.hasOwnProperty(i) === false) {
          continue
        }
        const row = Data.patients.data[i]
        let hash = {}
        if (data[row.date] === undefined) {
          hash['未就学児'] = 0
          hash['10代'] = 0
          hash['20代'] = 0
          hash['30代'] = 0
          hash['40代'] = 0
          hash['50代'] = 0
          hash['60代'] = 0
          hash['70代'] = 0
          hash['80代'] = 0
          hash['90代'] = 0
        } else {
          hash = data[row.date]
        }
        hash[row['年代']] += 1
        data[row.date] = hash
        lastDate = new Date(row.date)
      }
      const dt = new Date(2020, 0, 28, 0, 0, 0)
      lastDate.setHours(0, 0, 0)
      while (dt.getTime() < lastDate.getTime()) {
        dt.setDate(dt.getDate() + 1)
        const year = String(dt.getFullYear())
        const month = String(dt.getMonth() + 1)
        const day = String(dt.getDate())
        const thisDate =
          year + '-' + month.padStart(2, '0') + '-' + day.padStart(2, '0')
        let target = {}
        target['未就学児'] = 0
        target['10代'] = 0
        target['20代'] = 0
        target['30代'] = 0
        target['40代'] = 0
        target['50代'] = 0
        target['60代'] = 0
        target['70代'] = 0
        target['80代'] = 0
        target['90代'] = 0
        if (data[thisDate] !== undefined) {
          target = data[thisDate]
        }
        ageData.labels.push(month + '/' + day)
        ageData.data[0].push(target['未就学児'])
        ageData.data[1].push(target['10代'])
        ageData.data[2].push(target['20代'])
        ageData.data[3].push(target['30代'])
        ageData.data[4].push(target['40代'])
        ageData.data[5].push(target['50代'])
        ageData.data[6].push(target['60代'])
        ageData.data[7].push(target['70代'])
        ageData.data[8].push(target['80代'])
        ageData.data[9].push(target['90代'])
      }
      return ageData
    }
  },
  head() {
    return {
      title: '大阪府の最新感染動向'
    }
  }
}
</script>

<style lang="scss" scoped>
.MainPage {
  .DataBlock {
    margin: 20px -8px;
    .DataCard {
      @include largerThan($medium) {
        padding: 10px;
      }
      @include lessThan($small) {
        padding: 4px 8px;
      }
    }
  }
}
</style>
