<template>
  <ul
    :class="$style.container"
    :aria-label="
      ariaLabel(
        検査実施人数,
        陽性物数,
        入院中,
        軽症中等症,
        重症,
        死亡,
        退院,
        現在陽性者数,
        入院調整中,
        入院待機中,
        入院もしくは療養方法の調整中,
        自宅療養,
        宿泊療養,
        療養等調整中,
        府外健康観察
      )
    "
  >
    <li>
      <div :class="[$style.row, $style['is-conducted']]">
        <span v-text="$t('検査実施件数')">)"></span>
        <span :class="$style.value"
          >{{ 検査実施人数 }}{{ $t('件.tested') }}</span
        >
      </div>
    </li>
    <li>
      <div :class="[$style.row, $style['is-positive']]">
        <span>{{ $t('陽性者数（累積）') }}</span>
        <span :class="$style.value">{{ 陽性物数 }}{{ $t('人') }}</span>
      </div>
      <ul
        :class="[
          $style.container,
          $style['sub-container'],
          $style['is-positive']
        ]"
      >
        <li>
          <div :class="[$style.row, $style['is-current-positive']]">
            <span>{{ $t('現在陽性者数') }}</span>
            <span :class="$style.value">{{ 現在陽性者数 }}{{ $t('人') }}</span>
          </div>
          <ul
            :class="[
              $style.container,
              $style['sub-container'],
              $style['is-current-positive']
            ]"
          >
            <li>
              <div :class="[$style.row, $style['is-gray']]">
                <span v-text="$t('入院')" />
                <span :class="$style.value">{{ 入院中 }}{{ $t('人') }}</span>
              </div>
              <ul
                :class="[
                  $style.container,
                  $style['sub-container'],
                  $style['is-gray']
                ]"
              >
                <li>
                  <div :class="[$style.row, $style['is-gray']]">
                    <span>{{ $t('重症') }}</span>
                    <span :class="$style.value">{{ 重症 }}{{ $t('人') }}</span>
                  </div>
                </li>
              </ul>
            </li>
            <li>
              <div :class="[$style.row, $style['is-gray']]">
                <span v-text="$t('入院等調整中')" />
                <span :class="$style.value"
                  >{{ 入院調整中 }}{{ $t('人') }}</span
                >
              </div>
            </li>
            <li>
              <div :class="[$style.row, $style['is-gray']]">
                <span>{{ $t('自宅療養') }}</span>
                <span :class="$style.value">{{ 自宅療養 }}{{ $t('人') }}</span>
              </div>
            </li>
            <li>
              <div :class="[$style.row, $style['is-gray']]">
                <span>{{ $t('宿泊療養') }}</span>
                <span :class="$style.value">{{ 宿泊療養 }}{{ $t('人') }}</span>
              </div>
            </li>
          </ul>
        </li>
        <li>
          <div :class="[$style.row, $style['is-current-positive']]">
            <span>{{ $t('他府県管理') }}</span>
            <span :class="$style.value">{{ 府外健康観察 }}{{ $t('人') }}</span>
          </div>
        </li>
        <li>
          <div :class="[$style.row, $style['is-deceased']]">
            <span>{{ $t('死亡') }}</span>
            <span :class="$style.value">{{ 死亡 }}{{ $t('人') }}</span>
          </div>
        </li>
        <li>
          <div :class="$style.row">
            <span>{{ $t('退院・解除済累計') }}</span>
            <span :class="$style.value">{{ 退院 }}{{ $t('人') }}</span>
          </div>
        </li>
      </ul>
    </li>
  </ul>
</template>

<script>
/* eslint-disable vue/prop-name-casing */
export default {
  props: {
    検査実施人数: {
      type: Number,
      required: true
    },
    陽性物数: {
      type: Number,
      required: true
    },
    入院中: {
      type: Number,
      required: true
    },
    軽症中等症: {
      type: Number,
      required: true
    },
    重症: {
      type: Number,
      required: true
    },
    死亡: {
      type: Number,
      required: true
    },
    退院: {
      type: Number,
      required: true
    },
    現在陽性者数: {
      type: Number,
      required: true
    },
    入院調整中: {
      type: Number,
      required: true
    },
    入院待機中: {
      type: Number,
      required: true
    },
    入院もしくは療養方法の調整中: {
      type: Number,
      required: true
    },
    自宅療養: {
      type: Number,
      required: true
    },
    宿泊療養: {
      type: Number,
      required: true
    },
    療養等調整中: {
      type: Number,
      required: true
    },
    府外健康観察: {
      type: Number,
      required: true
    }
  },
  methods: {
    /** グラフ内容がわかる支援技術用テキストの中身を取得する **/
    ariaLabel(
      inspected,
      positive,
      hospitalized,
      mild,
      critically,
      deceased,
      discharged,
      currentlyPositive,
      hospitalizeAdjust,
      recuperatingHome,
      recuperatingLodging,
      recuperatingAdjust
    ) {
      return this.$t(
        '検査陽性者の状況: 検査実施人数は{inspected}人、うち累積の陽性者数は{positive}人で、現在陽性者数は{currentlyPositive}人です。入院中は{hospitalized}人で、重症は{critically}人です、また入院調整中は{hospitalizeAdjust}人です。自宅療養は{recuperatingHome}人、宿泊療養は{recuperatingLodging}人、また療養等調整中は{recuperatingAdjust}人です。さらに死亡は{deceased}人、退院・解除済累計は{discharged}人です。',
        {
          inspected,
          positive,
          hospitalized,
          mild,
          critically,
          deceased,
          discharged,
          currentlyPositive,
          hospitalizeAdjust,
          recuperatingHome,
          recuperatingLodging,
          recuperatingAdjust
        }
      )
    }
  }
}
</script>

<style lang="scss" module>
$borderWidth: 2px;
$itemGap: 0.25em;

$positiveColor: lighten($green-1, 50%);
$currentPositiveColor: #e6e6e6;
$deceasedColor: #ccc;
$conductedColor: #333;

// for .sub-container
@mixin scBoxShadow($color) {
  box-shadow: $color 0px 2px 0px 0px inset;
}

ul.container {
  padding: 0;

  letter-spacing: 0.05em;

  &,
  li {
    list-style: none;
  }

  > li + li {
    margin-top: $itemGap;
  }
}

ul.sub-container {
  padding: $itemGap 0 0 2.25em;
  position: relative;

  &::before {
    content: '';

    width: 2em;

    border: solid $green-1;
    border-width: 0 $borderWidth $borderWidth;

    @include scBoxShadow(#fff);

    position: absolute;
    top: -2px;
    left: 0;
    bottom: 0;
  }

  &.is-positive::before {
    background: $positiveColor;
    @include scBoxShadow($positiveColor);
  }

  &.is-current-positive {
    &::before,
    .sub-container::before {
      background: $currentPositiveColor;
      @include scBoxShadow($currentPositiveColor);
    }

    .row {
      background: $currentPositiveColor;
    }
  }
}

.row {
  display: flex;
  align-items: center;
  justify-content: space-between;

  padding: 0.5em 1em;

  font-weight: bold;

  border: solid 2px $green-1;

  color: darken($green-1, 15%);

  &.is-positive {
    background: $positiveColor;
  }

  &.is-deceased {
    background: $deceasedColor;
  }

  &.is-current-positive {
    background: $currentPositiveColor;
  }

  &.is-conducted {
    border-color: $conductedColor;
    color: $conductedColor;
  }
}

.value {
  flex: none;

  margin-left: 1em;

  letter-spacing: 0.075em;
}
</style>
