<template>
  <div id="app">
    <div class="navbar-div">
      <transition
        name="nav-fade"
        mode="out-in"
      >
        <NavBar v-show="$route.name != 'NoteEdit'"/>
      </transition>
    </div>
    <transition
      name="fade"
      mode="out-in"
    >
      <!-- <keep-alive include="NoteEdit"> -->
        <router-view />
      <!-- </keep-alive> -->
    </transition>

    <b-toast
      id="update-toast"
      title="Webdocs更新"
      auto-hide-delay="5000"
      solid
      variant="info"
    >
      Webdocs有更新！<br>
      点击
      <b-link @click="reload()">
        刷新
      </b-link>
      立刻更新， <br>
      或下次访问时自动更新。
    </b-toast>

    <LoginModal ref="login-modal" />
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue'
import LoginModal from '@/components/LoginModal.vue'

export default {
  name: 'App',
  components: {
    NavBar,
    LoginModal,
  },
  created() {
    this.axios.interceptors.response.use(res => res, err => {
      err.needHandle = true
      if (!err.response) {
        err.needHandle = false
        this.$bvToast.toast(this.$t('Fail to connect server'), {
          title: this.$t('Network Error'),
          variant: 'secondary',
          autoHideDelay: 4000,
          solid: true
        })
      } else {
        //! this should be the only `console.log` of network request
        console.log(err.response)
        switch (err.response.status) {
          case 400:
            // Bad Request: most of these are validation error.
            // Should be processed by the caller.
            break
          case 401:
            // Unauthorized: probably not login.
            // If 401 is returned, it is probable that you forget to
            // call `checkLogin()`.

            // clear user if token invalid
            this.$store.commit('setUserState', null)
            break
          case 403:
            // Forbidden: user does not have permission.
            err.needHandle = false
            this.$bvToast.toast(this.$t('You do not have permission'), {
              title: this.$t('Forbidden'),
              variant: 'secondary',
              autoHideDelay: 4000,
              solid: true
            })
            break
          case 404:
            // Not Found: the resource is not existed.
            // Should be processed by the caller.
            break
          case 500:
            // Internal Server Error
            err.needHandle = false
            this.$bvToast.toast(this.$t('It seems some error occured in the server'), {
              title: this.$t('Internal Server Error'),
              variant: 'secondary',
              autoHideDelay: 4000,
              solid: true
            })
            break
          default:
            err.needHandle = false
            this.$bvToast.toast(this.$t('Unknown status code ') + err.response.status, {
              title: this.$t('Unknown Error'),
              variant: 'secondary',
              autoHideDelay: 4000,
              solid: true
            })
            break
        }
      }
      return Promise.reject(err)
    })

    document.querySelector('#first-page-spinner').remove()
  },
  methods: {
    login() {
      return this.$refs['login-modal'].login()
    },
    reload() {
      if('serviceWorker' in navigator) {
        navigator.serviceWorker.getRegistrations()
          .then((registrations) => {
              for(let registration of registrations) {
                console.log('unregister',registration);
                registration.unregister();
              }
          });
      }
      setTimeout(() => window.location.reload(true), 100);
    }
  }
}
</script>

<style lang="scss">
// #app {
//   font-family: Avenir, Helvetica, Arial, sans-serif;
//   -webkit-font-smoothing: antialiased;
//   -moz-osx-font-smoothing: grayscale;
//   text-align: center;
//   color: #2c3e50;
// }

// #nav {
//   padding: 30px;

//   a {
//     font-weight: bold;
//     color: #2c3e50;

//     &.router-link-exact-active {
//       color: #42b983;
//     }
//   }
// }

/* 可以设置不同的进入和离开动画 */
/* 设置持续时间和动画函数 */
.nav-fade-enter-active, .nav-fade-leave-active {
  transition: all .8s ease;
  // #nav {
  //   transition: all .8s ease;
  // }
}
.nav-fade-enter, .nav-fade-leave-to {
  // transform: translateY(-100px);
  top: -5rem !important;
  // opacity: 0;
}

.navbar-div {
  margin-bottom: 5rem;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity .15s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}
</style>
