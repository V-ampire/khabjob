import http from "@/http/common";
import { getHttpErrorType } from "@/http/errors";


export class ApiClient {
  /**
   * Базовый класс для api клиента.
   * Содержит методы: [
   *  list()
   *  detail()
   *  create()
   *  update()
   *  delete()
   * ]
   */
  constructor(endpoint, accessToken=null) {
    /**
     * @endpoint - ресурс объекта
     * @accessToken - токен авторизации
     */
    this.endpoint = endpoint;
    this.accessToken = accessToken;
  }

  setAccessToken(accessToken) {
    this.accessToken = accessToken
  }

  async list(params={}) {
    /**
     * Загрузить список объектов.
     */
    let response
    let headers = {}
    if (this.accessToken) {
      headers['Authorization'] = `Bearer ${this.accessToken}`
    }
    try {
      response = await http.get(`${this.endpoint}`, {headers: headers, params: params})
    } catch (err) {
      throw getHttpErrorType(err)
    }
    return response
  }

  async detail(uuid) {
    /**
     * Загрузить информацю об объекте.
     */
    let response
    let headers = {}
    if (this.accessToken) {
      headers['Authorization'] = `Bearer ${this.accessToken}`
    }
    try {
      response = await http.get(`${this.endpoint}/${uuid}`, {headers: headers})
    } catch (err) {
      throw getHttpErrorType(err)
    }
    return response
  }

  async create(formData) {
    /**
     * Создать объект.
     */
    let response
    let headers = {}
    if (this.accessToken) {
      headers['Authorization'] = `Bearer ${this.accessToken}`
    }
    headers['Content-Type'] = 'multipart/form-data'
    try {
      response = await http.post(`${this.endpoint}`, formData, {headers: headers})
    } catch (err) {
      throw getHttpErrorType(err)
    }
    return response
  }

  async update(uuid, formData) {
    /**
     * Обновить данные объекта.
     */
    let response
    let headers = {}
    if (this.accessToken) {
      headers['Authorization'] = `Bearer ${this.accessToken}`
    }
    headers['Content-Type'] = 'multipart/form-data'
    try {
      response = await http.patch(`${this.endpoint}/${uuid}`, formData, {headers: headers})
    } catch (err) {
      throw getHttpErrorType(err)
    }
    return response
  }

  async delete(uuid) {
    /**
     * Удалить объект.
     */
    let response
    let headers = {}
    if (this.accessToken) {
      headers['Authorization'] = `Bearer ${this.accessToken}`
    }
    try {
      response = await http.delete(`${this.endpoint}/${uuid}`, {headers: headers})
    } catch (err) {
      throw getHttpErrorType(err)
    }
    return response
  }

  async delete_batch(params={}) {
    /**
     * Удалить объект.
     */
    let response
    let headers = {}
    if (this.accessToken) {
      headers['Authorization'] = `Bearer ${this.accessToken}`
    }
    try {
      response = await http.delete(`${this.endpoint}`, {headers: headers, params: params})
    } catch (err) {
      throw getHttpErrorType(err)
    }
    return response
  }
}


export class AuthorizationClient {
  /**
   * Базовый класс для клиента авторизации.
   * Содержит методы: [
   *  login()
   *  logout()
   * ]
   * TODO: Методы refresh, register
   */
   constructor(endpoint, accessToken=null) {
    /**
     * @endpoint - ресурс объекта
     * @accessToken - JWT access token
     */
    this.endpoint = endpoint;
    this.accessToken = accessToken;
  }

  setAccessToken(accessToken) {
    this.accessToken = accessToken
  }

  async login(formData) {
    /**
     * Получить токены.
     */
    let response
    const headers = {
      'Content-Type': 'multipart/form-data'
    }
    try {
      response = await http.post(`${this.endpoint}/login`, formData, {headers: headers})
    } catch (err) {
      throw getHttpErrorType(err)
    }
    return response
  }

  async logout() {
    /**
     * Разлогиниться.
     */
    let response
    let headers = {}
    if (this.accessToken) {
      headers['Authorization'] = `Bearer ${this.accessToken}`
    }
    try {
      response = await http.get(`${this.endpoint}/logout`, {headers: headers})
    } catch (err) {
      throw getHttpErrorType(err)
    }
    return response
  }
}


export class SearchClient {
  constructor(endpoint, accessToken=null) {
    /**
     * @endpoint - ресурс объекта
     * @accessToken - токен авторизации
     */
    this.endpoint = endpoint;
    this.accessToken = accessToken;
  }

  async search(params={}) {
    /**
     * Загрузить список объектов.
     */
    let response
    let headers = {}
    if (this.accessToken) {
      headers['Authorization'] = `Bearer ${this.accessToken}`
    }
    try {
      response = await http.get(`${this.endpoint}`, {headers: headers, params: params})
    } catch (err) {
      throw getHttpErrorType(err)
    }
    return response
  }
}
