import axios from 'axios'
import { ON_APP_LOGOUT } from '@/events/types.js'
import eventBus from '@/events/eventBus.js'

import config from '@/config'


const http = axios.create({
	baseURL: config.apiRoot
})


http.interceptors.response.use((response) => {
  return response
}, (error) => {
  if (error.request.status === 401 && error.config && !error.config.__isRetryRequest) {
    eventBus.$emit(ON_APP_LOGOUT)
  }
  return Promise.reject(error);
})


export default http;