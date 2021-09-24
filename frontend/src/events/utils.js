import { ON_APP_ERROR, ON_OPEN_CONFIRM, ON_CONFIRM_RESULT,  ON_APP_SUCCESS } 
  from '@/events/types'
import eventBus from '@/events/eventBus'


export function showErrorAlert(errorMessage) {
  eventBus.$emit(ON_APP_ERROR, errorMessage);
}


export function onErrorEvent(handler) {
  eventBus.$on(ON_APP_ERROR, handler);
}


export function showSuccessEvent(successMessage) {
  eventBus.$emit(ON_APP_SUCCESS, successMessage)
}


export function onSuccessEvent(handler) {
  eventBus.$on(ON_APP_SUCCESS, handler);
}


export function onConfirmAction(confirmParams, action) {
  /**
   * Set up handler for event with action confimation.
   * After confirm off handler.
   * @action - Callback to execute after action confimation,
   * Result of confirm will be passed to callback.
   * Open confirmation modal window.
   */
  eventBus.$on(ON_CONFIRM_RESULT, (confirm) => {
    eventBus.$off(ON_CONFIRM_RESULT);
    action(confirm);
  })
  eventBus.$emit(ON_OPEN_CONFIRM, confirmParams);
}


export function onOpenConfirmAction(handler) {
  eventBus.$on(ON_OPEN_CONFIRM, handler);
}


export function confirmAction(confirm) {
  eventBus.$emit(ON_CONFIRM_RESULT, confirm);
}
