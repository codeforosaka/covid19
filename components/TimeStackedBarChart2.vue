<template>
  <data-view :title="title" :title-id="titleId" :date="date">
    <template v-slot:button>
      <data-selector v-model="dataKind" />
    </template>
    <bar
      :chart-id="chartId"
      :chart-data="displayData"
      :options="options"
      :height="240"
    />
    <div class="note">
      {{ $t('※報道提供における本日判明数での集計') }}
    </div>
    <template v-slot:infoPanel>
      <data-view-basic-info-panel
        :l-text="displayInfo.lText"
        :s-text-list="[displayInfo.sText1, displayInfo.sText2]"
        :unit="displayInfo.unit"
      />
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
import DataView from '@/components/DataView.vue'
import DataSelector from '@/components/DataSelector.vue'
import DataViewBasicInfoPanel from '@/components/DataViewBasicInfoPanel.vue'

export default {
  components: { DataView, DataSelector, DataViewBasicInfoPanel },
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
    }
  },
  data() {
    return {
      dataKind: 'transition'
    }
  },
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
    options() {
      const unit = this.unit
      const sumArray = this.eachArraySum(this.chartData)
      const data = this.chartData
      const cumulativeData = this.chartData.map(item => {
        return this.cumulative(item)
      })
      const cumulativeSumArray = this.eachArraySum(cumulativeData)
      return {
        tooltips: {
          displayColors: false,
          position: 'nearest',
          intersect: false,
          axis: 'x',
          filter(tooltipItem) {
            return tooltipItem.datasetIndex === 1
          },
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
        responsive: true,
        maintainAspectRatio: false,
        legend: {
          display: true
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
                minRotation: 0,
                callback: label => {
                  return label.split('/')[1]
                }
              }
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
                fontStyle: 'bold',
                callback: label => {
                  const monthStringArry = [
                    'Jan',
                    'Feb',
                    'Mar',
                    'Apr',
                    'May',
                    'Jun',
                    'Jul',
                    'Aug',
                    'Sep',
                    'Oct',
                    'Nov',
                    'Dec'
                  ]
                  const month = monthStringArry.indexOf(label.split(' ')[0]) + 1
                  return month + '月'
                }
              },
              type: 'time',
              time: {
                unit: 'month'
              }
            }
          ],
          yAxes: [
            {
              location: 'bottom',
              stacked: true,
              gridLines: {
                display: true,
                color: '#E5E5E5'
              },
              ticks: {
                suggestedMin: 0,
                maxTicksLimit: 8,
                fontColor: '#808080'
              }
            }
          ]
        }
      }
    }
  },
  methods: {
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
    }
  }
}
</script>

<style lang="scss" scoped>
.Graph-Desc {
  margin: 10px 0;
  font-size: 12px;
  color: $gray-3;
}
</style>
