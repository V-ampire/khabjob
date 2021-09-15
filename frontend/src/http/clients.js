import { ApiClient, AuthorizationClient } from '@/http/base';


export function authApi(accessToken=null) {
  const endpoint = '/auth';

  return new AuthorizationClient(endpoint, accessToken)
}


export function publicVacanciesApi(accessToken=null) {
  const endpoint = '/public/vacancies';

  return new ApiClient(endpoint, accessToken)
}