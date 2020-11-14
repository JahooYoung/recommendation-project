import Vue from 'vue'
import VueI18n from 'vue-i18n'
import axios from './axios'
import messages from '../locales/en.js'

Vue.use(VueI18n)

const i18n = new VueI18n({
  locale: 'en', // 设置语言环境
  fallbackLocale: 'en',
  messages: { en: messages } // 设置语言环境信息
})

const loadedLanguages = ['en'] // 我们的预装默认语言

function setI18nLanguage (lang) {
  i18n.locale = lang
  axios.defaults.headers.common['Accept-Language'] = lang
  document.querySelector('html').setAttribute('lang', lang)
  if (window.localStorage) {
    window.localStorage.locale = lang
  }
  return lang
}

export function loadLanguageAsync (lang) {
  if (i18n.locale !== lang) {
    if (!loadedLanguages.includes(lang)) {
      return import(/* webpackChunkName: "lang-[request]" */ `@/locales/${lang}.js`).then(msgs => {
        i18n.setLocaleMessage(lang, msgs.default)
        loadedLanguages.push(lang)
        return setI18nLanguage(lang)
      })
    }
    return Promise.resolve(setI18nLanguage(lang))
  }
  return Promise.resolve(lang)
}

if (window.localStorage && window.localStorage.locale) {
  loadLanguageAsync(window.localStorage.locale)
}

export default i18n

// function loadLocaleMessages () {
//   const locales = require.context('./locales', true, /[A-Za-z0-9-_,\s]+\.json$/i)
//   const messages = {}
//   locales.keys().forEach(key => {
//     const matched = key.match(/([A-Za-z0-9-_]+)\./i)
//     if (matched && matched.length > 1) {
//       const locale = matched[1]
//       messages[locale] = locales(key)
//     }
//   })
//   return messages
// }

// export default new VueI18n({
//   locale: process.env.VUE_APP_I18N_LOCALE || 'en',
//   fallbackLocale: process.env.VUE_APP_I18N_FALLBACK_LOCALE || 'en',
//   messages: loadLocaleMessages()
// })
