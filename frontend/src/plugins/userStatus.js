import { mapState } from 'vuex'
// import { loadLanguageAsync } from '@/plugins/i18n'

function UserStatus () {}

UserStatus.install = function (Vue) {
  if (this.installed) {
    return
  }
  this.installed = true

  Vue.mixin({
    computed: mapState(['user']),
    methods: {
      async needLogin () {
        if (!this.user) {
          // this.toastWarning(this.$t('You need to login first'), null, '/login')
          await this.$root.$children[0].login()
        }
      },
      // checkActivated () {
      //   if (!this.checkLogin()) {
      //     return false
      //   }
      //   if (!this.userActivated) {
      //     this.toastWarning(this.$t('You need to activate first'), null, '/user-profile')
      //     return false
      //   }
      //   return true
      // },
      // async checkUserActivation () {
      //   try {
      //     const res = await this.axios.get('/api/dummy/')
      //     this.$store.commit('setUserActivation', res.data.isActivated)
      //     if (!res.data.isActivated) {
      //       this.toastWarning(this.$t('Click here to activate your account!'), this.$t('Account not activated'), '/user-profile')
      //     }
      //   } catch (err) {
      //     if (err.response && err.response.status >= 400 && err.response.status < 500) {
      //       this.$store.commit('setUserState', null)
      //       this.toastError(this.$t('Your signin seems expired, click here to login again!'), null, '/login')
      //     }
      //   }
      // }
    }
  })
}

export default UserStatus
