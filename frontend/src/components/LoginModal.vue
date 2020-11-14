<template>
  <div>
    <b-modal
      ref="login-modal"
      title="Login"
      no-stacking
      :ok-disabled="haveErr"
      @ok.prevent="submit"
      @hide="checkLogin"
    >
      <b-form-group
        id="usernameInputGroup"
        :label="$t('Username:')"
        label-for="usernameInput"
      >
        <b-form-input
          id="usernameInput"
          v-model="form.username"
          autofocus
          type="text"
          required
        />
      </b-form-group>
      <b-form-group
        id="passwordInputGroup"
        :label="$t('Password:')"
        label-for="passwordInput"
        :state="!haveErr"
      >
        <b-form-input
          id="passwordInput"
          v-model="form.password"
          type="password"
          required
          @keydown.enter.prevent="!haveErr && submit()"
        />
        <template #invalid-feedback>
          <div v-if="haveErr">
            {{ $t('Username or password is wrong') }}!
          </div>
        </template>
      </b-form-group>

      <template #modal-footer="{ ok, cancel }">
        <b-button variant="outline-secondary" @click="register()">
          Register
        </b-button>
        <b-button variant="secondary" @click="cancel()">
          Cancel
        </b-button>
        <b-button variant="primary" @click="ok()">
          OK
        </b-button>
      </template>
    </b-modal>

    <RegisterModal ref="register-modal"/>
  </div>
</template>

<script>
import RegisterModal from './RegisterModal.vue'

export default {
  name: 'LoginModal',
  components: {
    RegisterModal
  },
  data () {
    return {
      form: {
        username: '',
        password: '',
      },
      haveErr: false,
      registering: false,
      resolve: null,
      reject: null,
    }
  },
  watch: {
    'form.username' () {
      this.haveErr = false
    },
    'form.password' () {
      this.haveErr = false
    }
  },
  methods: {
    login() {
      this.form.username = this.form.password = ''
      this.haveErr = false
      this.registering = false
      this.$refs['login-modal'].show()
      return new Promise((resolve, reject) => {
        this.resolve = resolve
        this.reject = reject
      })
    },
    register() {
      this.registering = true
      this.$refs['login-modal'].hide()
      setTimeout(() => {
        this.$refs['register-modal'].register().then(resolve, reject)
      }, 200)
    },
    async submit(event) {
      // event.preventDefault()
      try {
        const res = await this.axios.post('/api/auth/login/', {
          username: this.form.username,
          password: this.form.password
        })
        this.$store.commit('setUserState', {
          user: this.form.username,
          key: res.data.key
        })
        this.$refs['login-modal'].hide()
        this.resolve()
        // await this.checkUserActivation()
        // if (window.history.length > 1) {
        //   this.$router.back()
        // } else {
        //   this.$router.push('/')
        // }
      } catch (err) {
        if (err.response.status == 400) {
          this.haveErr = true
        } else {
          console.log(err.response)
          this.reject('Unknown Error')
        }
      }
    },
    checkLogin() {
      if (!this.registering && !this.$store.state.user) {
        this.reject('User cancelled')
      }
    },
  }
}
</script>

<style>

</style>
