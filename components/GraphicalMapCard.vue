<template>
  <!-- <v-col cols="12" md="6" class="DataCard"> -->
  <data-view
    :title="$t('市町村毎の感染状況(地図)')"
    :title-id="'osaka-city-map-table'"
    :date="Data.patients.date"
  >
    <template v-slot:button>
      <p :class="$style.note">
        {{ $t('（注）退院している人数を含む') }}
      </p>
      <p :class="$style.note2">{{ $t('凡例（単位は人）') }}</p>
      <table :class="$style.note2">
        <tbody>
          <tr>
            <td><span class="color-test infected-level1" />0</td>
            <td><span class="color-test infected-level2" />1-4</td>
            <td><span class="color-test infected-level3" />5-19</td>
          </tr>
          <tr>
            <td><span class="color-test infected-level4" />20-49</td>
            <td><span class="color-test infected-level5" />50-99</td>
            <td>
              <span class="color-test infected-level6" />100 {{ $t('以上') }}
            </td>
          </tr>
        </tbody>
      </table>
    </template>
    <div id="map" ref="map" class="osaka-map" />
    <date-select-slider
      :chart-data="chartData"
      :value="[0, sliderMax]"
      :slider-max="sliderMax"
      :min-range="0"
      @sliderInput="sliderUpdate"
    />
    <p :class="$style.note">
      <a
        href="https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-N03-v2_4.html"
        target="_blank"
        rel="noopener noreferrer"
      >
        {{ $t('「国土数値情報（行政区域）」（国土交通省）を加工して作成') }}
      </a>
    </p>
  </data-view>
  <!-- </v-col> -->
</template>

<script>
import * as d3 from 'd3'
import dayjs from 'dayjs'
import Data from '@/data/data.json'
import DataView from '@/components/DataView.vue'
import DateSelectSlider from '@/components/DateSelectSlider.vue'

// 市町村の患者人数の連想配列
// key:市町村名
// value:陽性者数
let cityPatientsNumber = {}
let map

export default {
  components: {
    DataView,
    DateSelectSlider
  },
  data() {
    // データの一番古い日付
    const dateMin = dayjs(Data.patients.data[0].date)
    // データの一番新しい日付
    const dateMax = dayjs(
      Data.patients.data[Object.keys(Data.patients.data).length - 1].date
    )
    // 日付のダミーデータ
    const chartData = []
    for (let i = 0; dateMin.add(i, 'day') <= dateMax; i++) {
      chartData[i] = { label: dateMin.add(i, 'day') }
    }
    // 日付範囲選択スライダーで選択している範囲
    const graphRange = [0, (dateMax - dateMin) / 86400000 - 1]

    const data = {
      Data,
      dateMin,
      dateMax,
      chartData,
      graphRange
    }
    return data
  },
  computed: {
    // スライダーのデータ数
    sliderMax() {
      return (this.dateMax - this.dateMin) / 86400000
    }
  },
  mounted() {
    this.loadYouseiData()
    drawOsaka(this)
    updateData()
  },
  methods: {
    // 日付範囲選択スライダー変更イベント
    sliderUpdate(sliderValue) {
      console.log(sliderValue)
      this.graphRange = sliderValue
      this.loadYouseiData()
      updateData()
    },
    // 陽性者数集計
    loadYouseiData() {
      console.log('start loadYouseiData()')
      // 初期化
      cityPatientsNumber = {}

      const patients = Data.patients.data

      const minPos = this.graphRange[0]
      const maxPos = this.graphRange[1]
      const minDate = dayjs(this.chartData[minPos].label)
      const maxDate = dayjs(this.chartData[maxPos].label)

      for (const key of patients) {
        const date = dayjs(key.date)
        cityPatientsNumber[key.居住地] = cityPatientsNumber[key.居住地] || 0
        // 日付の範囲ならカウント
        if (minDate <= date && date <= maxDate) {
          cityPatientsNumber[key.居住地] += 1
        }
      }

      console.log('end loadYouseiData()')
    }
  }
}

