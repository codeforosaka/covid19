<template>
  <div class="SideNavigation">
    <div class="SideNavigation-HeadingContainer sp-flex">
      <v-icon
        class="SideNavigation-HeadingIcon pc-none"
        :aria-label="$t('サイドメニュー項目を開く')"
        @click="openNavi"
      >
        mdi-menu
      </v-icon>
      <nuxt-link :to="localePath('/')" class="SideNavigation-HeadingLink">
        <div class="SideNavigation-Logo">
          <img src="/logo.png" :alt="$t('大阪府')" />
        </div>
        <h1 class="SideNavigation-Heading">
          {{ $t('新型コロナウイルス感染症') }}<br />{{ $t('対策サイト') }}
        </h1>
      </nuxt-link>
    </div>

    <div class="sp-none" :class="{ open: isNaviOpen }">
      <v-icon
        class="SideNavigation-ListContainerIcon pc-none"
        :aria-label="$t('サイドメニュー項目を閉じる')"
        @click="closeNavi"
      >
        mdi-close
      </v-icon>

      <div class="SideNavigation-ListItemContainer">
        <div
          v-if="this.$i18n.locales.length > 1"
          class="SideNavigation-Language"
        >
          <label class="SideNavigation-LanguageLabel" for="LanguageSelector">
            {{ $t('多言語対応選択メニュー') }}
          </label>
          <LanguageSelector />
        </div>
      </div>

      <v-divider class="SideNavigation-Divider" />

      <v-list :flat="true">
        <v-container
          v-for="(item, i) in items"
          :key="i"
          class="SideNavigation-ListItemContainer"
          @click="closeNavi"
        >
          <ListItem :link="item.link" :icon="item.icon" :title="item.title" />
          <v-divider v-show="item.divider" class="SideNavigation-Divider" />
        </v-container>
      </v-list>
      <div class="SideNavigation-Footer">
        <i18n
          tag="small"
          path="このサイトの内容物は{creativeCommons}の下に提供されています。"
          class="SideNavigation-Copyright"
        >
          <template v-slot:creativeCommons>
            <a
              rel="noopener"
              target="_blank"
              :href="$t('https://creativecommons.org/licenses/by/4.0/deed.ja')"
            >
              {{ $t('クリエイティブ・コモンズ 表示 4.0 ライセンス') }}
            </a>
          </template>
        </i18n>
        <br />
        <small class="SideNavigation-Copyright">
          2020 Osaka Prefectural Government × CODE for OSAKA
        </small>
      </div>
    </div>
  </div>
</template>

<script>
import ListItem from '@/components/ListItem'
import LanguageSelector from '@/components/LanguageSelector.vue'

export default {
  components: {
    LanguageSelector,
    ListItem
  },
  props: {
    isNaviOpen: {
      type: Boolean,
      required: true
    }
  },
  computed: {
    items() {
      return [
        {
          icon: 'mdi-chart-timeline-variant',
          title: this.$t('府内の最新感染動向'),
          link: this.localePath('/')
        },
        {
          icon: 'covid',
          title: this.$t('新型コロナウイルス感染症について'),
          link: 'http://www.pref.osaka.lg.jp/iryo/osakakansensho/corona.html'
        },
        {
          icon: 'mdi-domain',
          title: this.$t('新型コロナウイルス感染症関連情報'),
          link: 'http://www.pref.osaka.lg.jp/kikaku/covid19info/index.html'
        },
        {
          icon: 'mdi-account-multiple',
          title: this.$t('大阪府新型コロナウイルス対策本部'),
          link: 'http://www.pref.osaka.lg.jp/iryo/2019ncov/index.html',
          divider: true
        },
        {
          title: this.$t('知事からのメッセージ'),
          link: 'http://www.pref.osaka.lg.jp/kikaku/message_governor/index.html'
        },
        {
          title: this.$t('当サイトについて'),
          link: this.localePath('/about')
        },
        {
          title: this.$t('大阪府公式ホームページ'),
          link: 'http://www.pref.osaka.lg.jp/',
          divider: true
        },
        {
          title: this.$t('大阪府公式Twitter'),
          link: 'https://twitter.com/osakaprefPR/'
        },
        {
          title: this.$t('大阪府公式Facebook'),
          link: 'https://www.facebook.com/osaka.pref'
        },
        {
          title: this.$t('大阪府公式LINE'),
          link: 'https://lin.ee/8IJ5WMv'
        },
        {
          title: this.$t('おおさか防災ネットTwitter'),
          link: 'https://twitter.com/osaka_bousai',
          divider: true
        }
      ]
    },
    isClass() {
      return item => (item.title.charAt(0) === '【' ? 'kerningLeft' : '')
    }
  },
  methods: {
    openNavi() {
      this.$emit('openNavi')
    },
    closeNavi() {
      this.$emit('closeNavi')
    }
  }
}
</script>

<style lang="scss" scoped>
.SideNavigation {
  position: relative;
  height: 100%;
  background: $white;
  box-shadow: 0px 0px 2px rgba(0, 0, 0, 0.15);
  &-HeadingContainer {
    padding: 1.25em 0 1.25em 1.25em;
    align-items: center;
    @include lessThan($small) {
      padding: 7px 0 7px 20px;
    }
  }
  &-HeadingIcon {
    margin-right: 16px;
  }
  &-HeadingLink {
    @include lessThan($small) {
      display: flex;
      align-items: center;
    }
    text-decoration: none;
  }
  &-ListContainerIcon {
    margin: 24px 16px 0;
  }
  &-ListItemContainer {
    padding: 2px 20px;
  }
  &-Logo {
    margin: 20px 16px 0 0;
    width: 110px;
    @include lessThan($small) {
      margin-top: 0;
    }
  }
  &-Heading {
    margin-top: 8px;
    font-size: 13px;
    color: #898989;
    padding: 0.5em 0;
    text-decoration: none;
    @include lessThan($small) {
      margin-top: 0;
    }
  }
  &-HeadingDivider {
    margin: 0px 20px 4px;
    @include lessThan($small) {
      display: none;
    }
  }
  &-Divider {
    margin: 12px 0;
  }
  &-Footer {
    padding: 20px;
    background-color: $white;
  }
  &-SocialLinkContainer {
    display: flex;
    & img {
      width: 30px;
      &:first-of-type {
        margin-right: 10px;
      }
    }
  }
  &-Copyright {
    display: block;
    margin-top: 10px;
    font-size: 8px;
    line-height: 1.2;
    color: $gray-1;
    font-weight: bold;
  }
}

.SideNavigation-Menu {
  @include lessThan($small) {
    padding-top: 50px;
  }
}

.SideNavigation-LanguageLabel {
  display: block;
  margin-bottom: 5px;
  font-size: 0.85rem;
}

.open {
  @include lessThan($small) {
    position: fixed;
    top: 0;
    bottom: 0;
    left: 0;
    display: block !important;
    width: 100%;
    z-index: z-index-of(opened-side-navigation);
    background-color: $white;
    height: 100%;
    overflow-y: scroll;
  }
}
@include largerThan($small) {
  .pc-none {
    display: none;
  }
}
@include lessThan($small) {
  .sp-flex {
    display: flex;
  }
  .sp-none {
    display: none;
  }
}
</style>
