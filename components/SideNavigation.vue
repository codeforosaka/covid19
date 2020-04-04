<template>
  <div class="SideNavigation">
    <div class="SideNavigation-HeadingContainer sp-flex">
      <v-icon
        class="SideNavigation-HeadingIcon pc-none"
        :aria-label="$t('Navi Open')"
        @click="openNavi"
      >
        mdi-menu
      </v-icon>
      <nuxt-link to="/" class="SideNavigation-HeadingLink">
        <div class="SideNavigation-Logo">
          <img src="/logo.png" :alt="$t('Tokyo')" />
        </div>
        <h1 class="SideNavigation-Heading">
          {{ $t('COVID-19') }}<br />{{ $t('Measures site') }}
        </h1>
      </nuxt-link>
    </div>
    <v-divider class="SideNavigation-HeadingDivider" />
    <div class="sp-none" :class="{ open: isNaviOpen }">
      <v-icon
        class="SideNavigation-ListContainerIcon pc-none"
        :aria-label="$t('Navi Close')"
        @click="closeNavi"
      >
        mdi-close
      </v-icon>
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
        <div class="SideNavigation-SocialLinkContainer">
          <a
            href="https://lin.ee/8IJ5WMv"
            target="_blank"
            rel="noopener noreferrer"
            class="SideNavigation-SocialLink"
          >
            <picture>
              <source srcset="/line.webp" type="image/webp" />
              <img src="/line.png" alt="LINE" />
            </picture>
          </a>
          <a
            href="https://twitter.com/osaka_bousai"
            target="_blank"
            rel="noopener noreferrer"
            class="SideNavigation-SocialLink"
          >
            <picture>
              <source srcset="/twitter.webp" type="image/webp" />
              <img src="/twitter.png" alt="Twitter" />
            </picture>
          </a>
          <a
            href="https://twitter.com/osakaprefPR"
            target="_blank"
            rel="noopener noreferrer"
            class="SideNavigation-SocialLink"
          >
            <picture>
              <source srcset="/twitter.webp" type="image/webp" />
              <img src="/twitter.png" alt="Twitter" />
            </picture>
          </a>
          <a
            href="https://www.facebook.com/osaka.pref"
            target="_blank"
            rel="noopener noreferrer"
            class="SideNavigation-SocialLink"
          >
            <picture>
              <source srcset="/facebook.webp" type="image/webp" />
              <img src="/facebook.png" alt="Facebook" />
            </picture>
          </a>
          <a
            href="https://github.com/codeforosaka/covid19"
            target="_blank"
            rel="noopener noreferrer"
            class="SideNavigation-SocialLink"
          >
            <picture>
              <source srcset="/github.webp" type="image/webp" />
              <img src="/github.png" alt="GitHub" />
            </picture>
          </a>
        </div>
        <small class="SideNavigation-Copyright" lang="en">
          Content on This Site is Licensed Under a
          <a
            rel="license"
            target="_blank"
            href="http://creativecommons.org/licenses/by/4.0/"
          >
            Creative Commons Attribution 4.0 International License </a
          ><br />
          2020 Osaka Prefectural Government × CODE for OSAKA
        </small>
      </div>
    </div>
  </div>
</template>

<i18n>
{
  "ja": {
    "Navi Open": "サイドメニュー項目を開く",
    "Navi Close": "サイドメニュー項目を閉じる",
    "Tokyo": "大阪府",
    "COVID-19": "新型コロナウイルス感染症",
    "Measures site": "対策サイト",
    "Tokyo Metropolitan Government": "大阪府",
    "Tokyo COVID-19 Task Force": "新型コロナウイルス感染症対策本部",
    "The latest updates": "府内の最新感染動向",
    "If you have any symptoms": "新型コロナウイルス感染症が心配なときに",
    "for Families with children": "お子様をお持ちの皆様へ",
    "for Citizens": "府民の皆様へ",
    "for Enterprises and Employees": "企業の皆様・はたらく皆様へ",
    "Official statements from Task Force": "大阪府新型コロナウイルス感染症対策本部報",
    "Cancelled public events": "大阪府主催等 中止又は延期するイベント等",
    "Government official website": "大阪府公式ホームページ",
    "Message from Governor Koike": "知事からのメッセージ",
    "About us": "当サイトについて",
    "About covid19": "新型コロナウイルス感染症について",
    "Related info": "新型コロナウイルス感染症関連情報",
    "Task Force": "大阪府新型コロナウイルス対策本部",
    "Message from Governor": "知事からのメッセージ",
    "Official Twitter": "大阪府公式Twitter",
    "Official Facebook": "大阪府公式Facebook",
    "Official LINE": "大阪府公式LINE",
    "Bousai Twitter": "おおさか防災ネットTwitter"
  }
}
</i18n>

<script>
import ListItem from '@/components/ListItem'

export default {
  components: {
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
          title: this.$t('The latest updates'),
          link: '/'
        },
        {
          icon: 'covid',
          title: this.$t('About covid19'),
          link: 'http://www.pref.osaka.lg.jp/iryo/osakakansensho/corona.html'
        },
        {
          icon: 'mdi-domain',
          title: this.$t('Related info'),
          link: 'http://www.pref.osaka.lg.jp/kikaku/covid19info/index.html'
        },
        {
          icon: 'mdi-account-multiple',
          title: this.$t('Task Force'),
          link: 'http://www.pref.osaka.lg.jp/iryo/2019ncov/index.html',
          divider: true
        },
        {
          title: this.$t('Message from Governor'),
          link:
            'http://www.pref.osaka.lg.jp/iryo/osakakansensho/corona_message.html'
        },
        {
          title: this.$t('About us'),
          link: '/about'
        },
        {
          title: this.$t('Government official website'),
          link: 'http://www.pref.osaka.lg.jp/',
          divider: true
        },
        {
          title: this.$t('Official Twitter'),
          link: 'https://twitter.com/osakaprefPR/'
        },
        {
          title: this.$t('Official Facebook'),
          link: 'https://www.facebook.com/osaka.pref'
        },
        {
          title: this.$t('Official LINE'),
          link: 'https://lin.ee/8IJ5WMv'
        },
        {
          title: this.$t('Bousai Twitter'),
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
    padding: 0px 20px 20px 20px;
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
  &-SocialLink {
    border: 1px dotted transparent;
    border-radius: 30px;
    color: $gray-3;

    &:link,
    &:hover,
    &:visited,
    &:active {
      color: inherit;
      text-decoration: none;
    }

    &:focus {
      color: inherit;
      text-decoration: none;
      border: 1px dotted $gray-3;
      outline: none;
    }

    & + & {
      margin-left: 10px;
    }

    img {
      width: 30px;
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
