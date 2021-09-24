import { authApi } from '@/http/clients'
import { ResponseFormatError } from '@/http/errors'

const LS_USER_KEY = 'user'
const LS_TOKEN_KEY = 'token'

const initUser = JSON.parse(localStorage.getItem(LS_USER_KEY))
const initToken = JSON.parse(localStorage.getItem(LS_TOKEN_KEY))

export default {
  namespaced: true,
  state: () => ({
    user: initUser,
    token: initToken,
  }),
  getters: {
    isAuthenticated: state => {
      return Boolean(state.user && state.token)
    }
  },
  mutations: {
    SET_USER(state, user) {
      localStorage.setItem(LS_USER_KEY, JSON.stringify(user))
      state.user = user
    },
    SET_TOKEN(state, token) {
      localStorage.setItem(LS_TOKEN_KEY, JSON.stringify(token))
      state.token = token
    },
    REMOVE_USER(state) {
      localStorage.removeItem(LS_USER_KEY)
      state.user = null
    },
    REMOVE_TOKEN(state) {
      localStorage.removeItem(LS_TOKEN_KEY)
      state.token = null
    }
  },
  actions: {
    async LOGIN({ commit }, credentials) {
      const response = await authApi().login(credentials)

      if (!response.data.user && !response.data.jwt_token) {
        throw ResponseFormatError()
      }

      commit('SET_USER', response.data.user)
      commit('SET_TOKEN', response.data.jwt_token)
    },
    async LOGOUT({ state, commit }) {
      await authApi(state.token).logout()

      commit('REMOVE_USER')
      commit('REMOVE_TOKEN')
    }
  }
}