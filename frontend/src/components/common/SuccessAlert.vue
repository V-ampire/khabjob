<template>
  <div class="success-alert">
    <b-modal 
      id="successAlertModal" 
      title="Успешно!" 
      header-bg-variant="success"
      ok-only
      ref="modal"
    >
      <b-alert show variant="success">{{ message }}</b-alert>
    </b-modal>
  </div>
</template>

<script>
import { onSuccessEvent } from '@/events/utils.js'

export default {
  data() {
    return {
      message: '',
      timeout: 5000
    }
  },
  mounted() {
    onSuccessEvent(this.open)
  },
  methods: {
    open (message) {
      this.message = message;
      this.$refs.modal.show()
      setTimeout(() => {
        this.close()
      }, this.timeout);
    },
    close () {
      this.$refs.modal.hide()
    }
  },
}
</script>