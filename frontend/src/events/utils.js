import { ON_APP_ERROR, ON_OPEN_CONFIRM, ON_CONFIRM_RESULT,  ON_APP_SUCCESS, ON_RELOAD } 
  from '@/events/types'
import eventBus from '@/events/eventBus'


export function showErrorAlert(errorMessage) {
  /**
   * Показать окно с ошибкой.
   * @errorMessage - сообщение об ошибке
   */
  eventBus.$emit(ON_APP_ERROR, errorMessage);
}


export function onErrorEvent(handler) {
  /**
   * Вклюить обработку ошибок.
   * @handler - обработчик в который будет передано сообщение об ошибке.
   */
  eventBus.$on(ON_APP_ERROR, handler);
}


export function showSuccessEvent(successMessage) {
  /**
   * Показать окно успешным результатом.
   */
  eventBus.$emit(ON_APP_SUCCESS, successMessage)
}


export function onSuccessEvent(handler) {
  /**
   * Включить обработку успешных сообщений.
   * @handler - обработчик в который будет передано сообщение.
   */
  eventBus.$on(ON_APP_SUCCESS, handler);
}


export function onConfirmAction(confirmParams, action) {
  /**
   * Установить обработчик события подтверждения.
   * После подтверждения удаляет обработчик.
   * @action - Колбек, который нужно выполнить при подтверждении, в колбек будет
   * передан результат подтверждения.
   * Вызвать событие для открытия окна подтверждения.
   */
  eventBus.$on(ON_CONFIRM_RESULT, (confirm) => {
    eventBus.$off(ON_CONFIRM_RESULT);
    action(confirm);
  })
  eventBus.$emit(ON_OPEN_CONFIRM, confirmParams);
}


export function onOpenConfirmAction(handler) {
  /**
   * Включает обработку события на открытие окна подтверждения.
   */
  eventBus.$on(ON_OPEN_CONFIRM, handler);
}


export function confirmAction(confirm) {
  /**
   * Вызывает событие подтверждения действия с результатом подтверждения.
   * @confirm - рзультат подтверждения действия.
   */
  eventBus.$emit(ON_CONFIRM_RESULT, confirm);
}


export function onReloadEvent(handler) {
  /**
   * Устанавливает обработчик на событие обновление данных.
   */
  eventBus.$on(ON_RELOAD, handler);
}


export function offReloadEvent(handler) {
  eventBus.$off(ON_RELOAD, handler);
}


export function reloadData(params) {
  /**
   * Вызывает обновление данных.
   */
  eventBus.$emit(ON_RELOAD, params);
}
