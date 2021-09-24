<template>
  <div class="error-alert">
    <b-modal 
      id="errorAlertModal" 
      title="Ошибка!" 
      header-bg-variant="danger"
      ok-only
      ref="modal"
    >
      <b-alert show variant="danger">{{ message }}</b-alert>
    </b-modal>
  </div>
</template>

<script>
import { onErrorEvent } from '@/events/utils.js'

export default {
  data() {
    return {
      message: '',
      timeout: 5000
    }
  },
  mounted() {
    onErrorEvent(this.open)
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