// 大阪府描画
function drawOsaka(vm) {
  console.log('start drawOsaka()')

  // マップ描画領域作成
  map = d3
    .select('#map')
    .append('svg')
    .append('g')

  // staticフォルダのgeoJSONファイルをhttp経由で読み込む
  Promise.all([
    d3.json('osakapref.json'),
    d3.json('osakapref-centroid.json')
  ]).then(files => {
    const json = files[0]
    const centroid = files[1]

    // 市区町村表示領域を生成
    // ツールチップ
    const tooltip = d3
      .select('body')
      .append('div')
      .attr('class', 'tooltip')

    // 投影を処理する関数を用意する。データからSVGのPATHに変換するため。
    let projection = d3.geoMercator().fitWidth(486, json)

    // pathジェネレータ関数
    const path = d3.geoPath().projection(projection)
    // これがenterしたデータ毎に呼び出されpath要素のd属性にgeoJSONデータから変換した値を入れて市町村境界描画

    // paddingを追加し、viewBox属性のための数値を取得
    let bounds = path.bounds(json)
    projection = projection.fitExtent(
      [
        [5, 5],
        [bounds[1][0], bounds[1][1]]
      ],
      json
    )
    bounds = path.bounds(json)

    d3.select('#map')
      .select('svg')
      .attr(
        'viewBox',
        `0, 0, ${bounds[0][0] + bounds[1][0]}, ${bounds[0][1] + bounds[1][1]}`
      )
      .attr('width', bounds[0][0] + bounds[1][0])
      .attr('height', bounds[0][1] + bounds[1][1])

    // 地図表示
    map
      .selectAll('path')
      .data(json.features)
      .enter()
      .append('path')
      .attr('class', 'land')
      .attr('d', path)
      // 陽性者に対応した色で境界内を塗る
      .style('fill', function(d) {
        const cityName = getCity(d)
        return getColor(cityPatientsNumber[cityName])
      })
      // マウスオーバーでツールチップ表示
      .on('mouseover, mousemove', function(d) {
        const cityName = getCity(d)
        tooltip
          .style('opacity', 0.9)
          .html(
            `<strong>${vm.$t(cityName)}</strong><br>${
              cityPatientsNumber[cityName]
            } ${vm.$t('人')}`
          )
          .style('left', d3.event.pageX + 'px')
          .style('top', d3.event.pageY - 45 + 'px')
      })
      .on('mouseout', function() {
        tooltip.style('opacity', 0)
      })

    // 市区町村名の表示
    const textGroup = map
      .selectAll('g')
      .data(
        centroid.features.map(v => [
          projection(v.geometry.coordinates),
          v.properties.name
        ])
      )
      .enter()
      .append('g')

    ;['text-back', 'text-front'].forEach(v => {
      textGroup
        .append('text')
        .attr('class', `text ${v}`)
        .attr('x', d => d[0][0])
        .attr('y', d => d[0][1])
        .text(d => d[1])
        .on('mouseover, mousemove', d => {
          const cityName = d[1]
          tooltip
            .style('opacity', 0.9)
            .html(
              `<strong>${vm.$t(cityName)}</strong><br>${
                cityPatientsNumber[cityName]
              } ${vm.$t('人')}`
            )
            .style('left', `${d3.event.pageX}px`)
            .style('top', `${d3.event.pageY - 45}px`)
        })
        .on('mouseout', () => {
          tooltip.style('opacity', 0)
        })
    })
    console.log('end drawOsaka()')
  })
}

function updateData() {
  map
    .selectAll('path')
    // 陽性者に対応した色で境界内を塗る
    .style('fill', function(d) {
      const cityName = getCity(d)
      return getColor(cityPatientsNumber[cityName])
    })

  // 左側にデータ表示
  let i = 0
  map.selectAll('#map-data-list').remove()
  for (const [key, value] of Object.entries(cityPatientsNumber)) {
    map
      .append('text')
      .attr('id', 'map-data-list')
      .attr('x', 20)
      .attr('y', function() {
        return i++ * 13 + 20
      })
      .style('font-size', 12 + 'px')
      .text(key + ': ' + value)
  }
}

// 陽性者数に応じて塗る色を返す
function getColor(num) {
  if (num > 99) {
    return 'red'
  } else if (num > 49) {
    return 'deeppink'
  } else if (num > 19) {
    return 'magenta'
  } else if (num > 4) {
    return 'pink'
  } else if (num > 0) {
    return 'lemonchiffon'
  } else if (num === 0) {
    return 'white'
  }
  // ここには来ないはず
  console.error('想定外のnum' + num)
  return ''
}

// 市町村名取得
// @param gio gioJSONの１データ
function getCity(gio) {
  // 大阪市と堺市はN03_004が区なので、N03_003を参照する。その他はN03_004を使用する
  const cityName = gio.properties.N03_004.endsWith('区')
    ? gio.properties.N03_003
    : gio.properties.N03_004
  return cityName
}
</script>

<style lang="scss" module>
.note {
  @include font-size(12);

  margin-top: 10px;
  margin-bottom: 0;
  color: $gray-3;

  &2 {
    @include font-size(14);
  }
}
</style>
<!-- 本来ならばSVGをinline展開してそこに限定してcssを適用するべきだが、inline展開ができなかったため妥協 -->
<style lang="scss">
$infected-level1: white;
$infected-level2: lemonchiffon;
$infected-level3: pink;
$infected-level4: magenta;
$infected-level5: deeppink;
$infected-level6: red;

.color-test {
  vertical-align: middle;
  width: 2.5rem;
  height: 1rem;
  display: inline-block;
  margin: 0 0.5rem 0 0;
}
.infected-level1 {
  fill: $infected-level1 !important;
  background-color: $infected-level1;
}
.infected-level2 {
  fill: $infected-level2 !important;
  background-color: $infected-level2;
}
.infected-level3 {
  fill: $infected-level3 !important;
  background-color: $infected-level3;
}
.infected-level4 {
  fill: $infected-level4 !important;
  background-color: $infected-level4;
}
.infected-level5 {
  fill: $infected-level5 !important;
  background-color: $infected-level5;
}
.infected-level6 {
  fill: $infected-level6 !important;
  background-color: $infected-level6;
}
.osaka-map {
  font-size: 0;
}

.tooltip {
  background: rgba(0, 0, 0, 0.9);
  font-size: 11px;
  color: #fff;
  border-radius: 4px;
  padding: 4px;
  transition: opacity 0.2s;
  position: absolute;
  opacity: 0;
}

#map svg {
  width: 100%;
}

#map .land {
  stroke: #333;
  stroke-width: 1px;
}

#map .text {
  font-size: 12px;
  font-weight: bold;

  text-anchor: middle;
  dominant-baseline: middle;
}

#map .text-back {
  stroke: #fff;
  stroke-width: 4px;
  stroke-linejoin: round;
}

#map .text-front {
  fill: #000;
}
</style>
