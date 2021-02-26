<template>
  <data-view class="SvgCard" :title="title" :title-id="titleId" :date="date">
    <slot />
    <div class="note">
      {{ $t('※11月15日までは再陽性者を除き、11月16日以降は再陽性者を含む')
      }}<br />
      {{ $t('※11月16日以降、検査実施件数に再陽性検査数を含む') }}
    </div>
  </data-view>
</template>

<style lang="scss" scoped>
.SvgCard {
  ::v-deep svg {
    width: 100%;
  }
  .Graph-Desc {
    margin-top: 10px;
    margin-bottom: 0;
    font-size: 12px;
    color: $gray-3;
  }
  .note {
    padding: 8px;
    font-size: 12px;
    color: #808080;
  }
}
</style>

<script>
import DataView from '@/components/DataView.vue'

export default {
  components: { DataView },
  props: {
    title: {
      type: String,
      default: ''
    },
    titleId: {
      type: String,
      default: ''
    },
    date: {
      type: String,
      default: ''
    },
    note: {
      type: String,
      required: false,
      default: ''
    }
  }
}
</script>
