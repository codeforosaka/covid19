<template>
  <data-view :title="title" :title-id="titleId" :date="date" :url="url">
    <ul
      :class="$style.GraphLegend"
      :style="{ display: canvas ? 'block' : 'none' }"
    >
      <li v-for="(item, i) in items" :key="i" @click="onClickLegend(i)">
        <button>
          <div
            v-if="i === 2"
            :style="{
              backgroundColor: colors[i][0],
              border: 0,
              height: '3px'
            }"
          />
          <div
            v-else
            :style="{
              backgroundColor: colors[i][0],
              borderColor: colors[i][1]
            }"
          />
          <span
            :style="{
              textDecoration: displayLegends[i] ? 'none' : 'line-through'
            }"
            >{{ item }}</span
          >
        </button>
      </li>
    </ul>
    <scrollable-chart v-show="canvas" :display-data="displayData">
      <template v-slot:chart="{ chartWidth }">
        <bar
          :ref="'barChart'"
          :chart-id="chartId"
          :chart-data="displayData"
          :options="displayOption"
          :display-legends="displayLegends"
          :height="240"
          :width="chartWidth"
        />
      </template>
      <template v-slot:sticky-chart>
        <bar
          class="sticky-legend"
          :chart-id="`${chartId}-header-right`"
          :chart-data="displayDataHeader"
          :options="displayOptionHeader"
          :plugins="yAxesBgRightPlugin"
          :display-legends="displayLegends"
          :height="240"
        />
      </template>
    </scrollable-chart>
    <div class="note">
      {{ note }}
    </div>
    <template v-slot:infoPanel>
      <data-view-basic-info-panel
        :l-text="displayInfo.lText"
        :s-text-list="[displayInfo.sText]"
        :unit="displayInfo.unit"
      />
    </template>
    <template v-slot:footer>
      <open-data-link :url="url" />
    </template>
  </data-view>
</template>

<style>
.note {
  padding: 8px;
  font-size: 12px;
  color: #808080;
}
</style>

<script>
import dayjs from 'dayjs'
import DataView from '@/components/DataView.vue'
import DataViewBasicInfoPanel from '@/components/DataViewBasicInfoPanel.vue'
import OpenDataLink from '@/components/OpenDataLink.vue'
import ScrollableChart from '@/components/ScrollableChart.vue'
import { yAxesBgPlugin, yAxesBgRightPlugin } from '@/plugins/vue-chart'

