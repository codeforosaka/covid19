<template>
  <data-view :title="title" :title-id="titleId" :date="date" :url="url">
    <scrollable-chart v-show="canvas" :display-data="displayData">
      <template v-slot:chart="{ chartWidth }">
        <bar
          :ref="'barChart'"
          :chart-id="chartId"
          :chart-data="displayData"
          :options="displayOption"
          :height="240"
          :width="chartWidth"
        />
      </template>
      <template v-slot:sticky-chart>
        <bar
          class="sticky-legend"
          :chart-id="`${chartId}-header`"
          :chart-data="displayDataHeader"
          :options="displayOptionHeader"
          :plugins="yAxesBgPlugin"
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
import { yAxesBgPlugin } from '@/plugins/vue-chart'

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
      default: 'no-cum-time-bar-chart'
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
    unit: {
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
    }
  },
  data() {
    return {
      canvas: true
    }
  },
  computed: {
    displayInfo() {
      const diff =
        this.chartData.valList[this.chartData.valList.length - 1] -
        this.chartData.valList[this.chartData.valList.length - 2]

      let stext = ''
      if (diff < 0) {
        stext = diff.toLocaleString() + this.unit
      } else {
        stext = '+' + diff.toLocaleString() + this.unit
      }
      return {
        lText: this.chartData.valList[
          this.chartData.valList.length - 1
        ].toLocaleString(),
        sText: '（前日比：' + stext + '）',
        unit: this.unit
      }
    },
    displayData() {
      return {
        labels: this.chartData.dateList,
        datasets: [
          {
            label: '直近1週間の人口10万人あたり新規陽性者数',
            data: this.chartData.valList,
            backgroundColor: '#2445b5',
            borderWidth: 0
          }
        ]
      }
    },
    displayOption() {
      const unit = this.unit
      const scaledTicksYAxisMax = this.scaledTicksYAxisMax
      const options = {
        tooltips: {
          displayColors: false,
          callbacks: {
            label(tooltipItem) {
              const labelText = `${tooltipItem.value.toLocaleString()} ${unit}`
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
              stacked: true,
              gridLines: {
                display: true,
                color: '#E5E5E5'
              },
              ticks: {
                suggestedMin: 0,
                maxTicksLimit: 8,
                fontColor: '#808080',
                suggestedMax: scaledTicksYAxisMax
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
            data: [Math.max(...this.chartData.valList)],
            backgroundColor: 'transparent',
            borderWidth: 0
          }
        ]
      }
    },
    displayOptionHeader() {
      return {
        maintainAspectRatio: false,
        legend: {
          display: false
        },
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
                fontColor: 'transparent',
                maxRotation: 0,
                minRotation: 0,
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
                drawTicks: false, // true -> false
                drawBorder: false,
                tickMarkLength: 10
              },
              ticks: {
                fontSize: 11,
                fontColor: 'transparent', // #808080
                padding: 13, // 3 + 10(tickMarkLength)
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
              stacked: true,
              gridLines: {
                display: true,
                drawOnChartArea: false,
                color: '#E5E5E5'
              },
              ticks: {
                suggestedMin: 0,
                maxTicksLimit: 8,
                fontColor: '#808080'
              }
            }
          ]
        },
        animation: { duration: 0 }
      }
    },
    scaledTicksYAxisMax() {
      return Math.max(...this.chartData.valList)
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
  methods: {}
}
</script>
