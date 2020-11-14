import Vue from 'vue'
import _axios from 'axios'
import store from '@/store'

const TIME_FIELD = /created|last_modified/

export function camelCase (str) {
  return str.replace(/_([a-z])/g, match => match[1].toUpperCase())
}

export function snakeCase (str) {
  return str.replace(/[A-Z]/g, match => '_' + match[0].toLowerCase())
}

export function transformObject2JSON (obj) {
  if (typeof obj !== 'object' || !obj) {
    return obj
  }
  if (obj instanceof Array) {
    return obj.map(transformObject2JSON)
  }
  const result = {}
  for (let key in obj) {
    const field = obj[key]
    key = snakeCase(key)
    if (field instanceof Date) {
      result[key] = field.toISOString()
    } else if (typeof field === 'object') {
      result[key] = transformObject2JSON(field)
    } else if (field !== undefined) {
      result[key] = field
    }
  }
  return result
}

export function transformJSON2Object (obj) {
  if (typeof obj !== 'object' || !obj) {
    return obj
  }
  if (obj instanceof Array) {
    return obj.map(transformJSON2Object)
  }
  const result = {}
  for (let key in obj) {
    const field = obj[key]
    const objKey = camelCase(key)
    if (TIME_FIELD.test(key) && typeof field === 'string') {
      result[objKey] = new Date(field)
    } else if (typeof field === 'object') {
      result[objKey] = transformJSON2Object(field)
    } else {
      result[objKey] = field
    }
  }
  return result
}

const CSRFRegex = /.*csrftoken=([^;.]*).*$/
const CSRFMatch = document.cookie.match(CSRFRegex)

const axios = _axios.create({
  headers: {
    'Content-Type': 'application/json',
    'X-Requested-With': 'XMLHttpRequest',
    // 'X-CSRFToken': CSRFMatch && CSRFMatch[1]
  }
})

axios.interceptors.request.use(config => {
  // handle authorization
  if (store.state.userToken) {
    config.headers['Authorization'] = `Token ${store.state.userToken}`
    config.headers['X-CSRFToken'] = document.cookie.match(CSRFRegex)[1]
  }
  if (config.headers['Content-Type'] === 'application/json') {
    config.data = transformObject2JSON(config.data)
  }
  return config
})

axios.interceptors.response.use(res => {
  if (res.headers['content-type'] === 'application/json') {
    res.data = transformJSON2Object(res.data)
  }
  return res
})

Vue.prototype.axios = axios

export default axios