export default {
  components: {
    DataView,
    DataViewBasicInfoPanel,
    ScrollableChart,
    OpenDataLink
  },
  props: {
    title: {
      type: String,
      required: false,
      default: ''
    },
    titleId: {
      type: String,
      required: false,
      default: ''
    },
    chartId: {
      type: String,
      required: false,
      default: 'rate-chart'
    },
    chartData: {
      type: Object,
      required: false,
      default: () => {}
    },
    date: {
      type: String,
      required: true,
      default: ''
    },
    items: {
      type: Array,
      required: false,
      default: () => []
    },
    unit: {
      type: String,
      required: false,
      default: ''
    },
    unit2: {
      type: String,
      required: false,
      default: ''
    },
    note: {
      type: String,
      required: false,
      default: ''
    },
    url: {
      type: String,
      required: false,
      default: ''
    },
    yAxesBgPlugin: {
      type: Array,
      default: () => yAxesBgPlugin
    },
    yAxesBgRightPlugin: {
      type: Array,
      default: () => yAxesBgRightPlugin
    }
  },
  data() {
    return {
      displayLegends: [true, true, true],
      colors: [
        ['#C4D6ED', '#6F96CD'],
        ['#4071E0', '#4071E0'],
        ['#4B5469', '#4B5469']
      ],
      canvas: true
    }
  },
  computed: {
    displayInfo() {
      const diff =
        this.chartData.rateList[this.chartData.rateList.length - 1] -
        this.chartData.rateList[this.chartData.rateList.length - 2]

      let stext = ''
      if (diff < 0) {
        stext = diff.toLocaleString() + '%'
      } else {
        stext = '+' + diff.toLocaleString() + '%'
      }
      return {
        lText: this.chartData.rateList[
          this.chartData.rateList.length - 1
        ].toLocaleString(),
        sText: `（${this.$t('前日比')}：` + stext + '）',
        unit: '%'
      }
    },
    displayData() {
      return {
        labels: this.chartData.dateList,
        datasets: [
          {
            type: 'line',
            yAxisID: 'y-axis-1',
            label: 'test1',
            data: this.chartData.denomList,
            pointBackgroundColor: 'rgba(0,0,0,0)',
            pointBorderColor: 'rgba(0,0,0,0)',
            borderColor: '#6F96CD',
            backgroundColor: '#C4D6ED',
            borderWidth: 2,
            fill: true,
            order: 2,
            lineTension: 0
          },
          {
            type: 'bar',
            yAxisID: 'y-axis-1',
            label: 'test2',
            data: this.chartData.numerList,
            backgroundColor: '#4071E0',
            order: 3
          },
          {
            type: 'line',
            yAxisID: 'y-axis-2',
            label: 'test3',
            data: this.chartData.rateList,
            pointBackgroundColor: 'rgba(0,0,0,0)',
            pointBorderColor: 'rgba(0,0,0,0)',
            borderColor: '#4B5469',
            borderWidth: 2,
            fill: false,
            order: 1,
            lineTension: 0
          }
        ]
      }
    },
    displayOption() {
      const unit = this.unit
      const unit2 = this.unit2
      const scaledTicksYAxisMax = this.scaledTicksYAxisMax
      const scaledTicksYAxisMaxRight = this.scaledTicksYAxisMaxRight
      const options = {
        tooltips: {
          displayColors: false,
          callbacks: {
            label(tooltipItem) {
              let labelText = ''
              if (tooltipItem.datasetIndex === 2) {
                labelText = tooltipItem.value.toLocaleString() + '%'
              } else if (tooltipItem.datasetIndex === 0) {
                labelText = parseInt(tooltipItem.value).toLocaleString() + unit2
              } else {
                labelText = parseInt(tooltipItem.value).toLocaleString() + unit
              }
              return labelText
            }
          }
        },
        maintainAspectRatio: false,
        legend: {
          display: false
        },
        scales: {
          xAxes: [
            {
              id: 'day',
              stacked: true,
              gridLines: {
                display: false
              },
              ticks: {
                fontSize: 9,
                maxTicksLimit: 20,
                fontColor: '#808080',
                maxRotation: 0,
                callback: label => {
                  return dayjs(label).format('D')
                }
              }
              // #2384: If you set "type" to "time", make sure that the bars at both ends are not hidden.
              // #2384: typeをtimeに設定する時はグラフの両端が見切れないか確認してください
            },
            {
              id: 'month',
              stacked: true,
              gridLines: {
                drawOnChartArea: false,
                drawTicks: true,
                drawBorder: false,
                tickMarkLength: 10
              },
              ticks: {
                fontSize: 11,
                fontColor: '#808080',
                padding: 3,
                fontStyle: 'bold'
              },
              type: 'time',
              time: {
                unit: 'month',
                displayFormats: {
                  month: 'MMM'
                }
              }
            }
          ],
          yAxes: [
            {
              id: 'y-axis-1',
              position: 'left',
              stacked: true,
              gridLines: {
                display: true,
                drawOnChartArea: true,
                color: '#E5E5E5'
              },
              ticks: {
                maxTicksLimit: 8,
                fontColor: '#808080',
                suggestedMin: 0,
                suggestedMax: scaledTicksYAxisMax
              }
            },
            {
              id: 'y-axis-2',
              position: 'right',
              gridLines: {
                display: true,
                drawOnChartArea: false,
                color: '#E5E5E5'
              },
              ticks: {
                maxTicksLimit: 8,
                fontColor: '#808080',
                suggestedMin: 0,
                suggestedMax: scaledTicksYAxisMaxRight,
                callback: value => {
                  return `${value}%`
                }
              }
            }
          ]
        }
      }
      if (this.$route.query.ogp === 'true') {
        Object.assign(options, { animation: { duration: 0 } })
      }
      return options
    },
    displayDataHeader() {
      return {
        labels: ['2020-1-1'],
        datasets: [
          {
            data: [this.chartData.denomList[0]],
            backgroundColor: 'transparent',
            yAxisID: 'y-axis-1',
            borderWidth: 0
          },
          {
            data: [this.chartData.numerList[0]],
            backgroundColor: 'transparent',
            yAxisID: 'y-axis-1',
            borderWidth: 0
          },
          {
            data: [this.chartData.rateList[0]],
            backgroundColor: 'transparent',
            yAxisID: 'y-axis-2',
            borderWidth: 0
          }
        ]
      }
    },
    displayOptionHeader() {
      const scaledTicksYAxisMax = this.scaledTicksYAxisMax
      const scaledTicksYAxisMaxRight = this.scaledTicksYAxisMaxRight

      return {
        maintainAspectRatio: false,
        legend: { display: false },
        tooltips: { enabled: false },
        scales: {
          xAxes: [
            {
              id: 'day',
              stacked: true,
              gridLines: {
                display: false
              },
              ticks: {
                fontSize: 9,
                maxTicksLimit: 20,
                fontColor: 'transparent', // displayOption では '#808080'
                maxRotation: 0,
                callback: label => {
                  return dayjs(label).format('D')
                }
              }
            },
            {
              id: 'month',
              stacked: true,
              gridLines: {
                drawOnChartArea: false,
                drawTicks: false, // displayOption では true
                drawBorder: false,
                tickMarkLength: 10
              },
              ticks: {
                fontSize: 11,
                fontColor: 'transparent', // displayOption では '#808080'
                padding: 13, // 3 + 10(tickMarkLength)，displayOption では 3
                fontStyle: 'bold'
              },
              type: 'time',
              time: {
                unit: 'month',
                displayFormats: {
                  month: 'MMM'
                }
              }
            }
          ],
          yAxes: [
            {
              id: 'y-axis-1',
              position: 'left',
              stacked: true,
              gridLines: {
                display: true,
                drawOnChartArea: false, // displayOption では true
                color: '#E5E5E5'
              },
              ticks: {
                maxTicksLimit: 8,
                fontColor: '#808080',
                suggestedMin: 0,
                suggestedMax: scaledTicksYAxisMax
              }
            },
            {
              id: 'y-axis-2',
              position: 'right',
              gridLines: {
                display: true,
                drawOnChartArea: false,
                color: '#E5E5E5'
              },
              ticks: {
                maxTicksLimit: 8,
                fontColor: '#808080',
                suggestedMin: 0,
                suggestedMax: scaledTicksYAxisMaxRight,
                callback: value => {
                  return `${value}%`
                }
              }
            }
          ]
        },
        animation: { duration: 0 }
      }
    },
    scaledTicksYAxisMax() {
      return Math.max(...this.chartData.denomList)
    },
    scaledTicksYAxisMaxRight() {
      return Math.max(100, Math.max(...this.chartData.rateList))
    }
  },
  created() {
    this.canvas = process.browser
  },
  mounted() {
    const barChart = this.$refs.barChart
    const barElement = barChart.$el
    const canvas = barElement.querySelector('canvas')
    const labelledbyId = `${this.titleId}-graph`

    if (canvas) {
      canvas.setAttribute('role', 'img')
      canvas.setAttribute('aria-labelledby', labelledbyId)
    }
  },
  methods: {
    onClickLegend(i) {
      this.displayLegends[i] = !this.displayLegends[i]
      this.displayLegends = this.displayLegends.slice()
    }
  }
}
</script>

<style module lang="scss">
.note {
  padding: 8px;
  font-size: 12px;
  color: #808080;
}

.Graph {
  &Legend {
    text-align: center;
    list-style: none;
    padding: 0 !important;
    li {
      display: inline-block;
      margin: 0 3px;
      div {
        height: 12px;
        margin: 2px 4px;
        width: 40px;
        display: inline-block;
        vertical-align: middle;
        border-width: 1px;
        border-style: solid;
      }
      button {
        color: $gray-3;
        @include font-size(12);
      }
    }
  }
}
</style>
