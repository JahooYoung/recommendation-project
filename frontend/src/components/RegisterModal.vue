<template>
  <b-modal
    ref="register-modal"
    title="Register"
    :ok-disabled="haveErr"
    @ok.prevent="submit"
    @hide="checkLogin"
  >
    <b-form-group
      id="usernameInputGroup"
      :label="$t('Username:')"
      label-for="usernameInput"
      label-cols-sm="4"
      label-cols-lg="3"
      :state="($v.username.$dirty || null) && !$v.username.$error"
      :valid-feedback="$t('This username is available!')"
    >
      <b-form-input
        id="usernameInput"
        v-model.trim="$v.username.$model"
        autofocus
        @blur="$v.username.$touch()"
      />
      <template #invalid-feedback>
        <div v-if="!$v.username.required">
          {{ $t('This field is required.') }}
        </div>
        <div v-else-if="!$v.username.noServerError">
          {{ $t('Register.vue username',[err.username[0]]) }}
        </div>
      </template>
    </b-form-group>

    <b-form-group
      id="emailInputGroup"
      :label="$t('Email:')"
      label-for="emailInput"
      label-cols-sm="4"
      label-cols-lg="3"
      :state="!$v.email.$error"
    >
      <b-form-input
        id="emailInput"
        v-model.trim="$v.email.$model"
        @blur="$v.email.$touch()"
      />
      <template #invalid-feedback>
        <div v-if="!$v.email.required">
          {{ $t('This field is required.') }}
        </div>
        <div v-if="!$v.email.email">
          {{ $t('Please input a valid email') }}
        </div>
        <div v-else-if="!$v.email.noServerError">
          {{ $t('Register.vue email', [err.email[0]]) }}
        </div>
      </template>
    </b-form-group>

    <b-form-group
      id="passwordInputGroup"
      :label="$t('Password:')"
      label-for="passwordInput"
      label-cols-sm="4"
      label-cols-lg="3"
      :state="!$v.password.$error"
    >
      <b-form-input
        id="passwordInput"
        v-model.trim="$v.password.$model"
        type="password"
        @blur="$v.password.$touch()"
      />
      <template #invalid-feedback>
        <div v-if="!$v.password.required">
          {{ $t('This field is required.') }}
        </div>
        <div v-else-if="!$v.password.minLength">
          {{ $t('Password must contain at least characters',[$v.password.$params.minLength.min]) }}
        </div>
        <div v-else-if="!$v.password.complex">
          {{ $t('Password can not contains only digits, only lowercase alpha or only uppercase alpha.') }}
        </div>
        <div v-else-if="!$v.password.uncommon">
          {{ $t('This password is too common.') }}
        </div>
        <div v-else-if="!$v.password.noServerError">
          {{ $t('Register.vue password', err.password1[0]) }}
        </div>
      </template>
    </b-form-group>

    <b-form-group
      id="RepeatPasswordInputGroup"
      :label="$t('Repeat password:')"
      label-for="repeatPasswordInput"
      label-cols-sm="4"
      label-cols-lg="3"
      :state="!$v.repeatPassword.$error"
    >
      <b-form-input
        id="repeatPasswordInput"
        v-model.trim="$v.repeatPassword.$model"
        type="password"
        @blur="$v.repeatPassword.$touch()"
        @keydown.enter.prevent="!haveErr && submit()"
      />
      <template #invalid-feedback>
        <div v-if="!$v.repeatPassword.sameAsPassword">
          {{ $t('Two passwords are different!') }}
        </div>
      </template>
    </b-form-group>
  </b-modal>
</template>

<script>
import { validationMixin } from 'vuelidate'
import { required, minLength, maxLength, numeric, sameAs, email, helpers, not } from 'vuelidate/lib/validators'

export default {
  name: 'RegisterModal',
  mixins: [validationMixin],
  data () {
    return {
      username: '',
      password: '',
      repeatPassword: '',
      email: '',
      realName: '',
      submitted: {},
      err: {},
      resolve: null,
      reject: null,
    }
  },
  validations: {
    username: {
      required,
      noServerError (value) {
        return value !== this.submitted.username || !this.err.username
      }
    },
    password: {
      required,
      minLength: minLength(8),
      complex: not(helpers.regex('complex', /^([\d]*|[a-z]*|[A-Z]*)$/)),
      noServerError (value) {
        return value !== this.submitted.password1 || !this.err.password1
      }
    },
    repeatPassword: {
      sameAsPassword: sameAs('password')
    },
    email: {
      required,
      email,
      noServerError (value) {
        return value !== this.submitted.email || !this.err.email
      }
    },
  },
  methods: {
    register() {
      this.username = this.password = this.repeatPassword = this.email = ''
      this.err = {}
      this.$v.$reset()
      this.$refs['register-modal'].show()
      return new Promise((resolve, reject) => {
        this.resolve = resolve
        this.reject = reject
      })
    },
    async submit(event) {
      // event.preventDefault()
      try {
        this.err = {}
        this.submitted = {
          username: this.username,
          password1: this.password,
          password2: this.repeatPassword,
          email: this.email,
          realName: this.realName
        }
        const res = await this.axios.post('/api/auth/registration/', this.submitted)
        this.$store.commit('setUserState', {
          user: this.username,
          key: res.data.key
        })
        this.$refs['register-modal'].hide()
        this.resolve()
      } catch (err) {
        if (err.response && err.response.status === 400) {
          this.err = err.response.data
          this.$v.$touch()
        }
      }
    },
    checkLogin() {
      if (!this.$store.state.user) {
        this.reject('User cancelled')
      }
    },
  }
}
</script>

<style>

</style>
