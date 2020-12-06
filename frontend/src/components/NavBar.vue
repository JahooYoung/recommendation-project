<template>
    <b-navbar
      id="nav"
      fixed="top"
      toggleable="md"
      type="dark"
      variant="dark"
    >
      <b-navbar-brand to="/">
        {{ $t('MoreRcmd') }}
      </b-navbar-brand>

      <b-navbar-toggle target="nav-collapse" />

      <b-collapse
        id="nav-collapse"
        is-nav
      >
        <b-navbar-nav>
          <b-nav-item to="/">
            {{ $t(`Home`) }}
          </b-nav-item>
          <b-nav-item to="/movies">
            {{ $t(`Movie`) }}
          </b-nav-item>
          <b-nav-item to="/rcmd-stats">
            {{ $t(`Statistics`) }}
          </b-nav-item>
          <b-nav-item @click="runRecommendation">
            {{ $t(`Run Recommendation`) }}
          </b-nav-item>
        </b-navbar-nav>

        <!-- Right aligned nav items -->
        <b-navbar-nav class="ml-auto">
          <!-- <SearchBox /> -->

          <!-- <b-nav-item-dropdown
            :text="$t('Language')"
            right
          >
            <b-dropdown-item
              :active="$i18n.locale === 'en'"
              @click="changeLocale('en')"
            >
              English
            </b-dropdown-item>
            <b-dropdown-item
              :active="$i18n.locale === 'zh'"
              @click="changeLocale('zh')"
            >
              简体中文
            </b-dropdown-item>
          </b-nav-item-dropdown> -->

          <div v-if="user !== null">
            <b-nav-item-dropdown right>
              <template slot="button-content">
                {{ user }}
                <!-- <b-badge variant="light">
                  1
                </b-badge> -->
              </template>
              <!-- <b-dropdown-item
                href="#"
                exact-active-class=""
              >
                {{ $t('Notification') }}
                <b-badge variant="dark">
                  1
                </b-badge>
              </b-dropdown-item>
              <b-dropdown-divider /> -->
              <!-- <b-dropdown-item
                to="/user-profile"
                exact-active-class=""
              >
                {{ $t('Your Profile') }}
              </b-dropdown-item>
              <b-dropdown-item
                to="/registered-event"
                exact-active-class=""
              >
                {{ $t('Registered events') }}
              </b-dropdown-item>
              <b-dropdown-item
                to="/admin-event"
                exact-active-class=""
              >
                {{ $t('Admin events') }}
              </b-dropdown-item>
              <b-dropdown-divider /> -->
              <b-dropdown-item @click="logout">
                {{ $t('Logout') }}
              </b-dropdown-item>
            </b-nav-item-dropdown>
          </div>
          <div v-else>
            <b-nav-item @click="needLogin()">
              {{ $t('Login/Register') }}
            </b-nav-item>
          </div>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
</template>

<script>
import {
  BNavbar, BNavbarNav, BNavbarBrand, BNavbarToggle, BCollapse, BNavItem,
  BNavItemDropdown, BDropdownItem, BDropdownDivider, BBadge
} from 'bootstrap-vue'
import { mapState } from 'vuex'
// import SearchBoxLoading from './SearchBoxLoading.vue'
// import { loadLanguageAsync } from '@/plugins/i18n'

export default {
  name: 'NavBar',
  components: {
    // SearchBox: () => ({
    //   component: import(/* webpackChunkName: "searchbox" */ './SearchBox.vue'),
    //   loading: SearchBoxLoading
    // }),
    BNavbar,
    BNavbarNav,
    BNavbarBrand,
    BNavbarToggle,
    BCollapse,
    BNavItem,
    BNavItemDropdown,
    BDropdownItem,
    // BDropdownDivider,
    // BBadge
  },
  methods: {
    async logout () {
      const res = await this.axios.post('/api/auth/logout/')
      await this.$store.dispatch('clearLocalDB')
      this.$store.commit('setUserState', null)
      this.$router.push('/')
    },
    changeLocale (lang) {
      loadLanguageAsync(lang)
    },
    async runRecommendation() {
      await this.axios.post(`/api/run-recommendation/`)
      this.$bvToast.toast(this.$t('Updating recommendation!'), {
        title: this.$t('Received!'),
        variant: 'primary',
        autoHideDelay: 2000,
        solid: true
      })
      const handler = setInterval(async () => {
        let res
        try {
          res = await this.axios.get(`/api/run-recommendation/`)
        } catch (e) {
          console.log(e)
        }
        if (res.data.isEnded) {
          clearInterval(handler)
          this.$bvToast.toast(this.$t('Recommendation updated!'), {
            title: this.$t('Yahoo!'),
            variant: 'success',
            autoHideDelay: 4000,
            solid: true
          })
        }
      }, 4000)
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

/* #nav-collapse .router-link-exact-active {
  color: #ffffff;
} */
</style>
