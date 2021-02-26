<template>
  <data-view :title="title" :title-id="titleId" :date="date" :url="url">
    <template v-slot:button>
      <data-selector v-model="dataKind" :target-id="chartId" />
    </template>
    <ul
      :class="$style.GraphLegend"
      :style="{ display: canvas ? 'block' : 'none' }"
    >
      <li v-for="(item, i) in items" :key="i" @click="onClickLegend(i)">
        <button>
          <div
            :style="{
              backgroundColor: colorArray[i]
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
          :chart-id="`${chartId}-header`"
          :chart-data="displayDataHeader"
          :options="displayOptionHeader"
          :plugins="yAxesBgPlugin"
          :display-legends="displayLegends"
          :height="240"
        />
      </template>
    </scrollable-chart>
    <div :class="$style.note">
      {{ $t('※報道提供における本日判明数での集計') }}
    </div>
    <template v-slot:infoPanel>
      <data-view-basic-info-panel
        :l-text="displayInfo.lText"
        :s-text-list="[displayInfo.sText1, displayInfo.sText2]"
        :unit="displayInfo.unit"
      />
    </template>
    <template v-slot:footer>
      <open-data-link :url="url" />
    </template>
  </data-view>
</template>

<script>
import dayjs from 'dayjs'
import DataView from '@/components/DataView.vue'
import DataSelector from '@/components/DataSelector.vue'
import DataViewBasicInfoPanel from '@/components/DataViewBasicInfoPanel.vue'
import OpenDataLink from '@/components/OpenDataLink.vue'
import ScrollableChart from '@/components/ScrollableChart.vue'
import { yAxesBgPlugin } from '@/plugins/vue-chart'

