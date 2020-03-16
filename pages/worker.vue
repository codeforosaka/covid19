<template>
  <div class="Worker">
    <h2 class="Worker-Heading">
      企業の皆様・はたらく皆様へ
    </h2>
    <div v-for="(item, i) in items" :key="i">
      <TextCard :title="item.title" :link="item.link" :body="item.body" />
    </div>
  </div>
</template>
<script lang="ts">
import TextCard from '@/components/TextCard.vue'
export default {
  components: {
    TextCard
  },
  data() {
    return {
      items: [
        {
          title: '新型コロナウイルス感染症への対応のための融資メニュー',
          link:
            'http://www.pref.osaka.lg.jp/kinyushien/korona/index.html',
          body:
            '新型コロナウイルス感染症の発生により経営に影響を受けている中小企業のみなさまを支援するための融資制度がございますので、ご活用ください。'
        },
        {
          title: '事業継続緊急対策（テレワーク）助成金',
          link:
            'https://www.shigotozaidan.or.jp/koyo-kankyo/joseikin/kinkyutaisaku.html',
          body:
            '府内中堅・中小企業に対し、テレワークの導入に必要な機器やソフトウェア等の経費を助成します（限度額250万円、助成率10/10）。ぜひご活用ください。'
        },
        {
          title: '中小企業者等特別相談窓口',
          link:
            'http://www.pref.osaka.lg.jp/keieishien/corona/index.html',
          body:
            '資金繰りに関する相談、経営に関する相談（大阪府産業労働局　報道発表）'
        },
        {
          title: '新しいワークスタイルや企業活動の東京モデル「スムーズビズ」',
          link: 'https://smooth-biz.metro.tokyo.lg.jp/',
          body:
            'テレワーク・時差出勤などスムーズビズの取組は、新型コロナウイルス感染症の対策としても効果的です。感染症対策として、東京2020大会時の交通混雑緩和に向けた取組の前倒しをお願いします。'
        }
      ]
    }
  },
  head() {
    return {
      title: '企業の皆様・はたらく皆様へ'
    }
  }
}
</script>
<style lang="scss">
.Worker {
  &-Heading {
    @include font-size(30);
    font-weight: normal;
    color: $gray-2;
    margin-bottom: 12px;
  }
}
a {
  @include text-link();
}
</style>
