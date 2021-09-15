export class HttpError extends Error {
  constructor(message) {
    super(message);
    this.name = "HttpError";
  }
}


export class ResponseFormatError extends HttpError {
  constructor(response) {
    super('Сервер венул неизвестный формат ответа...');
    this.name = "ResponseFormatError";
    this.data = response.data;
    this.response = response;
  }
}


export class ServerError extends HttpError {
  constructor(error) {
    super('Сервер вернул ошибку! Повторите попытку чуть позже...');
    this.name = "ServerError";
    this.error = error;
    this.data = error.response.data;
    this.status = error.response.status;
  }
}


export class RequestError extends HttpError {
  constructor(error) {
    super('Упс! Возникла ошибка, возможно, нет соединения с интернетом...');
    this.name = "RequestError";
    this.error = error;
  }
}


export class SettingRequestError extends HttpError {
  constructor(error) {
    super('Упс! Возникла какая то ошибка, повторите попытку чуть позже...');
    this.name = "SettingRequestError";
    this.error = error;
  }
}


export function getHttpErrorType(error) {
  /**
   * Обрабатывает ошибку при выполнении http запроса.
   * Возвращает объект нужного класса http ошибки.
   */
  let httpError;
  if (error.response) {
    httpError = new ServerError(error);
  } else if (error.request) {
    httpError = new RequestError(error);
  } else {
    httpError = new SettingRequestError(error);
  }
  return httpError
}