export default {
  components: {
    DataView,
    DataSelector,
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
      default: 'time-stacked-bar-chart-2'
    },
    chartData: {
      type: Array,
      required: false,
      default: () => []
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
    labels: {
      type: Array,
      required: false,
      default: () => []
    },
    unit: {
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
  data: () => ({
    dataKind: 'transition',
    displayLegends: [true, true],
    colorArray: ['#364c97', '#0076eb'],
    canvas: true,
    isSmall: false
  }),
  computed: {
    displayInfo() {
      if (this.dataKind === 'transition') {
        const lastArray = this.pickLastNumber(this.chartData)
        const lastlastArray = this.pickLastLastNumber(this.chartData)
        const lastNum = lastArray[0]
        const lastRatio = this.formatDayBeforeRatio(
          lastArray[0] - lastlastArray[0]
        )
        let lastPercent =
          Math.floor((lastNum / this.sum(lastArray)) * 100 * 10 ** 2) / 10 ** 2

        if (isNaN(lastPercent)) {
          lastPercent = 0
        }

        return {
          lText: lastNum.toLocaleString(),
          sText1: `${this.$t('リンク不明率：{rate} %', {
            rate: lastPercent.toLocaleString()
          })}`,
          sText2: `${this.$t('前日比：{dif}', {
            dif: lastRatio
          })}`,
          unit: this.unit
        }
      }
      const lastSumArray = this.cumulativeSum(this.chartData)
      const lastSumNum = lastSumArray[0]
      const lastSumPercent =
        Math.floor((lastSumNum / this.sum(lastSumArray)) * 100 * 10 ** 2) /
        10 ** 2
      const cumulativeData = this.chartData.map(item => {
        return this.cumulative(item)
      })
      const lastSumRatio = this.formatDayBeforeRatio(
        cumulativeData[0][cumulativeData[0].length - 1] -
          cumulativeData[0][cumulativeData[0].length - 2]
      )

      return {
        lText: lastSumNum.toLocaleString(),
        sText1: `${this.$t('リンク不明率：{rate} %', {
          rate: lastSumPercent.toLocaleString()
        })}`,
        sText2: `${this.$t('前日比：{dif}', {
          dif: lastSumRatio
        })}`,
        unit: this.unit
      }
    },
    displayData() {
      const colorArray = ['#364c97', '#0076eb']
      if (this.dataKind === 'transition') {
        return {
          labels: this.labels,
          datasets: this.chartData.map((item, index) => {
            return {
              label: this.items[index],
              data: item,
              backgroundColor: colorArray[index],
              borderWidth: 0
            }
          })
        }
      }
      return {
        labels: this.labels,
        datasets: this.chartData.map((item, index) => {
          return {
            label: this.items[index],
            data: this.cumulative(item),
            backgroundColor: colorArray[index],
            borderWidth: 0
          }
        })
      }
    },
    displayOption() {
      const unit = this.unit
      const sumArray = this.eachArraySum(this.chartData)
      const data = this.chartData
      const cumulativeData = this.chartData.map(item => {
        return this.cumulative(item)
      })
      const cumulativeSumArray = this.eachArraySum(cumulativeData)
      const options = {
        tooltips: {
          displayColors: false,
          callbacks: {
            label: tooltipItem => {
              const labelText =
                this.dataKind === 'transition'
                  ? `${sumArray[tooltipItem.index]}${unit}（${this.$t(
                      'リンク不明'
                    )}: ${data[0][tooltipItem.index]}/${this.$t(
                      'リンク確認'
                    )}: ${data[1][tooltipItem.index]}）`
                  : `${cumulativeSumArray[tooltipItem.index]}${unit}（${this.$t(
                      'リンク不明'
                    )}: ${cumulativeData[0][tooltipItem.index]}/${this.$t(
                      'リンク確認'
                    )}: ${cumulativeData[1][tooltipItem.index]}）`

              // 長い場合 スラッシュで改行
              return labelText.length < 50
                ? labelText
                : labelText.split(/(?=\/)/g)
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
                suggestedMax: this.scaledTicksYAxisMax,
                maxTicksLimit: 8,
                fontColor: '#808080'
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
      let n = 0
      let max = 0
      for (const i in this.displayData.datasets[0].data) {
        const current =
          this.displayData.datasets[0].data[i] +
          this.displayData.datasets[1].data[i]
        if (current > max) {
          max = current
          n = Number(i)
        }
      }
      return {
        labels: ['2020/1/1'],
        datasets: [
          {
            data: [this.displayData.datasets[0].data[n]],
            backgroundColor: 'transparent',
            borderWidth: 0
          },
          {
            data: [this.displayData.datasets[1].data[n]],
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
                fontColor: '#808080',
                suggestedMax: this.scaledTicksYAxisMax
              }
            }
          ]
        },
        animation: { duration: 0 }
      }
    },
    scaledTicksYAxisMax() {
      let max = 0
      for (const i in this.chartData[0]) {
        max = Math.max(max, this.chartData[0][i] + this.chartData[1][i])
      }
      return max
    }
  },
  created() {
    this.canvas = process.browser
    this.dataKind =
      this.$route.query.embed && this.$route.query.dataKind === 'cumulative'
        ? 'cumulative'
        : 'transition'
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

    window.addEventListener('resize', this.handleResize)
    this.handleResize()
  },
  destroyed() {
    window.removeEventListener('resize', this.handleResize)
  },
  methods: {
    onClickLegend(i) {
      this.displayLegends[i] = !this.displayLegends[i]
      this.displayLegends = this.displayLegends.slice()
    },
    cumulative(array) {
      const cumulativeArray = []
      let patSum = 0
      array.forEach(d => {
        patSum += d
        cumulativeArray.push(patSum)
      })
      return cumulativeArray
    },
    sum(array) {
      return array.reduce((acc, cur) => {
        return acc + cur
      })
    },
    pickLastNumber(chartDataArray) {
      return chartDataArray.map(array => {
        return array[array.length - 1]
      })
    },
    pickLastLastNumber(chartDataArray) {
      return chartDataArray.map(array => {
        return array[array.length - 2]
      })
    },
    cumulativeSum(chartDataArray) {
      return chartDataArray.map(array => {
        return array.reduce((acc, cur) => {
          return acc + cur
        })
      })
    },
    cumulativeLastSum(chartDataArray) {
      chartDataArray.pop()
      return chartDataArray.map(array => {
        return array.reduce((acc, cur) => {
          return acc + cur
        })
      })
    },
    eachArraySum(chartDataArray) {
      const sumArray = []
      for (let i = 0; i < chartDataArray[0].length; i++) {
        sumArray.push(chartDataArray[0][i] + chartDataArray[1][i])
      }
      return sumArray
    },
    formatDayBeforeRatio(dayBeforeRatio) {
      const dayBeforeRatioLocaleString = dayBeforeRatio.toLocaleString()
      switch (Math.sign(dayBeforeRatio)) {
        case 1:
          return `+${dayBeforeRatioLocaleString}`
        case -1:
          return `${dayBeforeRatioLocaleString}`
        default:
          return `${dayBeforeRatioLocaleString}`
      }
    },
    handleResize() {
      this.isSmall = window.innerWidth <= 400
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
