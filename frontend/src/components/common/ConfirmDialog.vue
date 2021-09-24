<template>
  <div class="confirm-dialog">
    <b-modal 
      id="confirmDialogModal" 
      title="Подтвердите действие." 
      header-bg-variant="primary"
      ref="modal"
      v-on:hide="cancel"
      v-on:ok="agree"
    >
      <b-alert show variant="danger">{{ message }}</b-alert>
    </b-modal>
  </div>
</template>

<script>
/**
 * Modal window to confirm actions.
 * Method open() return a Promise with result true/false
 * depending on action confirmation.
 */
import { onOpenConfirmAction, confirmAction } from '@/events/utils.js'

export default {
  data: function () {
    return {
      resolve: null,
      reject: null,
      message: null,
    }
  },
  mounted() {
    onOpenConfirmAction(this.open)
  },
  methods: {
    async getConfirmResult() {
      return new Promise((resolve, reject) => {
        this.resolve = resolve;
        this.reject = reject;
      });
    },
    agree() {
      this.resolve(true);
    },
    cancel() {
      this.resolve(false);
    },
    async open(confirmParams) {
      this.message = confirmParams.message
      this.$refs.modal.show()
      const result = await this.getConfirmResult()
      confirmAction(result)
    }
  }
}
</script>